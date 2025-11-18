import { NextResponse } from 'next/server';
import { auth } from '@/lib/auth';
import {
  getAllAuthUsers,
  updateUserApproval,
  updateUserBlocked,
  updateUserRole,
  deleteAuthUser,
  logActivity,
} from '@/lib/auth-db';

export async function GET() {
  try {
    const session = await auth();

    if (!session || (session.user as any).role !== 'admin') {
      return NextResponse.json({ error: 'Não autorizado' }, { status: 401 });
    }

    const users = getAllAuthUsers();
    // Remove password from response
    const sanitizedUsers = users.map(({ password, ...user }) => user);
    
    return NextResponse.json(sanitizedUsers);
  } catch (error) {
    console.error('Error fetching users:', error);
    return NextResponse.json(
      { error: 'Erro ao buscar usuários' },
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
    const { action, userId, value } = body;

    if (!action || !userId) {
      return NextResponse.json(
        { error: 'Ação e userId são obrigatórios' },
        { status: 400 }
      );
    }

    let success = false;
    let actionDescription = '';

    switch (action) {
      case 'approve':
        success = updateUserApproval(userId, true);
        actionDescription = `Usuário #${userId} aprovado`;
        break;
      case 'unapprove':
        success = updateUserApproval(userId, false);
        actionDescription = `Aprovação do usuário #${userId} removida`;
        break;
      case 'block':
        success = updateUserBlocked(userId, true);
        actionDescription = `Usuário #${userId} bloqueado`;
        break;
      case 'unblock':
        success = updateUserBlocked(userId, false);
        actionDescription = `Usuário #${userId} desbloqueado`;
        break;
      case 'setRole':
        if (!value || !['admin', 'user'].includes(value)) {
          return NextResponse.json(
            { error: 'Role inválido' },
            { status: 400 }
          );
        }
        success = updateUserRole(userId, value);
        actionDescription = `Role do usuário #${userId} alterado para ${value}`;
        break;
      case 'delete':
        success = deleteAuthUser(userId);
        actionDescription = `Usuário #${userId} removido`;
        break;
      default:
        return NextResponse.json(
          { error: 'Ação inválida' },
          { status: 400 }
        );
    }

    if (success) {
      // Log the activity
      const ipAddress = request.headers.get('x-forwarded-for') || 
                        request.headers.get('x-real-ip') || 
                        null;
      logActivity(
        parseInt((session.user as any).id),
        action,
        actionDescription,
        ipAddress
      );

      return NextResponse.json({
        success: true,
        message: 'Ação executada com sucesso',
      });
    }

    return NextResponse.json(
      { error: 'Falha ao executar ação' },
      { status: 400 }
    );
  } catch (error) {
    console.error('Error processing user action:', error);
    return NextResponse.json(
      { error: 'Erro ao processar ação' },
      { status: 500 }
    );
  }
}
