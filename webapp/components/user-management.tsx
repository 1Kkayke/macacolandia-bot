"use client";

import { useState } from "react";
import { useQuery, useMutation, useQueryClient } from "@tanstack/react-query";
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from "@/components/ui/card";
import { Button } from "@/components/ui/button";
import { Input } from "@/components/ui/input";
import { Label } from "@/components/ui/label";
import { Badge } from "@/components/ui/badge";
import { Table, TableBody, TableCell, TableHead, TableHeader, TableRow } from "@/components/ui/table";
import { User } from "@/lib/db";
import { Coins, TrendingUp, TrendingDown, Trophy, User as UserIcon } from "lucide-react";

interface UserManagementProps {
  serverId: string;
}

export function UserManagement({ serverId }: UserManagementProps) {
  const [selectedUser, setSelectedUser] = useState<User | null>(null);
  const [coinAmount, setCoinAmount] = useState<string>("");
  const [description, setDescription] = useState<string>("");
  const queryClient = useQueryClient();

  const { data: users, isLoading } = useQuery<User[]>({
    queryKey: ["users", serverId],
    queryFn: async () => {
      const res = await fetch(`/api/users?guildId=${serverId}`);
      if (!res.ok) throw new Error("Failed to fetch users");
      return res.json();
    },
  });

  const updateCoinsMutation = useMutation({
    mutationFn: async ({ userId, amount, desc }: { userId: string; amount: number; desc?: string }) => {
      const res = await fetch(`/api/users/${userId}/coins`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ amount, description: desc }),
      });
      if (!res.ok) throw new Error("Failed to update coins");
      return res.json();
    },
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ["users", serverId] });
      setCoinAmount("");
      setDescription("");
      setSelectedUser(null);
    },
  });

  const handleAddCoins = () => {
    if (!selectedUser || !coinAmount) return;
    const amount = parseInt(coinAmount);
    if (isNaN(amount)) return;
    
    updateCoinsMutation.mutate({
      userId: selectedUser.user_id,
      amount,
      desc: description || `Admin adjustment: ${amount > 0 ? 'added' : 'removed'} ${Math.abs(amount)} coins`,
    });
  };

  const handleRemoveCoins = () => {
    if (!selectedUser || !coinAmount) return;
    const amount = parseInt(coinAmount);
    if (isNaN(amount)) return;
    
    updateCoinsMutation.mutate({
      userId: selectedUser.user_id,
      amount: -Math.abs(amount),
      desc: description || `Admin adjustment: removed ${Math.abs(amount)} coins`,
    });
  };

  if (isLoading) {
    return (
      <div className="flex items-center justify-center p-8">
        <div className="h-8 w-8 animate-spin rounded-full border-4 border-primary border-t-transparent"></div>
      </div>
    );
  }

  return (
    <div className="grid gap-6 md:grid-cols-2">
      <Card className="bg-card/50 border-primary/10 shadow-sm h-full flex flex-col glass-card animate-slide-in-right" style={{ animationDelay: "0.1s" }}>
        <CardHeader>
          <CardTitle className="flex items-center gap-2 text-gradient">
            <UserIcon className="h-5 w-5 text-primary animate-glow" />
            Usuários do Servidor
          </CardTitle>
          <CardDescription>Selecione um usuário para gerenciar</CardDescription>
        </CardHeader>
        <CardContent className="flex-1 overflow-hidden">
          <div className="max-h-[600px] overflow-y-auto pr-2 custom-scrollbar">
            <Table>
              <TableHeader>
                <TableRow className="hover:bg-transparent border-primary/10">
                  <TableHead>Usuário</TableHead>
                  <TableHead className="text-right">Moedas</TableHead>
                  <TableHead className="text-right">Jogos</TableHead>
                </TableRow>
              </TableHeader>
              <TableBody>
                {users?.map((user) => (
                  <TableRow
                    key={user.user_id}
                    className={`cursor-pointer transition-all duration-300 border-primary/5 ${
                      selectedUser?.user_id === user.user_id 
                        ? "bg-primary/15 hover:bg-primary/20 shadow-[inset_0_0_12px_rgba(168,85,247,0.2)]" 
                        : "hover:bg-primary/8 hover:shadow-sm"
                    }`}
                    onClick={() => setSelectedUser(user)}
                  >
                    <TableCell className="font-medium">
                      <div className="flex items-center gap-2">
                        <div className={`w-2 h-2 rounded-full ${selectedUser?.user_id === user.user_id ? "bg-primary animate-pulse" : "bg-muted"}`}></div>
                        {user.username}
                        {user.coins < 0 && (
                          <Badge variant="destructive" className="ml-2 text-[10px] px-1.5 py-0 h-5">
                            Devedor
                          </Badge>
                        )}
                      </div>
                    </TableCell>
                    <TableCell className="text-right">
                      <div className="flex items-center justify-end gap-1 font-mono">
                        <Coins className="h-3.5 w-3.5 text-yellow-500" />
                        <span>{user.coins.toLocaleString()}</span>
                      </div>
                    </TableCell>
                    <TableCell className="text-right font-mono text-muted-foreground">{user.games_played}</TableCell>
                  </TableRow>
                ))}
              </TableBody>
            </Table>
          </div>
        </CardContent>
      </Card>

      <Card className="bg-card/50 border-primary/10 shadow-sm h-full flex flex-col glass-card animate-slide-in-right" style={{ animationDelay: "0.2s" }}>
        <CardHeader>
          <CardTitle className="flex items-center gap-2 text-gradient">
            <Coins className="h-5 w-5 text-yellow-400 animate-glow" />
            Gerenciar Moedas
          </CardTitle>
          <CardDescription>
            {selectedUser
              ? `Gerenciando: ${selectedUser.username}`
              : "Selecione um usuário para gerenciar"}
          </CardDescription>
        </CardHeader>
        <CardContent className="space-y-6 flex-1">
          {selectedUser ? (
            <div className="animate-in fade-in slide-in-from-right-4 duration-300 space-y-6">
              <div className="grid grid-cols-2 gap-4">
                <div className="space-y-2 p-4 rounded-xl bg-primary/5 border border-primary/10">
                  <div className="text-sm text-muted-foreground">Saldo Atual</div>
                  <div className="flex items-center gap-2 text-2xl font-bold">
                    <Coins className="h-6 w-6 text-yellow-500" />
                    {selectedUser.coins.toLocaleString()}
                  </div>
                </div>
                <div className="space-y-2 p-4 rounded-xl bg-primary/5 border border-primary/10">
                  <div className="text-sm text-muted-foreground">Total de Jogos</div>
                  <div className="flex items-center gap-2 text-2xl font-bold">
                    <Trophy className="h-6 w-6 text-primary" />
                    {selectedUser.games_played}
                  </div>
                </div>
                <div className="space-y-2 p-3 rounded-lg bg-green-500/5 border border-green-500/10">
                  <div className="text-sm text-muted-foreground">Total Ganho</div>
                  <div className="flex items-center gap-2 text-lg font-semibold text-green-500">
                    <TrendingUp className="h-5 w-5" />
                    {selectedUser.total_won.toLocaleString()}
                  </div>
                </div>
                <div className="space-y-2 p-3 rounded-lg bg-red-500/5 border border-red-500/10">
                  <div className="text-sm text-muted-foreground">Total Perdido</div>
                  <div className="flex items-center gap-2 text-lg font-semibold text-red-500">
                    <TrendingDown className="h-5 w-5" />
                    {selectedUser.total_lost.toLocaleString()}
                  </div>
                </div>
              </div>

              <div className="space-y-4 border-t border-primary/10 pt-6">
                <div className="space-y-2">
                  <Label htmlFor="amount">Quantidade de Moedas</Label>
                  <Input
                    id="amount"
                    type="number"
                    placeholder="100"
                    value={coinAmount}
                    onChange={(e) => setCoinAmount(e.target.value)}
                    className="bg-background/50 border-primary/20 focus:border-primary"
                  />
                </div>
                <div className="space-y-2">
                  <Label htmlFor="description">Descrição (opcional)</Label>
                  <Input
                    id="description"
                    type="text"
                    placeholder="Motivo do ajuste..."
                    value={description}
                    onChange={(e) => setDescription(e.target.value)}
                    className="bg-background/50 border-primary/20 focus:border-primary"
                  />
                </div>
                <div className="flex gap-3 pt-2">
                  <Button
                    onClick={handleAddCoins}
                    disabled={!coinAmount || updateCoinsMutation.isPending}
                    className="flex-1 bg-gradient-to-r from-primary to-accent hover:from-primary/90 hover:to-accent/90 text-white shadow-lg shadow-primary/30 transition-all hover:-translate-y-1 hover:shadow-xl hover:shadow-primary/40 animate-shimmer"
                  >
                    <TrendingUp className="mr-2 h-4 w-4" />
                    Adicionar
                  </Button>
                  <Button
                    onClick={handleRemoveCoins}
                    disabled={!coinAmount || updateCoinsMutation.isPending}
                    variant="destructive"
                    className="flex-1 shadow-lg shadow-destructive/30 transition-all hover:-translate-y-1 hover:shadow-xl hover:shadow-destructive/40"
                  >
                    <TrendingDown className="mr-2 h-4 w-4" />
                    Remover
                  </Button>
                </div>
              </div>
            </div>
          ) : (
            <div className="h-full flex flex-col items-center justify-center text-center text-muted-foreground py-12 opacity-60">
              <div className="h-20 w-20 rounded-full bg-primary/10 flex items-center justify-center mb-4 animate-pulse">
                <UserIcon className="h-10 w-10 text-primary/50" />
              </div>
              <p className="text-lg font-medium">Nenhum usuário selecionado</p>
              <p className="text-sm max-w-[200px] mt-2">Selecione um usuário da lista ao lado para visualizar detalhes e gerenciar moedas</p>
            </div>
          )}
        </CardContent>
      </Card>
    </div>
  );
}
