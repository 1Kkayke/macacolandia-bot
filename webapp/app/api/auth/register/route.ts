import { NextResponse } from 'next/server';
import bcrypt from 'bcryptjs';
import { createPendingRegistration, getUserByEmail } from '@/lib/auth-db';
import { sendRegistrationNotification } from '@/lib/email';

export async function POST(request: Request) {
  try {
    const body = await request.json();
    const { name, email, password } = body;

    // Validation
    if (!name || !email || !password) {
      return NextResponse.json(
        { error: 'Todos os campos são obrigatórios' },
        { status: 400 }
      );
    }

    if (password.length < 6) {
      return NextResponse.json(
        { error: 'A senha deve ter pelo menos 6 caracteres' },
        { status: 400 }
      );
    }

    // Check if user already exists
    const existingUser = getUserByEmail(email);
    if (existingUser) {
      return NextResponse.json(
        { error: 'Este email já está cadastrado' },
        { status: 400 }
      );
    }

    // Hash password
    const hashedPassword = await bcrypt.hash(password, 10);

    // Get IP and user agent
    const ipAddress = request.headers.get('x-forwarded-for') || 
                      request.headers.get('x-real-ip') || 
                      null;
    const userAgent = request.headers.get('user-agent') || null;

    // Create pending registration
    const registrationId = createPendingRegistration(
      name,
      email,
      hashedPassword,
      ipAddress,
      userAgent
    );

    // Send email notification to admin
    const emailSent = await sendRegistrationNotification({
      name,
      email,
      ipAddress,
      userAgent,
      requestedAt: new Date().toISOString(),
      registrationId,
    });

    return NextResponse.json({
      success: true,
      message: 'Solicitação de registro enviada com sucesso! Aguarde a aprovação do administrador.',
      emailSent,
    });
  } catch (error) {
    console.error('Registration error:', error);
    return NextResponse.json(
      { error: 'Erro ao processar registro' },
      { status: 500 }
    );
  }
}
