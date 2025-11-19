"use client";

import { useEffect, useRef } from 'react';

declare global {
  interface Window {
    grecaptcha: any;
    onRecaptchaLoad: () => void;
  }
}

interface RecaptchaProps {
  onVerify: (token: string) => void;
  onExpire?: () => void;
  onError?: () => void;
  size?: 'normal' | 'compact' | 'invisible';
  theme?: 'light' | 'dark';
}

export function Recaptcha({
  onVerify,
  onExpire,
  onError,
  size = 'normal',
  theme = 'light',
}: RecaptchaProps) {
  const containerRef = useRef<HTMLDivElement>(null);
  const widgetIdRef = useRef<number | null>(null);

  useEffect(() => {
    const siteKey = process.env.NEXT_PUBLIC_RECAPTCHA_SITE_KEY;

    if (!siteKey) {
      console.warn('[RECAPTCHA] NEXT_PUBLIC_RECAPTCHA_SITE_KEY não configurada');
      // Em desenvolvimento, permitir sem captcha
      if (process.env.NODE_ENV === 'development') {
        onVerify('dev-bypass-token');
      }
      return;
    }

    const loadRecaptcha = () => {
      if (window.grecaptcha && containerRef.current && widgetIdRef.current === null) {
        try {
          widgetIdRef.current = window.grecaptcha.render(containerRef.current, {
            sitekey: siteKey,
            callback: onVerify,
            'expired-callback': onExpire,
            'error-callback': onError,
            size,
            theme,
          });
        } catch (error) {
          console.error('[RECAPTCHA] Erro ao renderizar:', error);
        }
      }
    };

    // Se grecaptcha já está carregado
    if (window.grecaptcha) {
      loadRecaptcha();
    } else {
      // Adicionar script se não existe
      const existingScript = document.getElementById('recaptcha-script');
      
      if (!existingScript) {
        const script = document.createElement('script');
        script.id = 'recaptcha-script';
        script.src = 'https://www.google.com/recaptcha/api.js?onload=onRecaptchaLoad&render=explicit';
        script.async = true;
        script.defer = true;
        
        window.onRecaptchaLoad = loadRecaptcha;
        
        document.head.appendChild(script);
      } else {
        window.onRecaptchaLoad = loadRecaptcha;
      }
    }

    return () => {
      if (widgetIdRef.current !== null && window.grecaptcha) {
        try {
          window.grecaptcha.reset(widgetIdRef.current);
        } catch (error) {
          // Ignorar erros de cleanup
        }
      }
    };
  }, [onVerify, onExpire, onError, size, theme]);

  // Se não está configurado em desenvolvimento, não renderizar
  if (
    !process.env.NEXT_PUBLIC_RECAPTCHA_SITE_KEY &&
    process.env.NODE_ENV === 'development'
  ) {
    return (
      <div className="p-3 bg-yellow-50 border border-yellow-200 rounded text-xs text-yellow-800">
        ⚠️ ReCAPTCHA não configurado (modo desenvolvimento)
      </div>
    );
  }

  return <div ref={containerRef} className="flex justify-center my-4" />;
}

export function resetRecaptcha(widgetId?: number) {
  if (window.grecaptcha) {
    try {
      if (widgetId !== undefined) {
        window.grecaptcha.reset(widgetId);
      } else {
        window.grecaptcha.reset();
      }
    } catch (error) {
      console.error('[RECAPTCHA] Erro ao resetar:', error);
    }
  }
}
