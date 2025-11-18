"use client";

import { Card, CardContent, CardDescription, CardHeader, CardTitle } from "@/components/ui/card";
import { AuthGuard } from "@/lib/auth-guard";
import { Shield, Users, FileText, Settings } from "lucide-react";
import Link from "next/link";

export default function AdminPage() {
  return (
    <AuthGuard requireAdmin>
      <AdminPageContent />
    </AuthGuard>
  );
}

function AdminPageContent() {
  const adminSections = [
    {
      title: "Solicitações de Registro",
      description: "Aprovar ou rejeitar novas solicitações",
      icon: FileText,
      href: "/admin/registrations",
      color: "text-blue-600",
    },
    {
      title: "Gerenciar Usuários",
      description: "Gerenciar todos os usuários do sistema",
      icon: Users,
      href: "/admin/users",
      color: "text-green-600",
    },
    {
      title: "Logs de Atividade",
      description: "Visualizar ações dos usuários",
      icon: Shield,
      href: "/admin/logs",
      color: "text-purple-600",
    },
    {
      title: "Configurações do Bot",
      description: "Configurar jogos, servidores e regras",
      icon: Settings,
      href: "/",
      color: "text-orange-600",
    },
  ];

  return (
    <div className="space-y-6">
      <div>
        <h1 className="text-3xl font-bold">Painel Administrativo</h1>
        <p className="text-muted-foreground mt-2">
          Gerencie usuários, solicitações e configurações do sistema
        </p>
      </div>

      <div className="grid gap-6 md:grid-cols-2">
        {adminSections.map((section) => (
          <Link key={section.href} href={section.href}>
            <Card className="hover:shadow-lg transition-shadow cursor-pointer h-full">
              <CardHeader>
                <div className="flex items-center gap-4">
                  <div className={`p-3 rounded-lg bg-muted ${section.color}`}>
                    <section.icon className="h-6 w-6" />
                  </div>
                  <div>
                    <CardTitle>{section.title}</CardTitle>
                    <CardDescription className="mt-1">
                      {section.description}
                    </CardDescription>
                  </div>
                </div>
              </CardHeader>
            </Card>
          </Link>
        ))}
      </div>
    </div>
  );
}
