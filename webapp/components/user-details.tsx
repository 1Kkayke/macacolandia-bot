"use client";

import { useState } from "react";
import { useQuery } from "@tanstack/react-query";
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from "@/components/ui/card";
import { Tabs, TabsContent, TabsList, TabsTrigger } from "@/components/ui/tabs";
import { Badge } from "@/components/ui/badge";
import { Table, TableBody, TableCell, TableHead, TableHeader, TableRow } from "@/components/ui/table";
import { User, Transaction, GameHistory, Achievement } from "@/lib/db";
import { Clock, Coins, Trophy, History } from "lucide-react";

interface UserDetailsProps {
  userId: string;
  onClose: () => void;
}

export function UserDetails({ userId, onClose }: UserDetailsProps) {
  const [activeTab, setActiveTab] = useState("transactions");

  const { data: user } = useQuery<User>({
    queryKey: ["user", userId],
    queryFn: async () => {
      const res = await fetch(`/api/users?userId=${userId}`);
      if (!res.ok) throw new Error("Failed to fetch user");
      return res.json();
    },
  });

  const { data: transactions } = useQuery<Transaction[]>({
    queryKey: ["transactions", userId],
    queryFn: async () => {
      const res = await fetch(`/api/users/${userId}/transactions?limit=50`);
      if (!res.ok) throw new Error("Failed to fetch transactions");
      return res.json();
    },
    enabled: activeTab === "transactions",
  });

  const { data: gameHistory } = useQuery<GameHistory[]>({
    queryKey: ["gameHistory", userId],
    queryFn: async () => {
      const res = await fetch(`/api/users/${userId}/games?limit=50`);
      if (!res.ok) throw new Error("Failed to fetch game history");
      return res.json();
    },
    enabled: activeTab === "games",
  });

  const { data: achievements } = useQuery<Achievement[]>({
    queryKey: ["achievements", userId],
    queryFn: async () => {
      const res = await fetch(`/api/users/${userId}/games?type=achievements`);
      if (!res.ok) throw new Error("Failed to fetch achievements");
      return res.json();
    },
    enabled: activeTab === "achievements",
  });

  if (!user) {
    return <div>Carregando...</div>;
  }

  const formatDate = (dateStr: string) => {
    return new Date(dateStr).toLocaleString("pt-BR");
  };

  return (
    <Card className="w-full">
      <CardHeader>
        <div className="flex items-center justify-between">
          <div>
            <CardTitle>{user.username}</CardTitle>
            <CardDescription>ID: {user.user_id}</CardDescription>
          </div>
          <button
            onClick={onClose}
            className="text-muted-foreground hover:text-foreground"
          >
            ✕
          </button>
        </div>
      </CardHeader>
      <CardContent>
        <Tabs value={activeTab} onValueChange={setActiveTab}>
          <TabsList className="grid w-full grid-cols-3">
            <TabsTrigger value="transactions">
              <Coins className="mr-2 h-4 w-4" />
              Transações
            </TabsTrigger>
            <TabsTrigger value="games">
              <History className="mr-2 h-4 w-4" />
              Histórico
            </TabsTrigger>
            <TabsTrigger value="achievements">
              <Trophy className="mr-2 h-4 w-4" />
              Conquistas
            </TabsTrigger>
          </TabsList>

          <TabsContent value="transactions" className="space-y-4">
            <div className="max-h-[400px] overflow-y-auto">
              <Table>
                <TableHeader>
                  <TableRow>
                    <TableHead>Data</TableHead>
                    <TableHead>Tipo</TableHead>
                    <TableHead>Descrição</TableHead>
                    <TableHead className="text-right">Valor</TableHead>
                  </TableRow>
                </TableHeader>
                <TableBody>
                  {transactions?.map((tx) => (
                    <TableRow key={tx.id}>
                      <TableCell className="text-xs">{formatDate(tx.timestamp)}</TableCell>
                      <TableCell>
                        <Badge variant={tx.amount > 0 ? "default" : "destructive"}>
                          {tx.transaction_type}
                        </Badge>
                      </TableCell>
                      <TableCell className="text-sm">{tx.description || "-"}</TableCell>
                      <TableCell
                        className={`text-right font-semibold ${
                          tx.amount > 0 ? "text-green-600" : "text-red-600"
                        }`}
                      >
                        {tx.amount > 0 ? "+" : ""}
                        {tx.amount.toLocaleString()}
                      </TableCell>
                    </TableRow>
                  ))}
                </TableBody>
              </Table>
            </div>
          </TabsContent>

          <TabsContent value="games" className="space-y-4">
            <div className="max-h-[400px] overflow-y-auto">
              <Table>
                <TableHeader>
                  <TableRow>
                    <TableHead>Data</TableHead>
                    <TableHead>Jogo</TableHead>
                    <TableHead className="text-right">Aposta</TableHead>
                    <TableHead>Resultado</TableHead>
                    <TableHead className="text-right">Ganhos</TableHead>
                  </TableRow>
                </TableHeader>
                <TableBody>
                  {gameHistory?.map((game) => (
                    <TableRow key={game.id}>
                      <TableCell className="text-xs">{formatDate(game.timestamp)}</TableCell>
                      <TableCell className="capitalize font-medium">{game.game_type}</TableCell>
                      <TableCell className="text-right">{game.bet_amount.toLocaleString()}</TableCell>
                      <TableCell>
                        <Badge variant={game.result === "win" ? "default" : "destructive"}>
                          {game.result === "win" ? "Vitória" : "Derrota"}
                        </Badge>
                      </TableCell>
                      <TableCell
                        className={`text-right font-semibold ${
                          game.winnings > 0 ? "text-green-600" : "text-red-600"
                        }`}
                      >
                        {game.winnings > 0 ? "+" : ""}
                        {game.winnings.toLocaleString()}
                      </TableCell>
                    </TableRow>
                  ))}
                </TableBody>
              </Table>
            </div>
          </TabsContent>

          <TabsContent value="achievements" className="space-y-4">
            <div className="grid gap-4 md:grid-cols-2">
              {achievements?.map((achievement) => (
                <Card key={achievement.id}>
                  <CardHeader>
                    <CardTitle className="flex items-center gap-2 text-base">
                      <Trophy className="h-5 w-5 text-yellow-600" />
                      {achievement.achievement_name}
                    </CardTitle>
                  </CardHeader>
                  <CardContent>
                    <div className="flex items-center gap-2 text-sm text-muted-foreground">
                      <Clock className="h-4 w-4" />
                      Desbloqueado em {formatDate(achievement.unlocked_at)}
                    </div>
                  </CardContent>
                </Card>
              ))}
              {!achievements?.length && (
                <div className="col-span-2 py-8 text-center text-muted-foreground">
                  Nenhuma conquista desbloqueada ainda
                </div>
              )}
            </div>
          </TabsContent>
        </Tabs>
      </CardContent>
    </Card>
  );
}
