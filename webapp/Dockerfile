# Stage 1: Dependencies
FROM node:20-alpine AS deps
WORKDIR /app

# Install Python and build tools for better-sqlite3
RUN apk add --no-cache python3 make g++

# Copy package files
COPY package.json package-lock.json* ./

# Install dependencies (with fallback to npm install if ci fails)
RUN npm ci || npm install

# Stage 2: Builder
FROM node:20-alpine AS builder
WORKDIR /app

# Copy dependencies from deps stage
COPY --from=deps /app/node_modules ./node_modules
COPY . .

# Build the Next.js application
RUN npm run build

# Stage 3: Runner
FROM node:20-alpine AS runner
WORKDIR /app

ENV NODE_ENV=production

# Install Python and build tools for better-sqlite3 (needed for ensure-admin)
RUN apk add --no-cache python3 make g++

# Add non-root user for security
RUN addgroup --system --gid 1001 nodejs
RUN adduser --system --uid 1001 nextjs

# Copy necessary files from builder
COPY --from=builder /app/public ./public
COPY --from=builder /app/.next/standalone ./
COPY --from=builder /app/.next/static ./.next/static

# Copy scripts directory and node_modules (for ensure-admin dependencies)
COPY --from=deps /app/node_modules ./node_modules
COPY --from=builder /app/scripts ./scripts
COPY --from=builder /app/package.json ./package.json

# Create data directory for database
RUN mkdir -p /app/data && chown -R nextjs:nodejs /app

# Create entrypoint script
RUN echo '#!/bin/sh\n\
echo "🔧 Inicializando aplicação..."\n\
if [ -n "$ADMIN_PASSWORD" ]; then\n\
  echo "🔐 Garantindo admin..."\n\
  node scripts/ensure-admin.js || echo "⚠️  Aviso: Erro ao garantir admin"\n\
else\n\
  echo "⚠️  ADMIN_PASSWORD não configurado - pulando ensure-admin"\n\
fi\n\
echo "🚀 Iniciando servidor..."\n\
exec node server.js' > /app/entrypoint.sh && \
    chmod +x /app/entrypoint.sh && \
    chown nextjs:nodejs /app/entrypoint.sh

USER nextjs

EXPOSE 3000

ENV PORT=3000
ENV HOSTNAME="0.0.0.0"

# Start the application with entrypoint
CMD ["/app/entrypoint.sh"]
