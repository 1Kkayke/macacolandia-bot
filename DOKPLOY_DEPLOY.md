# 🐳 Deploy no Dokploy

## 📦 Pré-requisitos

- Servidor com Dokploy instalado
- Acesso SSH ao servidor
- Repositório GitHub: https://github.com/1Kkayke/macacolandia-bot

## 🚀 Passos para Deploy

### 1. Acessar Dokploy

Abra o navegador e acesse: `http://seu-servidor-ip:3000`

### 2. Criar Novo Projeto

1. No dashboard do Dokploy, clique em **"Create Application"**
2. Escolha **"GitHub"** como fonte
3. Conecte sua conta do GitHub
4. Selecione o repositório: **`1Kkayke/macacolandia-bot`**
5. Branch: **`main`**

### 3. Configurar Build

- **Build Method**: Docker
- **Dockerfile Path**: `Dockerfile` (já existe no projeto)
- **Build Context**: `/`

### 4. Configurar Variáveis de Ambiente

Adicione as seguintes variáveis:

```
DISCORD_TOKEN=seu_token_aqui
PREFIX=!
```

### 5. Configurar Recursos

- **Memory**: 512MB (mínimo recomendado)
- **CPU**: 0.5 vCPU
- **Restart Policy**: Always

### 6. Deploy

1. Clique em **"Deploy"**
2. Aguarde o build (2-3 minutos)
3. Verifique os logs

### 7. Verificar Logs

Após o deploy, você deve ver:
```
🤖 Bot conectado como MacacolandiaBot
📊 ID: 1438891181672108102
🎵 Bot de música Macacolândia está online!
------
```

## 🔄 Atualizações Automáticas

Configure webhook do GitHub:

1. No Dokploy, copie a URL do webhook
2. No GitHub, vá em Settings → Webhooks → Add webhook
3. Cole a URL do Dokploy
4. Selecione "Just the push event"

Agora, todo push no GitHub atualiza automaticamente!

## 🐛 Troubleshooting

### Bot não conecta
- Verifique as variáveis de ambiente
- Confirme que o token está correto
- Verifique os logs de build

### Erro de memória
- Aumente a memória para 1GB

### FFmpeg não encontrado
- O Dockerfile já instala o FFmpeg automaticamente

## 📊 Monitoramento

No Dokploy você pode:
- Ver logs em tempo real
- Monitorar uso de recursos
- Reiniciar o container
- Ver histórico de deploys
