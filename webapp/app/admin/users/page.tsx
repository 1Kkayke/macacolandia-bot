"use client";

import { useQuery, useMutation, useQueryClient } from "@tanstack/react-query";
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from "@/components/ui/card";
import { Button } from "@/components/ui/button";
import { Table, TableBody, TableCell, TableHead, TableHeader, TableRow } from "@/components/ui/table";
import { Badge } from "@/components/ui/badge";
import { AuthGuard } from "@/lib/auth-guard";
import { Shield, Lock, Unlock, Trash2, CheckCircle, XCircle } from "lucide-react";

interface AuthUser {
  id: number;
  name: string;
  email: string;
  role: string;
  approved: boolean;
  blocked: boolean;
  created_at: string;
}

export default function UsersPage() {
  return (
    <AuthGuard requireAdmin>
      <UsersPageContent />
    </AuthGuard>
  );
}

function UsersPageContent() {
  const queryClient = useQueryClient();

  const { data: users, isLoading } = useQuery<AuthUser[]>({
    queryKey: ["auth-users"],
    queryFn: async () => {
      const res = await fetch("/api/admin/users");
      if (!res.ok) throw new Error("Failed to fetch");
      return res.json();
    },
  });

  const handleAction = useMutation({
    mutationFn: async ({ action, userId, value }: { action: string; userId: number; value?: string }) => {
      const res = await fetch("/api/admin/users", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ action, userId, value }),
      });
      if (!res.ok) throw new Error("Failed to process action");
      return res.json();
    },
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ["auth-users"] });
    },
  });

  const formatDate = (dateStr: string) => {
    return new Date(dateStr).toLocaleDateString("pt-BR");
  };

  if (isLoading) {
    return <div>Carregando...</div>;
  }

  return (
    <div className="space-y-6">
      <div>
        <h1 className="text-3xl font-bold">Gerenciar Usuários</h1>
        <p className="text-muted-foreground mt-2">
          Gerenciar permissões e acesso de todos os usuários
        </p>
      </div>

      <Card>
        <CardHeader>
          <CardTitle>Usuários do Sistema</CardTitle>
          <CardDescription>
            {users?.length || 0} usuários cadastrados
          </CardDescription>
        </CardHeader>
        <CardContent>
          {!users || users.length === 0 ? (
            <div className="text-center py-8 text-muted-foreground">
              Nenhum usuário cadastrado
            </div>
          ) : (
            <Table>
              <TableHeader>
                <TableRow>
                  <TableHead>Usuário</TableHead>
                  <TableHead>Email</TableHead>
                  <TableHead>Role</TableHead>
                  <TableHead>Status</TableHead>
                  <TableHead>Cadastro</TableHead>
                  <TableHead>Ações</TableHead>
                </TableRow>
              </TableHeader>
              <TableBody>
                {users.map((user) => (
                  <TableRow key={user.id}>
                    <TableCell className="font-medium">{user.name}</TableCell>
                    <TableCell>{user.email}</TableCell>
                    <TableCell>
                      <Badge variant={user.role === "admin" ? "default" : "secondary"}>
                        {user.role === "admin" && <Shield className="h-3 w-3 mr-1" />}
                        {user.role}
                      </Badge>
                    </TableCell>
                    <TableCell>
                      <div className="flex gap-2">
                        {user.approved ? (
                          <Badge variant="default">
                            <CheckCircle className="h-3 w-3 mr-1" />
                            Aprovado
                          </Badge>
                        ) : (
                          <Badge variant="secondary">Pendente</Badge>
                        )}
                        {user.blocked && (
                          <Badge variant="destructive">
                            <Lock className="h-3 w-3 mr-1" />
                            Bloqueado
                          </Badge>
                        )}
                      </div>
                    </TableCell>
                    <TableCell className="text-sm text-muted-foreground">
                      {formatDate(user.created_at)}
                    </TableCell>
                    <TableCell>
                      <div className="flex flex-wrap gap-2">
                        {!user.approved && (
                          <Button
                            size="sm"
                            variant="outline"
                            onClick={() =>
                              handleAction.mutate({ action: "approve", userId: user.id })
                            }
                          >
                            <CheckCircle className="h-4 w-4 mr-1" />
                            Aprovar
                          </Button>
                        )}
                        
                        {user.blocked ? (
                          <Button
                            size="sm"
                            variant="outline"
                            onClick={() =>
                              handleAction.mutate({ action: "unblock", userId: user.id })
                            }
                          >
                            <Unlock className="h-4 w-4 mr-1" />
                            Desbloquear
                          </Button>
                        ) : (
                          <Button
                            size="sm"
                            variant="outline"
                            onClick={() =>
                              handleAction.mutate({ action: "block", userId: user.id })
                            }
                          >
                            <Lock className="h-4 w-4 mr-1" />
                            Bloquear
                          </Button>
                        )}

                        {user.role === "user" && (
                          <Button
                            size="sm"
                            variant="outline"
                            onClick={() =>
                              handleAction.mutate({
                                action: "setRole",
                                userId: user.id,
                                value: "admin",
                              })
                            }
                          >
                            <Shield className="h-4 w-4 mr-1" />
                            Admin
                          </Button>
                        )}

                        <Button
                          size="sm"
                          variant="destructive"
                          onClick={() =>
                            handleAction.mutate({ action: "delete", userId: user.id })
                          }
                        >
                          <Trash2 className="h-4 w-4 mr-1" />
                          Remover
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
