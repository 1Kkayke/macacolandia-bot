"use client";

import Link from "next/link";
import { usePathname } from "next/navigation";
import { Bot, Home, Shield, LogOut } from "lucide-react";
import { Button } from "@/components/ui/button";
import { signOut, useSession } from "next-auth/react";

export function NavBar() {
  const pathname = usePathname();
  const { data: session } = useSession();
  const user = session?.user as any;

  const handleSignOut = () => {
    signOut({ callbackUrl: "/auth/login" });
  };

  const navItems = [
    { href: "/", label: "Dashboard", icon: Home },
    ...(user?.role === "admin"
      ? [{ href: "/admin", label: "Admin", icon: Shield }]
      : []),
  ];

  return (
    <nav className="sticky top-0 z-50 border-b border-primary/10 bg-card/60 backdrop-blur-xl shadow-sm">
      <div className="container mx-auto px-4">
        <div className="flex h-16 items-center justify-between">
          <div className="flex items-center gap-8">
            <Link href="/" className="flex items-center gap-2 group">
              <div className="relative">
                <div className="absolute inset-0 rounded-full bg-primary/20 blur-md opacity-0 group-hover:opacity-100 transition-opacity duration-500"></div>
                <Bot className="relative h-8 w-8 text-primary transition-transform duration-300 group-hover:scale-110 group-hover:rotate-3" />
              </div>
              <span className="text-xl font-bold bg-gradient-to-r from-foreground to-primary/80 bg-clip-text text-transparent">
                Macacolândia Bot
              </span>
            </Link>

            <div className="flex items-center gap-1">
              {navItems.map((item) => (
                <Link
                  key={item.href}
                  href={item.href}
                  className={`relative flex items-center gap-2 px-4 py-2 rounded-full text-sm font-medium transition-all duration-300 ${
                    pathname === item.href
                      ? "text-primary bg-primary/10 shadow-[0_0_10px_rgba(139,92,246,0.1)]"
                      : "text-muted-foreground hover:text-primary hover:bg-primary/5"
                  }`}
                >
                  <item.icon className={`h-4 w-4 ${pathname === item.href ? "animate-pulse" : ""}`} />
                  {item.label}
                </Link>
              ))}
            </div>
          </div>

          {session && (
            <div className="flex items-center gap-4">
              <div className="text-sm text-right hidden md:block">
                <div className="font-medium text-foreground">{user?.name}</div>
                <div className="text-xs text-primary/80 font-semibold uppercase tracking-wider">{user?.role}</div>
              </div>
              <Button 
                variant="outline" 
                size="sm" 
                onClick={handleSignOut}
                className="border-primary/20 hover:bg-destructive/10 hover:text-destructive hover:border-destructive/30 transition-all duration-300"
              >
                <LogOut className="h-4 w-4 mr-2" />
                Sair
              </Button>
            </div>
          )}
        </div>
      </div>
    </nav>
  );
}
