# 🐛 Guia de Debug - Webapp Next.js

## 📋 Como Rodar Localmente e Ver os Logs

### 1️⃣ **Instalar Dependências**

```powershell
cd webapp
npm install
```

### 2️⃣ **Rodar em Modo de Desenvolvimento**

```powershell
npm run dev
```

Isso vai iniciar o servidor em: `http://localhost:3000`

**Os logs vão aparecer no terminal!** 🎉

---

## 🔍 Onde Ver os Logs

### **No Terminal (Desenvolvimento Local):**

Quando você roda `npm run dev`, todos os logs aparecem aqui:

```
[AUTH-DB] Tentando conectar ao banco: ...
[REGISTER] Nova solicitação de registro: ...
[AUTH-DB] Inserindo registro pendente: ...
```

### **No Navegador (Console):**

Pressione `F12` e vá na aba **Console** para ver erros do frontend.

---

## 🐛 Como Debugar Erros

### **1. Internal Server Error - 500**

Quando você vê "Internal Server Error", os logs no terminal mostram o erro real.

**Passos:**
1. Abra o terminal onde rodou `npm run dev`
2. Tente fazer o registro novamente
3. Veja o erro que aparece no terminal
4. Procure por linhas começando com `[REGISTER]` ou `[AUTH-DB]`

**Exemplo de erro comum:**
```
[AUTH-DB] Falha ao abrir banco de dados: Error: SQLITE_CANTOPEN: unable to open database file
[AUTH-DB] Caminho do banco: C:\...\data\macacolandia.db
```

### **2. Erro de Banco de Dados**

**Sintomas:**
- `SQLITE_CANTOPEN`: Pasta não existe ou sem permissões
- `SQLITE_LOCKED`: Banco em uso por outro processo
- `SQLITE_CORRUPT`: Banco corrompido

**Soluções:**
```powershell
# Criar pasta manualmente
cd C:\Users\Kayke\Documents\github\macacolandia-bot
mkdir data

# Verificar se existe
ls data

# Dar permissões (se necessário)
icacls data /grant Everyone:F /T
```

### **3. Erro de Import/Module**

**Sintomas:**
- `Cannot find module '@/lib/...'`
- `Module not found`

**Solução:**
```powershell
cd webapp
npm install
```

### **4. Erro de Email (Não Crítico)**

O sistema agora **não falha** se o email não enviar. O registro continua mesmo sem email.

---

## 🛠️ Ferramentas de Debug

### **1. Console Logs (Já Implementado)**

O código já tem logs em todas as etapas críticas:

```typescript
console.log('[REGISTER] Nova solicitação...');
console.log('[AUTH-DB] Conectando...');
console.error('[AUTH-DB] Erro:', error);
```

### **2. VS Code Debugger**

Crie `.vscode/launch.json`:

```json
{
  "version": "0.2.0",
  "configurations": [
    {
      "name": "Next.js: debug server-side",
      "type": "node-terminal",
      "request": "launch",
      "command": "npm run dev",
      "cwd": "${workspaceFolder}/webapp",
      "serverReadyAction": {
        "pattern": "- Local:.+(https?://.+)",
        "uriFormat": "%s",
        "action": "debugWithChrome"
      }
    }
  ]
}
```

Depois:
1. Pressione `F5` no VS Code
2. Coloque breakpoints clicando à esquerda do número da linha
3. Faça o registro
4. O código vai parar nos breakpoints

### **3. Chrome DevTools (Frontend)**

1. Abra o site
2. Pressione `F12`
3. Vá na aba **Network**
4. Faça o registro
5. Clique na requisição `register`
6. Veja **Response** para ver o erro

---

## 📊 Verificar Status do Banco de Dados

### **Criar Script de Teste**

Crie `webapp/test-db.js`:

```javascript
const Database = require('better-sqlite3');
const path = require('path');

const DB_PATH = path.join(__dirname, '..', 'data', 'macacolandia.db');

console.log('🔍 Testando conexão com banco...');
console.log('📁 Caminho:', DB_PATH);

try {
  const db = new Database(DB_PATH, { readonly: false });
  console.log('✅ Conexão bem sucedida!');
  
  // Testar tabelas
  const tables = db.prepare("SELECT name FROM sqlite_master WHERE type='table'").all();
  console.log('📋 Tabelas encontradas:', tables.map(t => t.name).join(', '));
  
  db.close();
  console.log('✅ Teste concluído!');
} catch (error) {
  console.error('❌ Erro:', error.message);
}
```

**Rodar:**
```powershell
cd webapp
node test-db.js
```

---

## 🔧 Problemas Comuns e Soluções

### ❌ **Erro: Cannot find module 'better-sqlite3'**

```powershell
cd webapp
npm install better-sqlite3
```

### ❌ **Erro: ENOENT - pasta 'data' não existe**

```powershell
cd C:\Users\Kayke\Documents\github\macacolandia-bot
mkdir data
```

### ❌ **Erro: Permission denied**

```powershell
# Como Administrador
icacls data /grant Everyone:F /T
```

### ❌ **Erro: Port 3000 already in use**

```powershell
# Encontrar processo usando porta 3000
netstat -ano | findstr :3000

# Matar processo (substitua PID)
taskkill /PID <PID> /F

# Ou usar outra porta
$env:PORT=3001; npm run dev
```

### ❌ **Erro: bcrypt/bcryptjs - build failed**

```powershell
npm uninstall bcryptjs
npm install bcryptjs --save
npm rebuild
```

---

## 📝 Checklist de Debug

Quando tiver erro, siga esta ordem:

- [ ] 1. Ler o erro no terminal
- [ ] 2. Procurar por `[REGISTER]` ou `[AUTH-DB]` nos logs
- [ ] 3. Verificar se pasta `data/` existe
- [ ] 4. Verificar se arquivo `.db` foi criado
- [ ] 5. Testar conexão com banco (script acima)
- [ ] 6. Verificar Network tab no Chrome DevTools
- [ ] 7. Verificar se todas as dependências estão instaladas

---

## 🚀 Próximos Passos

### **Se funcionar localmente mas falhar no deploy:**

1. **Verificar variáveis de ambiente no Dokploy**
2. **Verificar se pasta `data/` tem permissões no servidor**
3. **Verificar logs do Docker/Dokploy**

### **Logs no Dokploy:**

```bash
# Via SSH no servidor
docker logs <container-id>

# Ou no painel do Dokploy
# Seção "Logs" do seu aplicativo
```

---

## 💡 Dicas

1. **Sempre rode `npm run dev` localmente primeiro**
2. **Leia os logs no terminal - eles mostram tudo!**
3. **Use console.log() para debug rápido**
4. **Use breakpoints no VS Code para debug avançado**
5. **Verifique o Network tab do Chrome para ver requisições**

---

## 📞 Mensagens de Log para Procurar

| Mensagem | Significado |
|----------|-------------|
| `[AUTH-DB] Criando diretório de dados` | Pasta sendo criada |
| `[AUTH-DB] Tentando conectar ao banco` | Iniciando conexão |
| `[AUTH-DB] Banco conectado` | Conexão OK |
| `[AUTH-DB] Tabelas inicializadas` | Setup completo |
| `[REGISTER] Nova solicitação` | Registro iniciado |
| `[REGISTER] Verificando se email já existe` | Checando duplicatas |
| `[REGISTER] Gerando hash da senha` | Hash em progresso |
| `[REGISTER] Criando registro pendente` | Salvando no DB |
| `[REGISTER] Registro concluído` | Sucesso! |
| `[AUTH-DB] Erro ao...` | ❌ Algo deu errado |

---

## ✅ Teste Rápido

```powershell
# 1. Instalar
cd C:\Users\Kayke\Documents\github\macacolandia-bot\webapp
npm install

# 2. Rodar
npm run dev

# 3. Abrir navegador
# http://localhost:3000/auth/register

# 4. Tentar registrar e VER O TERMINAL!
```

Os logs vão aparecer e você verá exatamente onde está o erro! 🎯
