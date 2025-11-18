import { NavBar } from "@/components/nav-bar";

export default function AdminLayout({
  children,
}: {
  children: React.ReactNode;
}) {
  return (
    <div className="min-h-screen bg-gradient-to-br from-background to-muted/20">
      <NavBar />
      <main className="container mx-auto px-4 py-8">{children}</main>
    </div>
  );
}
