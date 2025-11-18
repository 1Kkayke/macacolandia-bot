"use client";

import { useQuery } from "@tanstack/react-query";
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from "@/components/ui/card";
import { Table, TableBody, TableCell, TableHead, TableHeader, TableRow } from "@/components/ui/table";
import { Badge } from "@/components/ui/badge";
import { AuthGuard } from "@/lib/auth-guard";
import { Clock, User, Activity } from "lucide-react";

interface ActivityLog {
  id: number;
  user_id: number | null;
  user_name: string | null;
  user_email: string | null;
  action: string;
  details: string | null;
  ip_address: string | null;
  timestamp: string;
}

export default function LogsPage() {
  return (
    <AuthGuard requireAdmin>
      <LogsPageContent />
    </AuthGuard>
  );
}

function LogsPageContent() {
  const { data: logs, isLoading } = useQuery<ActivityLog[]>({
    queryKey: ["activity-logs"],
    queryFn: async () => {
      const res = await fetch("/api/admin/logs?limit=100");
      if (!res.ok) throw new Error("Failed to fetch");
      return res.json();
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
        <h1 className="text-3xl font-bold">Logs de Atividade</h1>
        <p className="text-muted-foreground mt-2">
          Visualizar todas as ações realizadas no sistema
        </p>
      </div>

      <Card>
        <CardHeader>
          <CardTitle>Atividades Recentes</CardTitle>
          <CardDescription>
            Últimas {logs?.length || 0} atividades registradas
          </CardDescription>
        </CardHeader>
        <CardContent>
          {!logs || logs.length === 0 ? (
            <div className="text-center py-8 text-muted-foreground">
              Nenhuma atividade registrada
            </div>
          ) : (
            <Table>
              <TableHeader>
                <TableRow>
                  <TableHead>Data/Hora</TableHead>
                  <TableHead>Usuário</TableHead>
                  <TableHead>Ação</TableHead>
                  <TableHead>Detalhes</TableHead>
                  <TableHead>IP</TableHead>
                </TableRow>
              </TableHeader>
              <TableBody>
                {logs.map((log) => (
                  <TableRow key={log.id}>
                    <TableCell className="text-sm">
                      <div className="flex items-center gap-1">
                        <Clock className="h-3 w-3 text-muted-foreground" />
                        {formatDate(log.timestamp)}
                      </div>
                    </TableCell>
                    <TableCell>
                      {log.user_name ? (
                        <div>
                          <div className="font-medium flex items-center gap-1">
                            <User className="h-3 w-3" />
                            {log.user_name}
                          </div>
                          <div className="text-xs text-muted-foreground">
                            {log.user_email}
                          </div>
                        </div>
                      ) : (
                        <span className="text-muted-foreground">Sistema</span>
                      )}
                    </TableCell>
                    <TableCell>
                      <Badge variant="outline">
                        <Activity className="h-3 w-3 mr-1" />
                        {log.action}
                      </Badge>
                    </TableCell>
                    <TableCell className="text-sm text-muted-foreground">
                      {log.details || "-"}
                    </TableCell>
                    <TableCell className="text-sm text-muted-foreground">
                      {log.ip_address || "-"}
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
