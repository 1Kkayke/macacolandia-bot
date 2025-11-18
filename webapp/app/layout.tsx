import type { Metadata } from "next";
import "./globals.css";
import { Providers } from "./providers";
import { SessionProvider } from "next-auth/react";

export const metadata: Metadata = {
  title: "Macacolândia Bot Admin",
  description: "Painel de administração do Bot Macacolândia",
};

export default function RootLayout({
  children,
}: Readonly<{
  children: React.ReactNode;
}>) {
  return (
    <html lang="pt-BR">
      <body className="antialiased">
        <SessionProvider>
          <Providers>{children}</Providers>
        </SessionProvider>
      </body>
    </html>
  );
}
