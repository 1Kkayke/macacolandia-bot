# 🌐 Guia de Configuração do Web App - Macacolândia Bot Admin

Este guia detalha como configurar e executar o painel de administração web do Bot Macacolândia.

## 📋 Pré-requisitos

- Node.js 18+ instalado
- Bot Macacolândia já configurado e com banco de dados criado
- NPM ou Yarn como gerenciador de pacotes

## 🚀 Instalação Rápida

### 1. Navegue até a pasta do webapp

```bash
cd webapp
```

### 2. Instale as dependências

```bash
npm install
```

### 3. Execute o servidor de desenvolvimento

```bash
npm run dev
```

O aplicativo estará disponível em: **http://localhost:3000**

## 📊 Funcionalidades do Painel

### Gerenciamento de Usuários
- ✅ Visualizar todos os usuários do servidor
- ✅ Adicionar moedas aos usuários
- ✅ Remover moedas dos usuários
- ✅ Ver estatísticas completas (jogos, vitórias, derrotas)
- ✅ Histórico de transações
- ✅ Histórico de jogos
- ✅ Conquistas desbloqueadas

### Dashboard de Estatísticas
- 📈 Total de usuários cadastrados
- 💰 Total de moedas em circulação
- 🎮 Total de jogos realizados
- 📊 Média de moedas por usuário
- 🎯 Estatísticas detalhadas por jogo (win rate, lucro/prejuízo)

### Multi-Servidor
- 🖥️ Abas para cada servidor Discord
- 📍 Navegação fácil entre servidores
- 🔒 Dados isolados por servidor

## 🏗️ Estrutura do Banco de Dados

O webapp se conecta ao banco de dados SQLite do bot localizado em:
```
../data/macacolandia.db
```

### Tabelas Utilizadas
- **users**: Informações dos usuários (ID, username, coins, stats)
- **transactions**: Histórico de transações de moedas
- **game_history**: Histórico de jogos jogados
- **achievements**: Conquistas desbloqueadas

## 🔧 Comandos Disponíveis

```bash
# Desenvolvimento
npm run dev         # Inicia o servidor de desenvolvimento

# Produção
npm run build       # Cria build otimizado
npm start          # Inicia servidor de produção

# Utilitários
npm run lint       # Verifica código com ESLint
```

## 🎨 Tecnologias Utilizadas

- **Next.js 14+**: Framework React com App Router
- **TypeScript**: Tipagem estática
- **Tailwind CSS**: Estilização utilitária
- **shadcn/ui**: Componentes UI acessíveis
- **React Query**: Gerenciamento de estado e cache
- **better-sqlite3**: Interface com banco de dados SQLite
- **Lucide React**: Ícones modernos

## 🔐 Segurança em Produção

⚠️ **IMPORTANTE**: Este painel é administrativo e deve ser protegido!

### Recomendações para Produção:

1. **Adicione autenticação**
   ```bash
   npm install next-auth
   ```
   Configure NextAuth.js para proteger as rotas.

2. **Use HTTPS**
   Configure um reverse proxy (Nginx, Caddy) com certificado SSL.

3. **Variáveis de ambiente**
   Crie arquivo `.env.local`:
   ```env
   NEXTAUTH_SECRET=seu_secret_aqui
   NEXTAUTH_URL=https://seu-dominio.com
   DATABASE_PATH=../data/macacolandia.db
   ```

4. **Rate Limiting**
   Implemente limitação de requisições para prevenir abuso.

5. **Firewall**
   Configure firewall para permitir acesso apenas de IPs autorizados.

## 🐳 Deploy com Docker

### Dockerfile (exemplo)

```dockerfile
FROM node:18-alpine

WORKDIR /app

# Copiar arquivos do projeto
COPY package*.json ./
RUN npm install --production

COPY . .
RUN npm run build

# Porta do app
EXPOSE 3000

# Comando de inicialização
CMD ["npm", "start"]
```

### docker-compose.yml (exemplo)

```yaml
version: '3.8'

services:
  webapp:
    build: ./webapp
    ports:
      - "3000:3000"
    volumes:
      - ./data:/app/data
    environment:
      - NODE_ENV=production
    restart: unless-stopped
```

## 🚀 Deploy em Serviços Cloud

### Vercel (Recomendado)

1. Conecte seu repositório ao Vercel
2. Configure a pasta raiz como `webapp`
3. Deploy automático a cada commit

### Railway

1. Crie novo projeto no Railway
2. Conecte o repositório
3. Configure:
   - **Root Directory**: `webapp`
   - **Build Command**: `npm run build`
   - **Start Command**: `npm start`

### Netlify

1. Conecte repositório
2. Configure:
   - **Base directory**: `webapp`
   - **Build command**: `npm run build`
   - **Publish directory**: `.next`

## 🔍 Troubleshooting

### Erro: "Cannot find database"
**Solução**: Certifique-se de que o bot foi executado pelo menos uma vez para criar o banco de dados em `data/macacolandia.db`.

### Erro: "Module not found: better-sqlite3"
**Solução**: 
```bash
npm install better-sqlite3
npm install --save-dev @types/better-sqlite3
```

### Erro de build no Vercel/Netlify
**Problema**: better-sqlite3 requer compilação nativa
**Solução**: Use serverless functions ou considere migrar para PostgreSQL/MySQL para ambiente serverless.

### Página não carrega dados
**Solução**: 
1. Verifique console do navegador (F12)
2. Confirme que as API routes estão funcionando: `http://localhost:3000/api/users`
3. Verifique permissões do arquivo do banco de dados

## 📱 Testando em Dispositivos Móveis

### Rede Local
```bash
# Execute com bind em todas as interfaces
npm run dev -- -H 0.0.0.0

# Acesse de seu celular
http://[seu-ip-local]:3000
```

Encontre seu IP local:
- **Windows**: `ipconfig`
- **Linux/Mac**: `ifconfig` ou `ip addr`

## 📝 Próximas Melhorias

- [ ] Sistema de autenticação completo
- [ ] Logs de auditoria
- [ ] Backup automático do banco
- [ ] Gráficos interativos
- [ ] Notificações em tempo real
- [ ] Exportação de relatórios (PDF/CSV)
- [ ] Gerenciamento de configurações do bot
- [ ] Sistema de roles e permissões

## 🤝 Contribuindo

Para contribuir com melhorias no webapp:

1. Fork o projeto
2. Crie uma branch (`git checkout -b feature/melhoria`)
3. Commit suas mudanças (`git commit -m 'Adiciona melhoria'`)
4. Push para a branch (`git push origin feature/melhoria`)
5. Abra um Pull Request

## 📞 Suporte

Se encontrar problemas:
1. Verifique este guia
2. Consulte a documentação do Next.js
3. Abra uma issue no GitHub com detalhes do erro

---

<p align="center">
  Desenvolvido com ❤️ para a comunidade Macacolândia
</p>
