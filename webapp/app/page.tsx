"use client";

import { useState, useEffect } from "react";
import { useQuery } from "@tanstack/react-query";
import { Tabs, TabsContent, TabsList, TabsTrigger } from "@/components/ui/tabs";
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from "@/components/ui/card";
import { UserManagement } from "@/components/user-management";
import { StatsDashboard } from "@/components/stats-dashboard";
import { NavBar } from "@/components/nav-bar";
import { AuthGuard } from "@/lib/auth-guard";
import { Bot, Server, Users, Activity } from "lucide-react";

interface ServerConfig {
  id: string;
  name: string;
  icon: string | null;
  member_count: number;
}

export default function Home() {
  return (
    <AuthGuard>
      <HomePage />
    </AuthGuard>
  );
}

function HomePage() {
  const [selectedServer, setSelectedServer] = useState<string>("");

  const { data: servers, isLoading } = useQuery<ServerConfig[]>({
    queryKey: ["servers"],
    queryFn: async () => {
      const res = await fetch("/api/servers");
      if (!res.ok) throw new Error("Failed to fetch servers");
      return res.json();
    },
  });

  // Set default selected server when data loads
  useEffect(() => {
    if (servers && servers.length > 0 && !selectedServer) {
      setSelectedServer(servers[0].id);
    }
  }, [servers, selectedServer]);

  if (isLoading) {
    return (
      <div className="flex min-h-screen items-center justify-center">
        <div className="text-center animate-bounce-in">
          <div className="relative mx-auto h-32 w-32 mb-8">
            <div className="absolute inset-0 rounded-full bg-gradient-to-r from-primary via-accent to-secondary animate-pulse-glow blur-2xl"></div>
            <Bot className="relative h-32 w-32 animate-float text-primary drop-shadow-[0_0_30px_rgba(168,85,247,0.8)] animate-glow" />
          </div>
          <p className="mt-6 text-xl font-bold text-gradient animate-shimmer">Carregando dashboard...</p>
          <div className="mt-4 flex justify-center gap-2">
            <div className="h-2 w-2 bg-primary rounded-full animate-bounce" style={{ animationDelay: "0s" }}></div>
            <div className="h-2 w-2 bg-accent rounded-full animate-bounce" style={{ animationDelay: "0.2s" }}></div>
            <div className="h-2 w-2 bg-secondary rounded-full animate-bounce" style={{ animationDelay: "0.4s" }}></div>
          </div>
        </div>
      </div>
    );
  }

  return (
    <div className="min-h-screen flex flex-col">
      <NavBar />

      <main className="container mx-auto px-4 py-8 flex-1">
        <div className="mb-8 flex flex-col md:flex-row md:items-center justify-between gap-4 animate-slide-in-up">
          <div>
            <h1 className="text-5xl font-bold tracking-tight text-gradient drop-shadow-lg animate-shimmer">
              Dashboard
            </h1>
            <p className="text-muted-foreground mt-3 text-lg font-medium animate-slide-in-right" style={{ animationDelay: "0.2s" }}>
              Gerencie seus servidores e visualize estatísticas em tempo real
            </p>
          </div>
          <div className="flex items-center gap-3 px-5 py-3 rounded-full bg-gradient-to-r from-primary/20 to-accent/20 border border-primary/30 text-primary text-sm font-bold shadow-lg shadow-primary/20 animate-scale-in backdrop-blur-xl" style={{ animationDelay: "0.3s" }}>
            <div className="h-3 w-3 rounded-full bg-gradient-to-r from-green-400 to-emerald-500 animate-pulse-glow shadow-[0_0_10px_rgba(34,197,94,0.5)]"></div>
            Sistema Online
          </div>
        </div>

        <Card className="mb-8 border-primary/20 bg-card/40 backdrop-blur-xl shadow-2xl overflow-hidden glass-card animate-scale-in" style={{ animationDelay: "0.4s" }}>
          <div className="absolute top-0 left-0 w-full h-1 bg-gradient-to-r from-transparent via-primary to-accent to-transparent animate-shimmer"></div>
          <CardHeader className="pb-2">
            <CardTitle className="flex items-center gap-3 text-2xl">
              <div className="p-3 rounded-xl bg-gradient-to-br from-primary/20 to-accent/20 text-primary shadow-[0_0_20px_rgba(168,85,247,0.4)] border border-primary/30 backdrop-blur-sm animate-pulse-glow">
                <Server className="h-6 w-6 animate-float" />
              </div>
              <span className="text-gradient">Servidores Ativos</span>
            </CardTitle>
            <CardDescription className="text-base">
              Selecione um servidor para gerenciar usuários e visualizar estatísticas
            </CardDescription>
          </CardHeader>
          <CardContent className="pt-6">
            {servers && servers.length > 0 ? (
              <Tabs value={selectedServer} onValueChange={setSelectedServer} className="w-full">
                <TabsList className="w-full justify-start h-auto p-1 bg-muted/30 backdrop-blur mb-8 overflow-x-auto flex-nowrap custom-scrollbar">
                  {servers.map((server, index) => (
                    <TabsTrigger 
                      key={server.id} 
                      value={server.id}
                      className="flex-1 min-w-[200px] data-[state=active]:bg-gradient-to-r data-[state=active]:from-primary/20 data-[state=active]:to-accent/20 data-[state=active]:text-primary data-[state=active]:shadow-lg data-[state=active]:shadow-primary/20 border border-transparent data-[state=active]:border-primary/40 transition-all duration-500 hover:bg-white/5 hover:border-primary/20 hover:shadow-md animate-slide-in-up"
                      style={{ animationDelay: `${0.1 * index}s` }}
                    >
                      <div className="flex flex-col items-start py-3 px-2 w-full">
                        <span className="font-bold text-base truncate w-full text-left flex items-center gap-2">
                          {server.icon ? (
                            <img src={server.icon} alt="" className="w-6 h-6 rounded-full border-2 border-primary/30 shadow-lg" />
                          ) : (
                            <div className="w-6 h-6 rounded-full bg-gradient-to-br from-primary/30 to-accent/30 flex items-center justify-center text-[10px] font-bold border border-primary/40 shadow-md">{server.name.substring(0, 2)}</div>
                          )}
                          {server.name}
                        </span>
                        <div className="flex items-center gap-1.5 mt-1.5 text-xs text-muted-foreground font-medium">
                          <Users className="h-3 w-3" />
                          <span>{server.member_count} membros</span>
                        </div>
                      </div>
                    </TabsTrigger>
                  ))}
                </TabsList>

                {servers.map((server) => (
                  <TabsContent key={server.id} value={server.id} className="mt-0 space-y-8 animate-slide-in-up">
                    <div className="grid gap-6 md:grid-cols-2 lg:grid-cols-4">
                      <Card className="bg-card/50 border-primary/20 hover:border-primary/50 card-hover glass-card group animate-bounce-in" style={{ animationDelay: "0.1s" }}>
                        <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
                          <CardTitle className="text-sm font-medium text-muted-foreground group-hover:text-primary transition-colors">Total de Membros</CardTitle>
                          <Users className="h-5 w-5 text-primary group-hover:scale-125 transition-all duration-300 animate-glow" />
                        </CardHeader>
                        <CardContent>
                          <div className="text-3xl font-bold text-gradient">{server.member_count}</div>
                          <p className="text-xs text-muted-foreground mt-1">
                            Usuários no servidor
                          </p>
                        </CardContent>
                      </Card>
                      {/* Add more summary cards here if needed */}
                    </div>

                    <div className="space-y-8">
                      <section className="relative">
                        <div className="flex items-center gap-2 mb-4">
                          <Activity className="h-5 w-5 text-primary" />
                          <h2 className="text-2xl font-bold">Estatísticas</h2>
                        </div>
                        <div className="rounded-xl border border-primary/10 bg-card/30 p-1 shadow-sm backdrop-blur-sm">
                          <StatsDashboard serverId={server.id} />
                        </div>
                      </section>

                      <section>
                        <div className="flex items-center gap-2 mb-4">
                          <Users className="h-5 w-5 text-primary" />
                          <h2 className="text-2xl font-bold">Gerenciamento de Usuários</h2>
                        </div>
                        <div className="rounded-xl border border-primary/10 bg-card/30 p-1 shadow-sm backdrop-blur-sm">
                          <UserManagement serverId={server.id} />
                        </div>
                      </section>
                    </div>
                  </TabsContent>
                ))}
              </Tabs>
            ) : (
              <div className="text-center py-12">
                <div className="mx-auto h-16 w-16 rounded-full bg-muted/50 flex items-center justify-center mb-4 animate-pulse">
                  <Server className="h-8 w-8 text-muted-foreground" />
                </div>
                <h3 className="text-lg font-semibold">Nenhum servidor encontrado</h3>
                <p className="text-muted-foreground mt-2 max-w-md mx-auto">
                  O bot ainda não sincronizou os dados dos servidores. Certifique-se de que o bot está online e conectado ao banco de dados.
                </p>
              </div>
            )}
          </CardContent>
        </Card>
      </main>

      <footer className="border-t border-primary/10 bg-card/30 py-8 backdrop-blur-md mt-auto">
        <div className="container mx-auto px-4 text-center text-sm text-muted-foreground">
          <p className="flex items-center justify-center gap-2">
            <Bot className="h-4 w-4" />
            © 2024 Macacolândia Bot • Desenvolvido com <span className="text-primary">♥</span> e Next.js
          </p>
        </div>
      </footer>
    </div>
  );
}
