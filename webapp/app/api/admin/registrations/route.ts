import { NextResponse } from 'next/server';
import { auth } from '@/lib/auth';
import {
  getPendingRegistrations,
  approvePendingRegistration,
  rejectPendingRegistration,
  getUserByEmail,
} from '@/lib/auth-db';
import { sendApprovalNotification } from '@/lib/email';

export async function GET() {
  try {
    const session = await auth();

    if (!session || (session.user as any).role !== 'admin') {
      return NextResponse.json({ error: 'Não autorizado' }, { status: 401 });
    }

    const registrations = getPendingRegistrations();
    return NextResponse.json(registrations);
  } catch (error) {
    console.error('Error fetching registrations:', error);
    return NextResponse.json(
      { error: 'Erro ao buscar solicitações' },
      { status: 500 }
    );
  }
}

export async function POST(request: Request) {
  try {
    const session = await auth();

    if (!session || (session.user as any).role !== 'admin') {
      return NextResponse.json({ error: 'Não autorizado' }, { status: 401 });
    }

    const body = await request.json();
    const { action, id } = body;

    if (!action || !id) {
      return NextResponse.json(
        { error: 'Ação e ID são obrigatórios' },
        { status: 400 }
      );
    }

    if (action === 'approve') {
      const success = approvePendingRegistration(id);
      
      if (success) {
        // Get the user to send approval email
        const pending = getPendingRegistrations().find(r => r.id === id);
        if (pending) {
          await sendApprovalNotification(pending.email, pending.name);
        }
        
        return NextResponse.json({
          success: true,
          message: 'Registro aprovado com sucesso',
        });
      }
    } else if (action === 'reject') {
      const success = rejectPendingRegistration(id);
      
      if (success) {
        return NextResponse.json({
          success: true,
          message: 'Registro rejeitado',
        });
      }
    }

    return NextResponse.json(
      { error: 'Falha ao processar ação' },
      { status: 400 }
    );
  } catch (error) {
    console.error('Error processing registration action:', error);
    return NextResponse.json(
      { error: 'Erro ao processar ação' },
      { status: 500 }
    );
  }
}
