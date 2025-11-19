/**
 * Validações centralizadas para formulários e inputs
 * Implementa validações robustas seguindo padrões de segurança
 */

import { z } from 'zod';

// ===== USERNAME VALIDATION =====
// Regras: 3-15 caracteres, apenas alfanuméricos e underscore, sem espaços
export const usernameSchema = z
  .string()
  .min(3, 'Username deve ter pelo menos 3 caracteres')
  .max(15, 'Username deve ter no máximo 15 caracteres')
  .regex(/^[a-zA-Z0-9_]+$/, 'Username deve conter apenas letras, números e underscore')
  .regex(/^\S+$/, 'Username não pode conter espaços');

export function validateUsername(username: string): { valid: boolean; error?: string } {
  try {
    usernameSchema.parse(username);
    return { valid: true };
  } catch (error) {
    if (error instanceof z.ZodError) {
      return { valid: false, error: error.issues[0].message };
    }
    return { valid: false, error: 'Erro ao validar username' };
  }
}

// ===== EMAIL VALIDATION =====
// Implementa validação RFC 5322 completa
export const emailSchema = z
  .string()
  .email('Email inválido')
  .min(5, 'Email muito curto')
  .max(254, 'Email muito longo (máximo 254 caracteres)')
  .regex(
    /^(?:[a-z0-9!#$%&'*+/=?^_`{|}~-]+(?:\.[a-z0-9!#$%&'*+/=?^_`{|}~-]+)*|"(?:[\x01-\x08\x0b\x0c\x0e-\x1f\x21\x23-\x5b\x5d-\x7f]|\\[\x01-\x09\x0b\x0c\x0e-\x7f])*")@(?:(?:[a-z0-9](?:[a-z0-9-]*[a-z0-9])?\.)+[a-z0-9](?:[a-z0-9-]*[a-z0-9])?|\[(?:(?:(2(5[0-5]|[0-4][0-9])|1[0-9][0-9]|[1-9]?[0-9]))\.){3}(?:(2(5[0-5]|[0-4][0-9])|1[0-9][0-9]|[1-9]?[0-9])|[a-z0-9-]*[a-z0-9]:(?:[\x01-\x08\x0b\x0c\x0e-\x1f\x21-\x5a\x53-\x7f]|\\[\x01-\x09\x0b\x0c\x0e-\x7f])+)\])$/i,
    'Email não está em formato válido RFC 5322'
  );

export function validateEmail(email: string): { valid: boolean; error?: string } {
  try {
    emailSchema.parse(email.toLowerCase().trim());
    return { valid: true };
  } catch (error) {
    if (error instanceof z.ZodError) {
      return { valid: false, error: error.issues[0].message };
    }
    return { valid: false, error: 'Erro ao validar email' };
  }
}

// ===== PASSWORD VALIDATION =====
// Regras: mínimo 8 caracteres, pelo menos 1 maiúscula, 1 minúscula, 1 número
export const passwordSchema = z
  .string()
  .min(8, 'Senha deve ter pelo menos 8 caracteres')
  .max(128, 'Senha muito longa (máximo 128 caracteres)')
  .regex(/[a-z]/, 'Senha deve conter pelo menos uma letra minúscula')
  .regex(/[A-Z]/, 'Senha deve conter pelo menos uma letra maiúscula')
  .regex(/[0-9]/, 'Senha deve conter pelo menos um número')
  .regex(/^[^\s]+$/, 'Senha não pode conter espaços');

export function validatePassword(password: string): { valid: boolean; error?: string; strength?: string } {
  try {
    passwordSchema.parse(password);
    
    // Calcular força da senha
    let strength = 'média';
    if (password.length >= 12 && /[!@#$%^&*(),.?":{}|<>]/.test(password)) {
      strength = 'forte';
    } else if (password.length >= 10) {
      strength = 'boa';
    }
    
    return { valid: true, strength };
  } catch (error) {
    if (error instanceof z.ZodError) {
      return { valid: false, error: error.issues[0].message };
    }
    return { valid: false, error: 'Erro ao validar senha' };
  }
}

// ===== NAME VALIDATION =====
export const nameSchema = z
  .string()
  .min(2, 'Nome deve ter pelo menos 2 caracteres')
  .max(100, 'Nome muito longo (máximo 100 caracteres)')
  .regex(/^[a-zA-ZÀ-ÿ\s'-]+$/, 'Nome contém caracteres inválidos');

export function validateName(name: string): { valid: boolean; error?: string } {
  try {
    nameSchema.parse(name.trim());
    return { valid: true };
  } catch (error) {
    if (error instanceof z.ZodError) {
      return { valid: false, error: error.issues[0].message };
    }
    return { valid: false, error: 'Erro ao validar nome' };
  }
}

// ===== COMPLETE REGISTRATION SCHEMA =====
export const registrationSchema = z.object({
  name: nameSchema,
  email: emailSchema,
  password: passwordSchema,
  confirmPassword: z.string(),
}).refine((data) => data.password === data.confirmPassword, {
  message: 'As senhas não correspondem',
  path: ['confirmPassword'],
});

// ===== COMPLETE LOGIN SCHEMA =====
export const loginSchema = z.object({
  email: emailSchema,
  password: z.string().min(1, 'Senha é obrigatória'),
});

// ===== SANITIZATION FUNCTIONS =====
// Protege contra XSS removendo caracteres perigosos
export function sanitizeInput(input: string): string {
  return input
    .trim()
    .replace(/[<>]/g, '') // Remove < e >
    .replace(/javascript:/gi, '') // Remove javascript:
    .replace(/on\w+\s*=/gi, ''); // Remove event handlers
}

// Sanitiza email removendo espaços e convertendo para lowercase
export function sanitizeEmail(email: string): string {
  return email.trim().toLowerCase().replace(/\s/g, '');
}

// ===== SQL INJECTION PROTECTION =====
// Valida que a string não contém padrões suspeitos de SQL injection
export function validateSqlInput(input: string): boolean {
  const suspiciousPatterns = [
    /(\b(SELECT|INSERT|UPDATE|DELETE|DROP|CREATE|ALTER|EXEC|EXECUTE)\b)/gi,
    /(--|\*|;|'|"|\\)/,
    /(\bOR\b|\bAND\b).*=.*=/gi,
    /1\s*=\s*1/gi,
    /'\s*OR\s*'1'\s*=\s*'1/gi,
  ];

  return !suspiciousPatterns.some(pattern => pattern.test(input));
}

// ===== RECAPTCHA TOKEN VALIDATION =====
export const recaptchaSchema = z.string().min(1, 'Token de captcha é obrigatório');

export function validateRecaptchaToken(token: string): { valid: boolean; error?: string } {
  try {
    recaptchaSchema.parse(token);
    return { valid: true };
  } catch (error) {
    return { valid: false, error: 'Token de captcha inválido' };
  }
}
