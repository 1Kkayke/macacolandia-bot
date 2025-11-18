"use client";

import { useState } from "react";
import { useQuery } from "@tanstack/react-query";
import { Tabs, TabsContent, TabsList, TabsTrigger } from "@/components/ui/tabs";
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from "@/components/ui/card";
import { UserManagement } from "@/components/user-management";
import { StatsDashboard } from "@/components/stats-dashboard";
import { NavBar } from "@/components/nav-bar";
import { AuthGuard } from "@/lib/auth-guard";
import { Bot, Server } from "lucide-react";

interface ServerConfig {
  guild_id: string;
  guild_name: string;
  user_count: number;
}

export default function Home() {
  return (
    <AuthGuard>
      <HomePage />
    </AuthGuard>
  );
}

function HomePage() {
  const [selectedServer, setSelectedServer] = useState<string>("server_1");

  const { data: servers, isLoading } = useQuery<ServerConfig[]>({
    queryKey: ["servers"],
    queryFn: async () => {
      const res = await fetch("/api/servers");
      if (!res.ok) throw new Error("Failed to fetch servers");
      return res.json();
    },
  });

  if (isLoading) {
    return (
      <div className="flex min-h-screen items-center justify-center">
        <div className="text-center">
          <Bot className="mx-auto h-12 w-12 animate-pulse text-primary" />
          <p className="mt-4 text-muted-foreground">Carregando...</p>
        </div>
      </div>
    );
  }

  return (
    <div className="min-h-screen bg-gradient-to-br from-background to-muted/20">
      <NavBar />

      <main className="container mx-auto px-4 py-8">
        <Card className="mb-6">
          <CardHeader>
            <CardTitle className="flex items-center gap-2">
              <Server className="h-5 w-5" />
              Servidores
            </CardTitle>
            <CardDescription>
              Selecione um servidor para gerenciar usuários e visualizar estatísticas
            </CardDescription>
          </CardHeader>
          <CardContent>
            <Tabs value={selectedServer} onValueChange={setSelectedServer}>
              <TabsList className="grid w-full grid-cols-2">
                {servers?.map((server) => (
                  <TabsTrigger key={server.guild_id} value={server.guild_id}>
                    <div className="flex flex-col items-start">
                      <span className="font-semibold">{server.guild_name}</span>
                      <span className="text-xs text-muted-foreground">
                        {server.user_count} usuários
                      </span>
                    </div>
                  </TabsTrigger>
                ))}
              </TabsList>

              {servers?.map((server) => (
                <TabsContent key={server.guild_id} value={server.guild_id} className="mt-6 space-y-6">
                  <div className="space-y-6">
                    <section>
                      <h2 className="mb-4 text-2xl font-bold">Estatísticas</h2>
                      <StatsDashboard serverId={server.guild_id} />
                    </section>

                    <section>
                      <h2 className="mb-4 text-2xl font-bold">Gerenciamento de Usuários</h2>
                      <UserManagement serverId={server.guild_id} />
                    </section>
                  </div>
                </TabsContent>
              ))}
            </Tabs>
          </CardContent>
        </Card>
      </main>

      <footer className="border-t bg-card/50 py-6 backdrop-blur">
        <div className="container mx-auto px-4 text-center text-sm text-muted-foreground">
          <p>
            © 2024 Macacolândia Bot • Desenvolvido com Next.js, Tailwind CSS e React Query
          </p>
        </div>
      </footer>
    </div>
  );
}
