# 🌐 Macacolândia Bot - Web Admin Panel

Painel de administração web para gerenciar o bot Macacolândia Discord, permitindo controle completo sobre usuários, economia, e estatísticas dos jogos.

## 🚀 Funcionalidades

### 💰 Gerenciamento de Usuários
- Visualizar todos os usuários de cada servidor
- Adicionar ou remover moedas de usuários
- Ver estatísticas detalhadas de cada usuário (jogos jogados, vitórias, perdas)
- Histórico completo de transações
- Histórico de jogos com detalhes de apostas e ganhos
- Visualizar conquistas desbloqueadas

### 📊 Dashboard de Estatísticas
- Estatísticas globais do servidor
- Total de usuários, moedas em circulação, jogos realizados
- Estatísticas por jogo (win rate, lucro/prejuízo)
- Média de moedas por usuário

### 🖥️ Multi-Servidor
- Suporte completo para múltiplos servidores Discord
- Interface com abas para navegar entre servidores
- Estatísticas e gerenciamento isolado por servidor

### 📱 Design Responsivo
- Interface moderna e intuitiva
- Totalmente responsivo para dispositivos móveis
- Tema escuro/claro automático
- Componentes acessíveis e elegantes

## 🛠️ Tecnologias Utilizadas

- **Framework**: Next.js 14+ (App Router)
- **Linguagem**: TypeScript
- **Estilização**: Tailwind CSS
- **Componentes**: shadcn/ui (componentes acessíveis)
- **State Management**: TanStack Query (React Query)
- **Formulários**: React Hook Form + Zod
- **Banco de Dados**: better-sqlite3 (interface com SQLite do bot)
- **Ícones**: Lucide React

## 📦 Instalação

1. **Navegue até a pasta do webapp:**
```bash
cd webapp
```

2. **Instale as dependências:**
```bash
npm install
```

3. **Configure o ambiente:**
O webapp usa o banco de dados SQLite do bot localizado em `../data/macacolandia.db`. Certifique-se de que o bot já foi executado ao menos uma vez para criar o banco de dados.

4. **Execute em modo de desenvolvimento:**
```bash
npm run dev
```

O aplicativo estará disponível em [http://localhost:3000](http://localhost:3000)

## 🚀 Produção

### Build
```bash
npm run build
```

### Start
```bash
npm start
```

## 📁 Estrutura do Projeto

```
webapp/
├── app/                          # Next.js App Router
│   ├── api/                      # API Routes
│   │   ├── users/               # Endpoints de usuários
│   │   ├── stats/               # Endpoints de estatísticas
│   │   └── servers/             # Endpoints de servidores
│   ├── layout.tsx               # Layout principal
│   ├── page.tsx                 # Página principal
│   ├── providers.tsx            # React Query Provider
│   └── globals.css              # Estilos globais
├── components/                   # Componentes React
│   ├── ui/                      # Componentes de UI (shadcn)
│   ├── user-management.tsx      # Gerenciamento de usuários
│   ├── stats-dashboard.tsx      # Dashboard de estatísticas
│   └── user-details.tsx         # Detalhes de usuário
├── lib/                         # Bibliotecas e utilitários
│   ├── db.ts                    # Interface com banco de dados
│   └── utils.ts                 # Funções utilitárias
└── public/                      # Arquivos estáticos
```

## 🔌 API Routes

### Usuários
- `GET /api/users` - Lista todos os usuários
- `GET /api/users?userId={id}` - Busca usuário específico
- `POST /api/users/[userId]/coins` - Adiciona/remove moedas
- `GET /api/users/[userId]/transactions` - Histórico de transações
- `GET /api/users/[userId]/games` - Histórico de jogos
- `GET /api/users/[userId]/games?type=achievements` - Conquistas

### Estatísticas
- `GET /api/stats` - Estatísticas globais e por jogo

### Servidores
- `GET /api/servers` - Lista servidores configurados

## 🔐 Segurança

⚠️ **IMPORTANTE**: Este é um painel administrativo. Em produção:

1. **Adicione autenticação**: Implemente NextAuth.js ou similar
2. **Proteja as rotas**: Use middleware para verificar permissões
3. **Rate limiting**: Limite requisições à API
4. **HTTPS**: Use sempre HTTPS em produção
5. **Validação**: Valide todos os inputs no servidor

## 📝 Licença

Este projeto faz parte do Bot Macacolândia e está disponível para uso pessoal e educacional.
