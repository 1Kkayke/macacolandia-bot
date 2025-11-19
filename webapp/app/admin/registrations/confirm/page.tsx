import React from "react";
import { auth } from "@/lib/auth";
import { approvePendingRegistration, rejectPendingRegistration } from "@/lib/auth-db";
import { sendApprovalNotification } from "@/lib/email";

interface Props {
  searchParams: { [key: string]: string | string[] | undefined };
}

export default async function ConfirmPage({ searchParams }: Props) {
  try {
    const session = await auth();

    if (!session || (session.user as any).role !== "admin") {
      return (
        <div style={{ padding: 24 }}>
          <h1>Não autorizado</h1>
          <p>Você precisa estar logado como administrador para executar essa ação.</p>
        </div>
      );
    }

    const actionParam = Array.isArray(searchParams.action) ? searchParams.action[0] : searchParams.action;
    const idParam = Array.isArray(searchParams.id) ? searchParams.id[0] : searchParams.id;

    if (!actionParam || !idParam) {
      return (
        <div style={{ padding: 24 }}>
          <h1>Link inválido</h1>
          <p>Parâmetros ausentes na URL.</p>
        </div>
      );
    }

    const id = parseInt(idParam, 10);
    if (isNaN(id)) {
      return (
        <div style={{ padding: 24 }}>
          <h1>ID inválido</h1>
          <p>O ID fornecido não é válido.</p>
        </div>
      );
    }

    if (actionParam === "approve") {
      const user = approvePendingRegistration(id);
      if (user) {
        // enviar email de aprovação (não bloqueante)
        try {
          await sendApprovalNotification(user.email, user.name);
        } catch (e) {
          console.error("Falha ao enviar email de aprovação:", e);
        }

        return (
          <div style={{ padding: 24 }}>
            <h1>Registro aprovado com sucesso</h1>
            <p>O usuário <strong>{user.email}</strong> foi aprovado.</p>
          </div>
        );
      }

      return (
        <div style={{ padding: 24 }}>
          <h1>Falha ao aprovar</h1>
          <p>Não foi possível aprovar a solicitação. Verifique se o registro ainda está pendente.</p>
        </div>
      );
    } else if (actionParam === "reject") {
      const success = rejectPendingRegistration(id);
      if (success) {
        return (
          <div style={{ padding: 24 }}>
            <h1>Registro rejeitado</h1>
            <p>A solicitação foi rejeitada com sucesso.</p>
          </div>
        );
      }

      return (
        <div style={{ padding: 24 }}>
          <h1>Falha ao rejeitar</h1>
          <p>Não foi possível rejeitar a solicitação. Verifique se o registro ainda está pendente.</p>
        </div>
      );
    }

    return (
      <div style={{ padding: 24 }}>
        <h1>Ação desconhecida</h1>
        <p>A ação informada não é suportada.</p>
      </div>
    );
  } catch (error) {
    console.error("Erro na confirmação de registro:", error);
    return (
      <div style={{ padding: 24 }}>
        <h1>Erro</h1>
        <p>Ocorreu um erro ao processar a solicitação.</p>
      </div>
    );
  }
}
