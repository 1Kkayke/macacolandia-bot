"use client";

import { useEffect, useState } from "react";
import { useQuery, useMutation, useQueryClient } from "@tanstack/react-query";
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from "@/components/ui/card";
import { Button } from "@/components/ui/button";
import { Table, TableBody, TableCell, TableHead, TableHeader, TableRow } from "@/components/ui/table";
import { Badge } from "@/components/ui/badge";
import { AuthGuard } from "@/lib/auth-guard";
import { CheckCircle, XCircle, Clock, Mail, User, Globe } from "lucide-react";

interface PendingRegistration {
  id: number;
  name: string;
  email: string;
  ip_address: string | null;
  user_agent: string | null;
  requested_at: string;
  status: string;
}

export default function RegistrationsPage() {
  return (
    <AuthGuard requireAdmin>
      <RegistrationsPageContent />
    </AuthGuard>
  );
}

function RegistrationsPageContent() {
  const queryClient = useQueryClient();

  const { data: registrations, isLoading } = useQuery<PendingRegistration[]>({
    queryKey: ["pending-registrations"],
    queryFn: async () => {
      const res = await fetch("/api/admin/registrations");
      if (!res.ok) throw new Error("Failed to fetch");
      return res.json();
    },
  });

  const handleAction = useMutation({
    mutationFn: async ({ action, id }: { action: string; id: number }) => {
      const res = await fetch("/api/admin/registrations", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ action, id }),
      });
      if (!res.ok) throw new Error("Failed to process action");
      return res.json();
    },
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ["pending-registrations"] });
    },
  });

  const formatDate = (dateStr: string) => {
    return new Date(dateStr).toLocaleString("pt-BR");
  };

  if (isLoading) {
    return <div>Carregando...</div>;
  }

  return (
    <div className="space-y-6">
      <div>
        <h1 className="text-3xl font-bold">Solicitações de Registro</h1>
        <p className="text-muted-foreground mt-2">
          Aprovar ou rejeitar solicitações de acesso ao painel
        </p>
      </div>

      <Card>
        <CardHeader>
          <CardTitle>Solicitações Pendentes</CardTitle>
          <CardDescription>
            {registrations?.length || 0} solicitações aguardando aprovação
          </CardDescription>
        </CardHeader>
        <CardContent>
          {!registrations || registrations.length === 0 ? (
            <div className="text-center py-8 text-muted-foreground">
              Nenhuma solicitação pendente
            </div>
          ) : (
            <Table>
              <TableHeader>
                <TableRow>
                  <TableHead>Usuário</TableHead>
                  <TableHead>Email</TableHead>
                  <TableHead>IP / Navegador</TableHead>
                  <TableHead>Data</TableHead>
                  <TableHead>Ações</TableHead>
                </TableRow>
              </TableHeader>
              <TableBody>
                {registrations.map((reg) => (
                  <TableRow key={reg.id}>
                    <TableCell>
                      <div className="flex items-center gap-2">
                        <User className="h-4 w-4 text-muted-foreground" />
                        <span className="font-medium">{reg.name}</span>
                      </div>
                    </TableCell>
                    <TableCell>
                      <div className="flex items-center gap-2">
                        <Mail className="h-4 w-4 text-muted-foreground" />
                        {reg.email}
                      </div>
                    </TableCell>
                    <TableCell className="text-sm">
                      <div className="space-y-1">
                        {reg.ip_address && (
                          <div className="flex items-center gap-1">
                            <Globe className="h-3 w-3" />
                            <span className="text-muted-foreground">{reg.ip_address}</span>
                          </div>
                        )}
                        {reg.user_agent && (
                          <div className="text-xs text-muted-foreground truncate max-w-xs">
                            {reg.user_agent}
                          </div>
                        )}
                      </div>
                    </TableCell>
                    <TableCell className="text-sm">
                      <div className="flex items-center gap-1">
                        <Clock className="h-3 w-3" />
                        {formatDate(reg.requested_at)}
                      </div>
                    </TableCell>
                    <TableCell>
                      <div className="flex gap-2">
                        <Button
                          size="sm"
                          onClick={() =>
                            handleAction.mutate({ action: "approve", id: reg.id })
                          }
                          disabled={handleAction.isPending}
                        >
                          <CheckCircle className="h-4 w-4 mr-1" />
                          Aprovar
                        </Button>
                        <Button
                          size="sm"
                          variant="destructive"
                          onClick={() =>
                            handleAction.mutate({ action: "reject", id: reg.id })
                          }
                          disabled={handleAction.isPending}
                        >
                          <XCircle className="h-4 w-4 mr-1" />
                          Rejeitar
                        </Button>
                      </div>
                    </TableCell>
                  </TableRow>
                ))}
              </TableBody>
            </Table>
          )}
        </CardContent>
      </Card>
    </div>
  );
}
