/**
 * Middleware do Next.js para segurança
 * Implementa rate limiting, headers de segurança e proteções
 */

import { NextResponse } from 'next/server';
import type { NextRequest } from 'next/server';

// Rate limiting em memória (use Redis em produção para múltiplas instâncias)
const requestCounts = new Map<string, { count: number; resetTime: number }>();

function getRateLimitKey(ip: string, path: string): string {
  return `${ip}:${path}`;
}

function checkRateLimit(ip: string, path: string, maxRequests: number, windowMs: number): {
  allowed: boolean;
  remaining: number;
  resetTime: number;
} {
  const key = getRateLimitKey(ip, path);
  const now = Date.now();
  const entry = requestCounts.get(key);

  // Se não existe ou expirou
  if (!entry || now > entry.resetTime) {
    requestCounts.set(key, {
      count: 1,
      resetTime: now + windowMs,
    });
    return {
      allowed: true,
      remaining: maxRequests - 1,
      resetTime: now + windowMs,
    };
  }

  // Se atingiu o limite
  if (entry.count >= maxRequests) {
    return {
      allowed: false,
      remaining: 0,
      resetTime: entry.resetTime,
    };
  }

  // Incrementar
  entry.count++;
  return {
    allowed: true,
    remaining: maxRequests - entry.count,
    resetTime: entry.resetTime,
  };
}

// Limpeza periódica
setInterval(() => {
  const now = Date.now();
  for (const [key, entry] of requestCounts.entries()) {
    if (now > entry.resetTime) {
      requestCounts.delete(key);
    }
  }
}, 60000); // A cada minuto

export function middleware(request: NextRequest) {
  const { pathname } = request.nextUrl;
  
  // Extrair IP
  const ip = request.headers.get('x-forwarded-for')?.split(',')[0].trim() ||
             request.headers.get('x-real-ip') ||
             'unknown';

  // ===== RATE LIMITING POR ROTA =====
  let rateLimitConfig: { maxRequests: number; windowMs: number } | null = null;

  if (pathname.startsWith('/api/auth/login') || pathname === '/auth/login') {
    rateLimitConfig = { maxRequests: 10, windowMs: 5 * 60 * 1000 }; // 10 req/5min
  } else if (pathname.startsWith('/api/auth/register') || pathname === '/auth/register') {
    rateLimitConfig = { maxRequests: 5, windowMs: 60 * 60 * 1000 }; // 5 req/1hora
  } else if (pathname.startsWith('/api/')) {
    rateLimitConfig = { maxRequests: 100, windowMs: 60 * 1000 }; // 100 req/1min (API geral)
  }

  if (rateLimitConfig) {
    const { allowed, remaining, resetTime } = checkRateLimit(
      ip,
      pathname,
      rateLimitConfig.maxRequests,
      rateLimitConfig.windowMs
    );

    if (!allowed) {
      const retryAfter = Math.ceil((resetTime - Date.now()) / 1000);
      return new NextResponse(
        JSON.stringify({
          error: 'Muitas requisições. Por favor, tente novamente mais tarde.',
          retryAfter,
        }),
        {
          status: 429,
          headers: {
            'Content-Type': 'application/json',
            'Retry-After': retryAfter.toString(),
            'X-RateLimit-Limit': rateLimitConfig.maxRequests.toString(),
            'X-RateLimit-Remaining': '0',
            'X-RateLimit-Reset': resetTime.toString(),
          },
        }
      );
    }

    // Adicionar headers de rate limit na resposta
    const response = NextResponse.next();
    response.headers.set('X-RateLimit-Limit', rateLimitConfig.maxRequests.toString());
    response.headers.set('X-RateLimit-Remaining', remaining.toString());
    response.headers.set('X-RateLimit-Reset', resetTime.toString());
  }

  // ===== HEADERS DE SEGURANÇA =====
  const response = NextResponse.next();

  // Content Security Policy
  response.headers.set(
    'Content-Security-Policy',
    [
      "default-src 'self'",
      "script-src 'self' 'unsafe-eval' 'unsafe-inline' https://www.google.com https://www.gstatic.com",
      "style-src 'self' 'unsafe-inline'",
      "img-src 'self' data: https:",
      "font-src 'self' data:",
      "connect-src 'self'",
      "frame-src 'self' https://www.google.com",
      "frame-ancestors 'none'",
      "base-uri 'self'",
      "form-action 'self'",
    ].join('; ')
  );

  // Proteger contra clickjacking
  response.headers.set('X-Frame-Options', 'DENY');

  // Prevenir MIME type sniffing
  response.headers.set('X-Content-Type-Options', 'nosniff');

  // XSS Protection (legado mas ainda útil)
  response.headers.set('X-XSS-Protection', '1; mode=block');

  // Referrer Policy
  response.headers.set('Referrer-Policy', 'strict-origin-when-cross-origin');

  // Permissions Policy
  response.headers.set(
    'Permissions-Policy',
    'camera=(), microphone=(), geolocation=(), interest-cohort=()'
  );

  // HSTS (HTTP Strict Transport Security) - apenas em produção
  if (process.env.NODE_ENV === 'production') {
    response.headers.set(
      'Strict-Transport-Security',
      'max-age=31536000; includeSubDomains; preload'
    );
  }

  return response;
}

// Configurar quais rotas o middleware deve processar
export const config = {
  matcher: [
    /*
     * Match all request paths except:
     * - _next/static (static files)
     * - _next/image (image optimization files)
     * - favicon.ico (favicon file)
     * - public folder
     */
    '/((?!_next/static|_next/image|favicon.ico|.*\\.(?:svg|png|jpg|jpeg|gif|webp)$).*)',
  ],
};
