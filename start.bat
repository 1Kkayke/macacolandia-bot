@echo off
chcp 65001 >nul
echo 🎵 Iniciando Bot de Música Macacolândia...
echo.

REM Check if .env file exists
if not exist .env (
    echo ❌ Erro: Arquivo .env não encontrado!
    echo 📝 Crie um arquivo .env baseado no .env.example
    echo.
    echo Exemplo:
    echo   copy .env.example .env
    echo   notepad .env  :: Edite e adicione seu token
    pause
    exit /b 1
)

REM Check if Python is installed
python --version >nul 2>&1
if %errorlevel% neq 0 (
    echo ❌ Erro: Python 3 não está instalado!
    echo Por favor, instale o Python 3.8 ou superior
    pause
    exit /b 1
)

REM Check if FFmpeg is installed
ffmpeg -version >nul 2>&1
if %errorlevel% neq 0 (
    echo ⚠️ Aviso: FFmpeg não está instalado!
    echo O bot precisa do FFmpeg para funcionar corretamente
    echo.
    echo Instale o FFmpeg:
    echo   Baixe de ffmpeg.org e adicione ao PATH
    echo.
    pause
)

REM Check if dependencies are installed
echo 📦 Verificando dependências...
python -c "import discord" 2>nul
if %errorlevel% neq 0 (
    echo 📥 Instalando dependências...
    pip install -r requirements.txt
    if %errorlevel% neq 0 (
        echo ❌ Erro ao instalar dependências!
        pause
        exit /b 1
    )
)

echo ✅ Todas as verificações passaram!
echo 🚀 Iniciando o bot...
echo.

REM Run the bot
python bot.py
pause
