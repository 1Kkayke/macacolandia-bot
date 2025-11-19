import { handlers } from '@/lib/auth';
import { NextResponse } from 'next/server';
import {
  recordFailedAttempt,
  checkAndLockAccount,
  getClientIp,
  getUserAgent,
} from '@/lib/security';

// Handler GET padrão
export const GET = handlers.GET;

// Wrapper para POST que adiciona lógica de tentativas falhas
export async function POST(request: Request) {
  const originalHandler = handlers.POST;
  
  // Capturar o resultado da autenticação
  const response = await originalHandler(request);
  
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
}
