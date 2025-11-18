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
      const res = await fetch(`/api/stats`);
      if (!res.ok) throw new Error("Failed to fetch stats");
      return res.json();
    },
  });

  if (isLoading) {
    return <div className="flex items-center justify-center p-8">Carregando estatísticas...</div>;
  }

  const globalStats = stats?.global || {};
  const gameStats = stats?.games || [];

  return (
    <div className="space-y-6">
      <div className="grid gap-4 md:grid-cols-2 lg:grid-cols-4">
        <Card>
          <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
            <CardTitle className="text-sm font-medium">Total de Usuários</CardTitle>
            <Users className="h-4 w-4 text-muted-foreground" />
          </CardHeader>
          <CardContent>
            <div className="text-2xl font-bold">{globalStats.totalUsers?.count || 0}</div>
            <p className="text-xs text-muted-foreground">Usuários cadastrados</p>
          </CardContent>
        </Card>

        <Card>
          <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
            <CardTitle className="text-sm font-medium">Total de Moedas</CardTitle>
            <Coins className="h-4 w-4 text-yellow-600" />
          </CardHeader>
          <CardContent>
            <div className="text-2xl font-bold">
              {(globalStats.totalCoins?.total || 0).toLocaleString()}
            </div>
            <p className="text-xs text-muted-foreground">Em circulação</p>
          </CardContent>
        </Card>

        <Card>
          <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
            <CardTitle className="text-sm font-medium">Total de Jogos</CardTitle>
            <Gamepad2 className="h-4 w-4 text-purple-600" />
          </CardHeader>
          <CardContent>
            <div className="text-2xl font-bold">
              {(globalStats.totalGames?.count || 0).toLocaleString()}
            </div>
            <p className="text-xs text-muted-foreground">Jogos realizados</p>
          </CardContent>
        </Card>

        <Card>
          <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
            <CardTitle className="text-sm font-medium">Média por Usuário</CardTitle>
            <TrendingUp className="h-4 w-4 text-green-600" />
          </CardHeader>
          <CardContent>
            <div className="text-2xl font-bold">
              {Math.round(globalStats.avgCoinsPerUser?.avg || 0).toLocaleString()}
            </div>
            <p className="text-xs text-muted-foreground">Moedas/usuário</p>
          </CardContent>
        </Card>
      </div>

      <Card>
        <CardHeader>
          <CardTitle>Estatísticas por Jogo</CardTitle>
          <CardDescription>Desempenho de cada jogo do cassino</CardDescription>
        </CardHeader>
        <CardContent>
          <div className="space-y-4">
            {Array.isArray(gameStats) && gameStats.length > 0 ? (
              gameStats.map((game: any) => {
                const winRate =
                  game.total_games > 0 ? ((game.wins / game.total_games) * 100).toFixed(1) : "0.0";
                const netProfit = game.total_winnings - game.total_bet;
                const isProfit = netProfit >= 0;

                return (
                  <div key={game.game_type} className="space-y-2 border-b pb-4 last:border-0">
                    <div className="flex items-center justify-between">
                      <div>
                        <h4 className="font-semibold capitalize">{game.game_type}</h4>
                        <p className="text-sm text-muted-foreground">
                          {game.total_games} jogos • {game.wins} vitórias
                        </p>
                      </div>
                      <div className="text-right">
                        <div className="text-sm font-medium">{winRate}% Win Rate</div>
                        <div
                          className={`text-sm font-semibold ${
                            isProfit ? "text-green-600" : "text-red-600"
                          }`}
                        >
                          {isProfit ? "+" : ""}
                          {netProfit.toLocaleString()} 🪙
                        </div>
                      </div>
                    </div>
                    <div className="relative h-2 w-full overflow-hidden rounded-full bg-secondary">
                      <div
                        className="h-full bg-primary transition-all"
                        style={{ width: `${winRate}%` }}
                      />
                    </div>
                  </div>
                );
              })
            ) : (
              <div className="py-8 text-center text-muted-foreground">
                Nenhuma estatística de jogo disponível
              </div>
            )}
          </div>
        </CardContent>
      </Card>
    </div>
  );
}
