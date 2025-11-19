import { handlers } from '@/lib/auth';
import { NextRequest, NextResponse } from 'next/server';
import {
  recordFailedAttempt,
  checkAndLockAccount,
  getClientIp,
  getUserAgent,
} from '@/lib/security';

// Export GET and POST handlers wrapped with debug-friendly try/catch.
// When NEXTAUTH_DEBUG=true (or in non-production), this will return
// a JSON body with message and stack to help troubleshooting.

export const GET = async (request: NextRequest) => {
  try {
    return await handlers.GET(request as any);
  } catch (err) {
    console.error('[NEXTAUTH][GET] Unhandled error:', err);
    const isDebug = process.env.NEXTAUTH_DEBUG === 'true' || process.env.NODE_ENV !== 'production';
    if (isDebug) {
      return NextResponse.json(
        { error: (err as any)?.message || 'internal error', stack: (err as any)?.stack || null },
        { status: 500 }
      );
    }
    return NextResponse.json({ error: 'Internal server error' }, { status: 500 });
  }
};

export async function POST(request: NextRequest) {
  try {
    const originalHandler = handlers.POST;

    // Capturar o resultado da autenticação
    const response = await originalHandler(request as any);

    // Se for uma requisição de callback de signin
    if (request.url.includes('callback/credentials')) {
      // Verificar se houve erro na resposta
      const responseClone = response.clone();

      try {
        const data = await responseClone.json();

        // Se houver erro de autenticação
        if (data?.error || response.status === 401) {
          const body = await request.json().catch(() => ({}));
          const email = body?.email;

          if (email) {
            const ip = getClientIp(request);
            const userAgent = getUserAgent(request);

            // Registrar tentativa falha
            recordFailedAttempt(
              email,
              ip,
              userAgent,
              'Senha incorreta ou credenciais inválidas'
            );

            // Verificar se deve bloquear
            const lockResult = checkAndLockAccount(email);
            if (lockResult.shouldLock) {
              console.warn(`[AUTH] Conta bloqueada após ${lockResult.attempts} tentativas: ${email}`);
            }
          }
        }
      } catch (e) {
        // Ignorar erros de parsing, retornar resposta original
      }
    }

    return response;
  } catch (err) {
    console.error('[NEXTAUTH][POST] Unhandled error:', err);
    const isDebug = process.env.NEXTAUTH_DEBUG === 'true' || process.env.NODE_ENV !== 'production';
    if (isDebug) {
      return NextResponse.json(
        { error: (err as any)?.message || 'internal error', stack: (err as any)?.stack || null },
        { status: 500 }
      );
    }
    return NextResponse.json({ error: 'Internal server error' }, { status: 500 });
  }
}
