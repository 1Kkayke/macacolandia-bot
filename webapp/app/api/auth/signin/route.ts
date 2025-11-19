import { NextRequest, NextResponse } from 'next/server';
import bcrypt from 'bcryptjs';
import { getUserByEmail } from '@/lib/auth-db';
import { 
  isAccountLocked, 
  recordFailedAttempt, 
  clearFailedAttempts, 
  checkAndLockAccount,
  logSecurityEvent, 
  getClientIp, 
  getUserAgent 
} from '@/lib/security';
import { signIn } from '@/lib/auth';

export async function POST(request: NextRequest) {
  const ip = getClientIp(request);
  const userAgent = getUserAgent(request);

  try {
    const body = await request.json();
    const { email, password } = body;

    if (!email || !password) {
      return NextResponse.json(
        { error: 'Email e senha são obrigatórios' },
        { status: 400 }
      );
    }

    // Verificar se conta está bloqueada
    const lockStatus = isAccountLocked(email);
    if (lockStatus.locked) {
      logSecurityEvent({
        event_type: 'login_attempt_locked_account',
        severity: 'medium',
        email,
        ip_address: ip,
        user_agent: userAgent,
        details: lockStatus.message || 'Tentativa de login em conta bloqueada',
      });

      return NextResponse.json(
        { 
          error: lockStatus.message || 'Conta bloqueada temporariamente. Tente novamente mais tarde.',
          locked: true,
          retryAfter: lockStatus.lockedUntil 
        },
        { status: 423 } // 423 Locked
      );
    }

    // Buscar usuário
    const user = getUserByEmail(email);

    if (!user) {
      // Registrar tentativa falha
      recordFailedAttempt(email, ip, userAgent, 'Email não encontrado');
      checkAndLockAccount(email);

      logSecurityEvent({
        event_type: 'login_attempt_invalid_user',
        severity: 'low',
        email,
        ip_address: ip,
        user_agent: userAgent,
        details: 'Tentativa de login com email não cadastrado',
      });

      return NextResponse.json(
        { error: 'Email ou senha incorretos' },
        { status: 401 }
      );
    }

    // Verificar se está aprovado
    if (!user.approved) {
      logSecurityEvent({
        event_type: 'login_attempt_unapproved',
        severity: 'low',
        email,
        ip_address: ip,
        user_agent: userAgent,
        details: 'Tentativa de login com conta não aprovada',
      });

      return NextResponse.json(
        { 
          error: 'Sua conta ainda não foi aprovada pelo administrador. Por favor, aguarde a aprovação.',
          unapproved: true
        },
        { status: 403 }
      );
    }

    // Verificar se está bloqueado permanentemente
    if (user.blocked) {
      logSecurityEvent({
        event_type: 'login_attempt_blocked_user',
        severity: 'medium',
        email,
        ip_address: ip,
        user_agent: userAgent,
        details: 'Tentativa de login com conta bloqueada permanentemente',
      });

      return NextResponse.json(
        { 
          error: 'Sua conta foi bloqueada. Entre em contato com o administrador.',
          blocked: true
        },
        { status: 403 }
      );
    }

    // Verificar senha
    const passwordMatch = await bcrypt.compare(password, user.password);

    if (!passwordMatch) {
      // Registrar tentativa falha
      recordFailedAttempt(email, ip, userAgent, 'Senha incorreta');
      const lockResult = checkAndLockAccount(email);

      logSecurityEvent({
        event_type: 'login_failed_wrong_password',
        severity: 'medium',
        email,
        ip_address: ip,
        user_agent: userAgent,
        details: `Senha incorreta - Tentativas: ${lockResult.attempts}`,
      });

      if (lockResult.shouldLock) {
        return NextResponse.json(
          { 
            error: `Muitas tentativas falhas. Sua conta foi bloqueada temporariamente por 15 minutos.`,
            locked: true,
            attempts: lockResult.attempts
          },
          { status: 423 }
        );
      }

      return NextResponse.json(
        { 
          error: 'Email ou senha incorretos',
          attempts: lockResult.attempts,
          remainingAttempts: Math.max(0, 5 - lockResult.attempts)
        },
        { status: 401 }
      );
    }

    // Login bem-sucedido - limpar tentativas falhas
    clearFailedAttempts(email);
    
    logSecurityEvent({
      event_type: 'login_success',
      severity: 'low',
      email,
      ip_address: ip,
      user_agent: userAgent,
      details: `Login bem-sucedido - Role: ${user.role}`,
    });

    // Fazer login via NextAuth
    try {
      const result = await signIn('credentials', {
        email,
        password,
        redirect: false,
      });

      if (result?.error) {
        return NextResponse.json(
          { error: 'Erro ao criar sessão' },
          { status: 500 }
        );
      }

      return NextResponse.json({
        success: true,
        user: {
          id: user.id,
          name: user.name,
          email: user.email,
          role: user.role,
        },
      });
    } catch (authError) {
      console.error('[SIGNIN] Erro ao criar sessão:', authError);
      return NextResponse.json(
        { error: 'Erro ao criar sessão' },
        { status: 500 }
      );
    }
  } catch (error) {
    console.error('[SIGNIN] Erro não tratado:', error);
    const errorMessage = error instanceof Error ? error.message : 'Erro desconhecido';
    
    logSecurityEvent({
      event_type: 'login_unexpected_error',
      severity: 'critical',
      email: 'unknown',
      ip_address: ip,
      user_agent: userAgent,
      details: `Erro inesperado: ${errorMessage}`,
    });

    return NextResponse.json(
      { error: 'Erro ao processar login. Tente novamente.' },
      { status: 500 }
    );
  }
}
