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
import { Coins, TrendingUp, TrendingDown, Trophy } from "lucide-react";

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
    return <div className="flex items-center justify-center p-8">Carregando usuários...</div>;
  }

  return (
    <div className="grid gap-6 md:grid-cols-2">
      <Card>
        <CardHeader>
          <CardTitle>Usuários do Servidor</CardTitle>
          <CardDescription>Selecione um usuário para gerenciar</CardDescription>
        </CardHeader>
        <CardContent>
          <div className="max-h-[600px] overflow-y-auto">
            <Table>
              <TableHeader>
                <TableRow>
                  <TableHead>Usuário</TableHead>
                  <TableHead className="text-right">Moedas</TableHead>
                  <TableHead className="text-right">Jogos</TableHead>
                </TableRow>
              </TableHeader>
              <TableBody>
                {users?.map((user) => (
                  <TableRow
                    key={user.user_id}
                    className={`cursor-pointer ${
                      selectedUser?.user_id === user.user_id ? "bg-muted" : ""
                    }`}
                    onClick={() => setSelectedUser(user)}
                  >
                    <TableCell className="font-medium">
                      {user.username}
                      {user.coins < 0 && (
                        <Badge variant="destructive" className="ml-2">
                          Devedor
                        </Badge>
                      )}
                    </TableCell>
                    <TableCell className="text-right">
                      <div className="flex items-center justify-end gap-1">
                        <Coins className="h-4 w-4 text-yellow-600" />
                        <span>{user.coins.toLocaleString()}</span>
                      </div>
                    </TableCell>
                    <TableCell className="text-right">{user.games_played}</TableCell>
                  </TableRow>
                ))}
              </TableBody>
            </Table>
          </div>
        </CardContent>
      </Card>

      <Card>
        <CardHeader>
          <CardTitle>Gerenciar Moedas</CardTitle>
          <CardDescription>
            {selectedUser
              ? `Gerenciando: ${selectedUser.username}`
              : "Selecione um usuário para gerenciar"}
          </CardDescription>
        </CardHeader>
        <CardContent className="space-y-6">
          {selectedUser ? (
            <>
              <div className="grid grid-cols-2 gap-4">
                <div className="space-y-2">
                  <div className="text-sm text-muted-foreground">Saldo Atual</div>
                  <div className="flex items-center gap-2 text-2xl font-bold">
                    <Coins className="h-6 w-6 text-yellow-600" />
                    {selectedUser.coins.toLocaleString()}
                  </div>
                </div>
                <div className="space-y-2">
                  <div className="text-sm text-muted-foreground">Total de Jogos</div>
                  <div className="flex items-center gap-2 text-2xl font-bold">
                    <Trophy className="h-6 w-6 text-purple-600" />
                    {selectedUser.games_played}
                  </div>
                </div>
                <div className="space-y-2">
                  <div className="text-sm text-muted-foreground">Total Ganho</div>
                  <div className="flex items-center gap-2 text-lg font-semibold text-green-600">
                    <TrendingUp className="h-5 w-5" />
                    {selectedUser.total_won.toLocaleString()}
                  </div>
                </div>
                <div className="space-y-2">
                  <div className="text-sm text-muted-foreground">Total Perdido</div>
                  <div className="flex items-center gap-2 text-lg font-semibold text-red-600">
                    <TrendingDown className="h-5 w-5" />
                    {selectedUser.total_lost.toLocaleString()}
                  </div>
                </div>
              </div>

              <div className="space-y-4 border-t pt-4">
                <div className="space-y-2">
                  <Label htmlFor="amount">Quantidade de Moedas</Label>
                  <Input
                    id="amount"
                    type="number"
                    placeholder="100"
                    value={coinAmount}
                    onChange={(e) => setCoinAmount(e.target.value)}
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
                  />
                </div>
                <div className="flex gap-2">
                  <Button
                    onClick={handleAddCoins}
                    disabled={!coinAmount || updateCoinsMutation.isPending}
                    className="flex-1"
                  >
                    <TrendingUp className="mr-2 h-4 w-4" />
                    Adicionar Moedas
                  </Button>
                  <Button
                    onClick={handleRemoveCoins}
                    disabled={!coinAmount || updateCoinsMutation.isPending}
                    variant="destructive"
                    className="flex-1"
                  >
                    <TrendingDown className="mr-2 h-4 w-4" />
                    Remover Moedas
                  </Button>
                </div>
              </div>
            </>
          ) : (
            <div className="py-8 text-center text-muted-foreground">
              Selecione um usuário da lista ao lado para começar
            </div>
          )}
        </CardContent>
      </Card>
    </div>
  );
}
