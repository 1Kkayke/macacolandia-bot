import nodemailer from 'nodemailer';

interface EmailConfig {
  host: string;
  port: number;
  secure: boolean;
  auth: {
    user: string;
    pass: string;
  };
}

function getEmailConfig(): EmailConfig {
  return {
    host: process.env.EMAIL_HOST || 'smtp.gmail.com',
    port: parseInt(process.env.EMAIL_PORT || '587'),
    secure: process.env.EMAIL_SECURE === 'true',
    auth: {
      user: process.env.EMAIL_USER || '',
      pass: process.env.EMAIL_PASS || '',
    },
  };
}

export async function sendRegistrationNotification(data: {
  name: string;
  email: string;
  ipAddress: string | null;
  userAgent: string | null;
  requestedAt: string;
  registrationId: number;
}) {
  const config = getEmailConfig();
  const adminEmail = process.env.ADMIN_EMAIL;

  if (!adminEmail) {
    console.error('ADMIN_EMAIL not configured');
    return false;
  }

  if (!config.auth.user || !config.auth.pass) {
    console.error('Email credentials not configured');
    return false;
  }

  const transporter = nodemailer.createTransport(config);

  const appUrl = process.env.NEXTAUTH_URL || 'http://localhost:3000';
  // Link para confirmação direta — leva a uma página que executa a ação e mostra confirmação
  const approveUrl = `${appUrl}/admin/registrations/confirm?action=approve&id=${data.registrationId}`;
  const rejectUrl = `${appUrl}/admin/registrations/confirm?action=reject&id=${data.registrationId}`;

  const htmlContent = `
<!DOCTYPE html>
<html>
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <style>
    body {
      font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, 'Helvetica Neue', Arial, sans-serif;
      line-height: 1.6;
      color: #333;
      max-width: 600px;
      margin: 0 auto;
      padding: 20px;
      background-color: #f4f4f4;
    }
    .container {
      background-color: #ffffff;
      border-radius: 8px;
      padding: 30px;
      box-shadow: 0 2px 4px rgba(0,0,0,0.1);
    }
    .header {
      text-align: center;
      padding-bottom: 20px;
      border-bottom: 3px solid #4CAF50;
      margin-bottom: 30px;
    }
    .header h1 {
      color: #2c3e50;
      margin: 0;
      font-size: 24px;
    }
    .content {
      margin-bottom: 30px;
    }
    .info-table {
      width: 100%;
      border-collapse: collapse;
      margin: 20px 0;
    }
    .info-table td {
      padding: 12px;
      border-bottom: 1px solid #eee;
    }
    .info-table td:first-child {
      font-weight: bold;
      color: #555;
      width: 140px;
    }
    .actions {
      text-align: center;
      margin-top: 30px;
      padding-top: 20px;
      border-top: 2px solid #eee;
    }
    .button {
      display: inline-block;
      padding: 12px 30px;
      margin: 0 10px;
      text-decoration: none;
      border-radius: 5px;
      font-weight: bold;
      font-size: 16px;
      transition: all 0.3s;
    }
    .approve {
      background-color: #4CAF50;
      color: white;
    }
    .approve:hover {
      background-color: #45a049;
    }
    .reject {
      background-color: #f44336;
      color: white;
    }
    .reject:hover {
      background-color: #da190b;
    }
    .footer {
      text-align: center;
      margin-top: 30px;
      padding-top: 20px;
      border-top: 1px solid #eee;
      color: #777;
      font-size: 14px;
    }
    .alert {
      background-color: #fff3cd;
      border-left: 4px solid #ffc107;
      padding: 15px;
      margin: 20px 0;
      border-radius: 4px;
    }
  </style>
</head>
<body>
  <div class="container">
    <div class="header">
      <h1>🔔 Nova Solicitação de Registro</h1>
      <p style="color: #666; margin: 10px 0 0 0;">Macacolândia Bot Admin Panel</p>
    </div>

    <div class="content">
      <p>Um novo usuário solicitou acesso ao painel administrativo do bot:</p>

      <table class="info-table">
        <tr>
          <td>👤 Nome:</td>
          <td><strong>${data.name}</strong></td>
        </tr>
        <tr>
          <td>📧 Email:</td>
          <td><strong>${data.email}</strong></td>
        </tr>
        <tr>
          <td>🌐 Endereço IP:</td>
          <td>${data.ipAddress || 'Não disponível'}</td>
        </tr>
        <tr>
          <td>💻 Navegador:</td>
          <td style="font-size: 12px;">${data.userAgent || 'Não disponível'}</td>
        </tr>
        <tr>
          <td>📅 Data/Hora:</td>
          <td>${new Date(data.requestedAt).toLocaleString('pt-BR', { 
            timeZone: 'America/Sao_Paulo',
            dateStyle: 'full',
            timeStyle: 'long'
          })}</td>
        </tr>
        <tr>
          <td>🆔 ID Registro:</td>
          <td>#${data.registrationId}</td>
        </tr>
      </table>

      <div class="alert">
        ⚠️ <strong>Atenção:</strong> Verifique cuidadosamente os dados antes de aprovar o acesso. O usuário só poderá fazer login após sua aprovação.
      </div>
    </div>

    <div class="actions">
      <p style="margin-bottom: 20px; color: #666;">Escolha uma ação:</p>
      <a href="${approveUrl}" class="button approve">✅ Aprovar Acesso</a>
      <a href="${rejectUrl}" class="button reject">❌ Rejeitar Solicitação</a>
    </div>

    <div class="footer">
      <p>Este é um email automático do sistema Macacolândia Bot.</p>
      <p>Você também pode gerenciar solicitações diretamente no painel admin.</p>
    </div>
  </div>
</body>
</html>
  `;

  try {
    await transporter.sendMail({
      from: `"Macacolândia Bot" <${config.auth.user}>`,
      to: adminEmail,
      subject: `🔔 Nova Solicitação de Registro - ${data.name}`,
      html: htmlContent,
    });
    return true;
  } catch (error) {
    console.error('Error sending email:', error);
    return false;
  }
}

export async function sendApprovalNotification(email: string, name: string) {
  const config = getEmailConfig();

  if (!config.auth.user || !config.auth.pass) {
    console.error('Email credentials not configured');
    return false;
  }

  const transporter = nodemailer.createTransport(config);
  const loginUrl = process.env.NEXTAUTH_URL || 'http://localhost:3000';

  const htmlContent = `
<!DOCTYPE html>
<html>
<head>
  <meta charset="UTF-8">
  <style>
    body {
      font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
      line-height: 1.6;
      color: #333;
      max-width: 600px;
      margin: 0 auto;
      padding: 20px;
      background-color: #f4f4f4;
    }
    .container {
      background-color: #ffffff;
      border-radius: 8px;
      padding: 30px;
      box-shadow: 0 2px 4px rgba(0,0,0,0.1);
    }
    .header {
      text-align: center;
      padding-bottom: 20px;
      border-bottom: 3px solid #4CAF50;
      margin-bottom: 30px;
    }
    .success-icon {
      font-size: 48px;
      margin-bottom: 10px;
    }
    .button {
      display: inline-block;
      padding: 15px 40px;
      background-color: #4CAF50;
      color: white;
      text-decoration: none;
      border-radius: 5px;
      font-weight: bold;
      margin-top: 20px;
    }
    .footer {
      text-align: center;
      margin-top: 30px;
      padding-top: 20px;
      border-top: 1px solid #eee;
      color: #777;
      font-size: 14px;
    }
  </style>
</head>
<body>
  <div class="container">
    <div class="header">
      <div class="success-icon">✅</div>
      <h1 style="color: #2c3e50; margin: 0;">Acesso Aprovado!</h1>
    </div>

    <div class="content">
      <p>Olá <strong>${name}</strong>,</p>
      <p>Sua solicitação de acesso ao painel administrativo do <strong>Macacolândia Bot</strong> foi aprovada!</p>
      <p>Agora você pode fazer login e começar a gerenciar o bot.</p>
      
      <div style="text-align: center;">
        <a href="${loginUrl}" class="button">Acessar Painel</a>
      </div>
    </div>

    <div class="footer">
      <p>Bem-vindo à equipe Macacolândia!</p>
    </div>
  </div>
</body>
</html>
  `;

  try {
    await transporter.sendMail({
      from: `"Macacolândia Bot" <${config.auth.user}>`,
      to: email,
      subject: '✅ Seu acesso foi aprovado - Macacolândia Bot',
      html: htmlContent,
    });
    return true;
  } catch (error) {
    console.error('Error sending approval email:', error);
    return false;
  }
}
