#!/usr/bin/env bash

# Macacolândia Music Bot Startup Script

echo "🎵 Iniciando Bot de Música Macacolândia..."
echo ""

# Check if .env file exists
if [ ! -f .env ]; then
    echo "❌ Erro: Arquivo .env não encontrado!"
    echo "📝 Crie um arquivo .env baseado no .env.example"
    echo ""
    echo "Exemplo:"
    echo "  cp .env.example .env"
    echo "  nano .env  # Edite e adicione seu token"
    exit 1
fi

# Check if Python is installed
if ! command -v python3 &> /dev/null; then
    echo "❌ Erro: Python 3 não está instalado!"
    echo "Por favor, instale o Python 3.8 ou superior"
    exit 1
fi

# Check if FFmpeg is installed
if ! command -v ffmpeg &> /dev/null; then
    echo "⚠️ Aviso: FFmpeg não está instalado!"
    echo "O bot precisa do FFmpeg para funcionar corretamente"
    echo ""
    echo "Instale o FFmpeg:"
    echo "  Ubuntu/Debian: sudo apt install ffmpeg"
    echo "  macOS: brew install ffmpeg"
    echo "  Windows: Baixe de ffmpeg.org"
    echo ""
    read -p "Continuar mesmo assim? (s/N) " -n 1 -r
    echo
    if [[ ! $REPLY =~ ^[Ss]$ ]]; then
        exit 1
    fi
fi

# Check if dependencies are installed
echo "📦 Verificando dependências..."
if ! python3 -c "import discord" 2>/dev/null; then
    echo "📥 Instalando dependências..."
    pip3 install -r requirements.txt
    if [ $? -ne 0 ]; then
        echo "❌ Erro ao instalar dependências!"
        exit 1
    fi
fi

echo "✅ Todas as verificações passaram!"
echo "🚀 Iniciando o bot..."
echo ""

# Run the bot
python3 bot.py
