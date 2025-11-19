import NextAuth, { NextAuthConfig } from 'next-auth';
import Credentials from 'next-auth/providers/credentials';
import bcrypt from 'bcryptjs';
import { getUserByEmail } from './auth-db';
import { 
  isAccountLocked, 
  clearFailedAttempts, 
  logSecurityEvent, 
  getClientIp, 
  getUserAgent 
} from './security';

export const authConfig: NextAuthConfig = {
  providers: [
    Credentials({
      name: 'credentials',
      credentials: {
        email: { label: 'Email', type: 'email' },
        password: { label: 'Senha', type: 'password' },
      },
      async authorize(credentials, req) {
        if (!credentials?.email || !credentials?.password) {
          return null;
        }

        const email = credentials.email as string;
        const password = credentials.password as string;

        // Extrair IP e User Agent para logs
        const ip = getClientIp(req as any);
        const userAgent = getUserAgent(req as any);

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
          throw new Error(lockStatus.message || 'Conta bloqueada temporariamente.');
        }

        const user = getUserByEmail(email);

        if (!user) {
          logSecurityEvent({
            event_type: 'login_attempt_invalid_user',
            severity: 'low',
            email,
            ip_address: ip,
            user_agent: userAgent,
            details: 'Tentativa de login com email não cadastrado',
          });
          return null;
        }

        // Check if user is approved and not blocked
        if (!user.approved) {
          logSecurityEvent({
            event_type: 'login_attempt_unapproved',
            severity: 'low',
            email,
            ip_address: ip,
            user_agent: userAgent,
            details: 'Tentativa de login com conta não aprovada',
          });
          throw new Error('Sua conta ainda não foi aprovada pelo administrador.');
        }

        if (user.blocked) {
          logSecurityEvent({
            event_type: 'login_attempt_blocked_user',
            severity: 'medium',
            email,
            ip_address: ip,
            user_agent: userAgent,
            details: 'Tentativa de login com conta bloqueada permanentemente',
          });
          throw new Error('Sua conta foi bloqueada.');
        }

        // Verificar senha
        const passwordMatch = await bcrypt.compare(password, user.password);

        if (!passwordMatch) {
          logSecurityEvent({
            event_type: 'login_failed_wrong_password',
            severity: 'medium',
            email,
            ip_address: ip,
            user_agent: userAgent,
            details: 'Senha incorreta',
          });
          return null;
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

        return {
          id: user.id.toString(),
          name: user.name,
          email: user.email,
          role: user.role,
        };
      },
    }),
  ],
  callbacks: {
    async jwt({ token, user }) {
      if (user) {
        token.id = user.id;
        token.role = (user as any).role;
      }
      return token;
    },
    async session({ session, token }) {
      if (session.user) {
        (session.user as any).id = token.id;
        (session.user as any).role = token.role;
      }
      return session;
    },
  },
  pages: {
    signIn: '/auth/login',
    error: '/auth/error',
  },
  session: {
    strategy: 'jwt',
    maxAge: 30 * 24 * 60 * 60, // 30 dias
  },
  cookies: {
    sessionToken: {
      name: `${process.env.NODE_ENV === 'production' ? '__Secure-' : ''}next-auth.session-token`,
      options: {
        httpOnly: true,
        sameSite: 'lax',
        path: '/',
        secure: process.env.NODE_ENV === 'production',
      },
    },
  },
  // Configurações de segurança adicionais
  useSecureCookies: process.env.NODE_ENV === 'production',
  debug: process.env.NODE_ENV === 'development',
};

export const { handlers, auth, signIn, signOut } = NextAuth(authConfig);
