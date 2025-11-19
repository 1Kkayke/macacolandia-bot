import { NextResponse } from 'next/server';
import bcrypt from 'bcryptjs';
import { createPendingRegistration, getUserByEmail } from '@/lib/auth-db';
import { sendRegistrationNotification } from '@/lib/email';
import {
  validateName,
  validateEmail,
  validatePassword,
  sanitizeInput,
  sanitizeEmail,
  validateSqlInput,
} from '@/lib/validation';
import {
  checkRateLimit,
  clearRateLimit,
  logSecurityEvent,
  verifyRecaptcha,
  getClientIp,
  getUserAgent,
} from '@/lib/security';

export async function POST(request: Request) {
  const ip = getClientIp(request);
  const userAgent = getUserAgent(request);

  try {
    const body = await request.json();
    const { name, email, password, recaptchaToken } = body;

    console.log('[REGISTER] Nova solicitação de registro:', { name, email, ip });

    // ===== VERIFICAR RATE LIMIT =====
    const rateLimit = checkRateLimit(ip, 'register');
    if (!rateLimit.allowed) {
      logSecurityEvent({
        event_type: 'register_rate_limit_exceeded',
        severity: 'medium',
        email: email || 'unknown',
        ip_address: ip,
        user_agent: userAgent,
        details: `Rate limit excedido: ${rateLimit.message}`,
      });

      return NextResponse.json(
        { error: rateLimit.message || 'Muitas tentativas. Tente mais tarde.' },
        { status: 429 }
      );
    }

    // ===== VALIDAR CAMPOS OBRIGATÓRIOS =====
    if (!name || !email || !password) {
      logSecurityEvent({
        event_type: 'register_missing_fields',
        severity: 'low',
        email: email || 'unknown',
        ip_address: ip,
        user_agent: userAgent,
        details: 'Campos obrigatórios ausentes',
      });

      return NextResponse.json(
        { error: 'Todos os campos são obrigatórios' },
        { status: 400 }
      );
    }

    // ===== VERIFICAR RECAPTCHA =====
    if (process.env.NODE_ENV === 'production' || process.env.RECAPTCHA_SECRET_KEY) {
      if (!recaptchaToken) {
        logSecurityEvent({
          event_type: 'register_missing_captcha',
          severity: 'medium',
          email,
          ip_address: ip,
          user_agent: userAgent,
          details: 'Token de captcha ausente',
        });

        return NextResponse.json(
          { error: 'Verificação de captcha é obrigatória' },
          { status: 400 }
        );
      }

      const captchaResult = await verifyRecaptcha(recaptchaToken, ip);
      if (!captchaResult.success) {
        logSecurityEvent({
          event_type: 'register_invalid_captcha',
          severity: 'high',
          email,
          ip_address: ip,
          user_agent: userAgent,
          details: `Captcha inválido: ${captchaResult.error}`,
        });

        return NextResponse.json(
          { error: 'Verificação de captcha falhou. Tente novamente.' },
          { status: 400 }
        );
      }
    }

    // ===== SANITIZAR E VALIDAR INPUTS =====
    const sanitizedName = sanitizeInput(name.trim());
    const sanitizedEmail = sanitizeEmail(email);

    // Validar nome
    const nameValidation = validateName(sanitizedName);
    if (!nameValidation.valid) {
      return NextResponse.json(
        { error: nameValidation.error },
        { status: 400 }
      );
    }

    // Validar email
    const emailValidation = validateEmail(sanitizedEmail);
    if (!emailValidation.valid) {
      logSecurityEvent({
        event_type: 'register_invalid_email',
        severity: 'low',
        email: sanitizedEmail,
        ip_address: ip,
        user_agent: userAgent,
        details: emailValidation.error || 'Email inválido',
      });

      return NextResponse.json(
        { error: emailValidation.error },
        { status: 400 }
      );
    }

    // Validar senha
    const passwordValidation = validatePassword(password);
    if (!passwordValidation.valid) {
      return NextResponse.json(
        { error: passwordValidation.error },
        { status: 400 }
      );
    }

    // ===== PROTEÇÃO SQL INJECTION =====
    if (!validateSqlInput(sanitizedName) || !validateSqlInput(sanitizedEmail)) {
      logSecurityEvent({
        event_type: 'register_sql_injection_attempt',
        severity: 'critical',
        email: sanitizedEmail,
        ip_address: ip,
        user_agent: userAgent,
        details: 'Tentativa de SQL injection detectada',
      });

      return NextResponse.json(
        { error: 'Entrada inválida detectada' },
        { status: 400 }
      );
    }

    // ===== VERIFICAR SE EMAIL JÁ EXISTE =====
    console.log('[REGISTER] Verificando se email já existe...');
    try {
      const existingUser = getUserByEmail(sanitizedEmail);
      if (existingUser) {
        console.log('[REGISTER] Email já cadastrado:', sanitizedEmail);
        
        logSecurityEvent({
          event_type: 'register_duplicate_email',
          severity: 'low',
          email: sanitizedEmail,
          ip_address: ip,
          user_agent: userAgent,
          details: 'Tentativa de registro com email já cadastrado',
        });

        return NextResponse.json(
          { error: 'Este email já está cadastrado' },
          { status: 400 }
        );
      }
    } catch (dbError) {
      console.error('[REGISTER] Erro ao verificar email existente:', dbError);
      
      logSecurityEvent({
        event_type: 'register_database_error',
        severity: 'high',
        email: sanitizedEmail,
        ip_address: ip,
        user_agent: userAgent,
        details: `Erro ao verificar email: ${dbError}`,
      });

      return NextResponse.json(
        { error: 'Erro ao verificar email no banco de dados' },
        { status: 500 }
      );
    }

    // ===== HASH DA SENHA =====
    console.log('[REGISTER] Gerando hash da senha...');
    const hashedPassword = await bcrypt.hash(password, 12); // 12 rounds para segurança extra

    // ===== CRIAR REGISTRO PENDENTE =====
    console.log('[REGISTER] Criando registro pendente...');
    let registrationId;
    try {
      registrationId = createPendingRegistration(
        sanitizedName,
        sanitizedEmail,
        hashedPassword,
        ip,
        userAgent
      );
      console.log('[REGISTER] Registro pendente criado com ID:', registrationId);
    } catch (dbError) {
      console.error('[REGISTER] Erro ao criar registro pendente:', dbError);
      
      logSecurityEvent({
        event_type: 'register_database_error',
        severity: 'high',
        email: sanitizedEmail,
        ip_address: ip,
        user_agent: userAgent,
        details: `Erro ao criar registro: ${dbError}`,
      });

      return NextResponse.json(
        { error: 'Erro ao salvar registro no banco de dados' },
        { status: 500 }
      );
    }

    // ===== ENVIAR EMAIL DE NOTIFICAÇÃO =====
    console.log('[REGISTER] Enviando notificação por email...');
    try {
      const emailSent = await sendRegistrationNotification({
        name: sanitizedName,
        email: sanitizedEmail,
        ipAddress: ip,
        userAgent,
        requestedAt: new Date().toISOString(),
        registrationId,
      });
      console.log('[REGISTER] Email enviado:', emailSent);
    } catch (emailError) {
      console.error('[REGISTER] Erro ao enviar email (não crítico):', emailError);
      // Não falha o registro se o email falhar
    }

    // ===== LIMPAR RATE LIMIT APÓS SUCESSO =====
    clearRateLimit(ip, 'register');

    // ===== LOG DE SUCESSO =====
    logSecurityEvent({
      event_type: 'register_success',
      severity: 'low',
      email: sanitizedEmail,
      ip_address: ip,
      user_agent: userAgent,
      details: `Registro pendente criado com sucesso - ID: ${registrationId}`,
    });

    console.log('[REGISTER] Registro concluído com sucesso!');
    return NextResponse.json({
      success: true,
      message: 'Solicitação de registro enviada com sucesso! Aguarde a aprovação do administrador.',
    });
  } catch (error) {
    console.error('[REGISTER] Erro não tratado:', error);
    const errorMessage = error instanceof Error ? error.message : 'Erro desconhecido';
    
    logSecurityEvent({
      event_type: 'register_unexpected_error',
      severity: 'critical',
      email: 'unknown',
      ip_address: ip,
      user_agent: userAgent,
      details: `Erro inesperado: ${errorMessage}`,
    });

    return NextResponse.json(
      { error: 'Erro ao processar registro. Tente novamente.' },
      { status: 500 }
    );
  }
}
