"use client";

import { useQuery } from "@tanstack/react-query";
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from "@/components/ui/card";
import { Users, Coins, Gamepad2, TrendingUp } from "lucide-react";

interface StatsDashboardProps {
  serverId: string;
}

export function StatsDashboard({ serverId }: StatsDashboardProps) {
  const { data: stats, isLoading } = useQuery({
    queryKey: ["stats", serverId],
    queryFn: async () => {
      const res = await fetch(`/api/stats?guildId=${serverId}`);
      if (!res.ok) throw new Error("Failed to fetch stats");
      return res.json();
    },
  });

  if (isLoading) {
    return (
      <div className="flex items-center justify-center p-8">
        <div className="h-8 w-8 animate-spin rounded-full border-4 border-primary border-t-transparent"></div>
      </div>
    );
  }

  const globalStats = stats?.global || {};
  const gameStats = stats?.games || [];

  return (
    <div className="space-y-6">
      <div className="grid gap-4 md:grid-cols-2 lg:grid-cols-4">
        <Card className="bg-card/50 border-primary/10 hover:border-primary/40 card-hover glass-card animate-slide-in-up group" style={{ animationDelay: "0.1s" }}>
          <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
            <CardTitle className="text-sm font-medium">Total de Usuários</CardTitle>
            <Users className="h-4 w-4 text-muted-foreground group-hover:text-primary transition-colors" />
          </CardHeader>
          <CardContent>
            <div className="text-2xl font-bold">{globalStats.totalUsers?.count || 0}</div>
            <p className="text-xs text-muted-foreground">Usuários cadastrados</p>
          </CardContent>
        </Card>

        <Card className="bg-card/50 border-primary/10 hover:border-primary/40 card-hover glass-card animate-slide-in-up group" style={{ animationDelay: "0.2s" }}>
          <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
            <CardTitle className="text-sm font-medium">Total de Moedas</CardTitle>
            <Coins className="h-4 w-4 text-yellow-400 group-hover:text-yellow-300 transition-all duration-300 group-hover:rotate-12 group-hover:scale-110" />
          </CardHeader>
          <CardContent>
            <div className="text-2xl font-bold">
              {(globalStats.totalCoins?.total || 0).toLocaleString()}
            </div>
            <p className="text-xs text-muted-foreground">Em circulação</p>
          </CardContent>
        </Card>

        <Card className="bg-card/50 border-primary/10 hover:border-primary/40 card-hover glass-card animate-slide-in-up group" style={{ animationDelay: "0.3s" }}>
          <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
            <CardTitle className="text-sm font-medium">Total de Jogos</CardTitle>
            <Gamepad2 className="h-4 w-4 text-primary group-hover:text-primary/80 transition-all duration-300 group-hover:rotate-12 group-hover:scale-110" />
          </CardHeader>
          <CardContent>
            <div className="text-2xl font-bold">
              {(globalStats.totalGames?.count || 0).toLocaleString()}
            </div>
            <p className="text-xs text-muted-foreground">Jogos realizados</p>
          </CardContent>
        </Card>

        <Card className="bg-card/50 border-primary/10 hover:border-primary/40 card-hover glass-card animate-slide-in-up group" style={{ animationDelay: "0.4s" }}>
          <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
            <CardTitle className="text-sm font-medium">Média por Usuário</CardTitle>
            <TrendingUp className="h-4 w-4 text-green-400 group-hover:text-green-300 transition-all duration-300 group-hover:rotate-12 group-hover:scale-110" />
          </CardHeader>
          <CardContent>
            <div className="text-2xl font-bold">
              {Math.round(globalStats.avgCoinsPerUser?.avg || 0).toLocaleString()}
            </div>
            <p className="text-xs text-muted-foreground">Moedas/usuário</p>
          </CardContent>
        </Card>
      </div>

      <Card className="bg-card/50 border-primary/10 shadow-sm glass-card animate-slide-in-up" style={{ animationDelay: "0.5s" }}>
        <CardHeader>
          <CardTitle className="text-gradient">Estatísticas por Jogo</CardTitle>
          <CardDescription>Desempenho de cada jogo do cassino</CardDescription>
        </CardHeader>
        <CardContent>
          <div className="space-y-6">
            {Array.isArray(gameStats) && gameStats.length > 0 ? (
              gameStats.map((game: any) => {
                const winRate =
                  game.total_games > 0 ? ((game.wins / game.total_games) * 100).toFixed(1) : "0.0";
                const netProfit = game.total_winnings - game.total_bet;
                const isProfit = netProfit >= 0;

                return (
                  <div key={game.game_type} className="space-y-3 border-b border-border/50 pb-4 last:border-0 last:pb-0">
                    <div className="flex items-center justify-between">
                      <div>
                        <h4 className="font-semibold capitalize flex items-center gap-2">
                          {game.game_type}
                          <span className="text-xs font-normal px-2 py-0.5 rounded-full bg-secondary text-muted-foreground">
                            {game.total_games} jogos
                          </span>
                        </h4>
                      </div>
                      <div className="text-right">
                        <div className="text-sm font-medium">{winRate}% Win Rate</div>
                        <div
                          className={`text-sm font-semibold ${
                            isProfit ? "text-green-500" : "text-red-500"
                          }`}
                        >
                          {isProfit ? "+" : ""}
                          {netProfit.toLocaleString()} 🪙
                        </div>
                      </div>
                    </div>
                    <div className="relative h-2.5 w-full overflow-hidden rounded-full bg-secondary/50">
                      <div
                        className="h-full bg-gradient-to-r from-primary to-purple-400 transition-all duration-1000 ease-out"
                        style={{ width: `${winRate}%` }}
                      />
                    </div>
                  </div>
                );
              })
            ) : (
              <div className="py-12 text-center text-muted-foreground flex flex-col items-center">
                <Gamepad2 className="h-12 w-12 mb-4 opacity-20" />
                <p>Nenhuma estatística de jogo disponível</p>
              </div>
            )}
          </div>
        </CardContent>
      </Card>
    </div>
  );
}
