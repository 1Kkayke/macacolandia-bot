import { NextResponse } from 'next/server';
import bcrypt from 'bcryptjs';
import { createPendingRegistration, getUserByEmail } from '@/lib/auth-db';
import { sendRegistrationNotification } from '@/lib/email';

export async function POST(request: Request) {
  try {
    const body = await request.json();
    const { name, email, password } = body;

    console.log('[REGISTER] Nova solicitação de registro:', { name, email });

    // Validation
    if (!name || !email || !password) {
      console.log('[REGISTER] Validação falhou: campos obrigatórios');
      return NextResponse.json(
        { error: 'Todos os campos são obrigatórios' },
        { status: 400 }
      );
    }

    if (password.length < 6) {
      console.log('[REGISTER] Validação falhou: senha muito curta');
      return NextResponse.json(
        { error: 'A senha deve ter pelo menos 6 caracteres' },
        { status: 400 }
      );
    }

    // Check if user already exists
    console.log('[REGISTER] Verificando se email já existe...');
    try {
      const existingUser = getUserByEmail(email);
      if (existingUser) {
        console.log('[REGISTER] Email já cadastrado:', email);
        return NextResponse.json(
          { error: 'Este email já está cadastrado' },
          { status: 400 }
        );
      }
    } catch (dbError) {
      console.error('[REGISTER] Erro ao verificar email existente:', dbError);
      return NextResponse.json(
        { error: 'Erro ao verificar email no banco de dados' },
        { status: 500 }
      );
    }

    // Hash password
    console.log('[REGISTER] Gerando hash da senha...');
    const hashedPassword = await bcrypt.hash(password, 10);

    // Get IP and user agent
    const ipAddress = request.headers.get('x-forwarded-for') || 
                      request.headers.get('x-real-ip') || 
                      null;
    const userAgent = request.headers.get('user-agent') || null;

    // Create pending registration
    console.log('[REGISTER] Criando registro pendente...');
    let registrationId;
    try {
      registrationId = createPendingRegistration(
        name,
        email,
        hashedPassword,
        ipAddress,
        userAgent
      );
      console.log('[REGISTER] Registro pendente criado com ID:', registrationId);
    } catch (dbError) {
      console.error('[REGISTER] Erro ao criar registro pendente:', dbError);
      return NextResponse.json(
        { error: 'Erro ao salvar registro no banco de dados' },
        { status: 500 }
      );
    }

    // Send email notification to admin
    console.log('[REGISTER] Enviando notificação por email...');
    try {
      const emailSent = await sendRegistrationNotification({
        name,
        email,
        ipAddress,
        userAgent,
        requestedAt: new Date().toISOString(),
        registrationId,
      });
      console.log('[REGISTER] Email enviado:', emailSent);
    } catch (emailError) {
      console.error('[REGISTER] Erro ao enviar email (não crítico):', emailError);
      // Não falha o registro se o email falhar
    }

    console.log('[REGISTER] Registro concluído com sucesso!');
    return NextResponse.json({
      success: true,
      message: 'Solicitação de registro enviada com sucesso! Aguarde a aprovação do administrador.',
    });
  } catch (error) {
    console.error('[REGISTER] Erro não tratado:', error);
    const errorMessage = error instanceof Error ? error.message : 'Erro desconhecido';
    return NextResponse.json(
      { error: `Erro ao processar registro: ${errorMessage}` },
      { status: 500 }
    );
  }
}
