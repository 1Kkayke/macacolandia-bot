"""
Script de teste para verificar se o YouTube está funcionando com cookies
"""

import yt_dlp
from pathlib import Path

def test_youtube():
    print("=" * 60)
    print("   TESTE DE CONEXÃO COM YOUTUBE")
    print("=" * 60)
    print()
    
    # Detectar navegador com cookies
    browser = None
    try:
        import browser_cookie3
        for browser_name in ['chrome', 'edge', 'firefox']:
            try:
                browser_func = getattr(browser_cookie3, browser_name, None)
                if browser_func:
                    list(browser_func(domain_name='.youtube.com'))
                    browser = browser_name
                    print(f"✅ Cookies encontrados no {browser_name.title()}")
                    break
            except Exception as e:
                print(f"❌ {browser_name.title()}: {str(e)[:50]}")
    except Exception as e:
        print(f"❌ Erro ao importar browser_cookie3: {e}")
    
    print()
    print("-" * 60)
    print("Testando download de vídeo do YouTube...")
    print("-" * 60)
    
    # Configuração do yt-dlp
    ydl_opts = {
        'format': 'bestaudio/best',
        'quiet': False,
        'no_warnings': False,
        'extract_flat': False,
        'default_search': 'ytsearch',
        'cookiesfrombrowser': (browser,) if browser else None,
        'extractor_args': {
            'youtube': {
                'player_client': ['android', 'web'],
                'skip': ['hls', 'dash'],
            }
        },
    }
    
    # URLs de teste
    test_queries = [
        'ytsearch:never gonna give you up',
        'ytsearch:despacito',
        'https://www.youtube.com/watch?v=dQw4w9WgXcQ',
    ]
    
    for i, query in enumerate(test_queries, 1):
        print(f"\n📝 Teste {i}/3: {query}")
        try:
            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                info = ydl.extract_info(query, download=False)
                
                if 'entries' in info:
                    info = info['entries'][0]
                
                print(f"✅ SUCESSO!")
                print(f"   Título: {info.get('title', 'N/A')}")
                print(f"   Duração: {info.get('duration', 0)}s")
                print(f"   URL: {info.get('webpage_url', 'N/A')}")
                
        except Exception as e:
            print(f"❌ FALHOU: {str(e)[:200]}")
    
    print()
    print("=" * 60)
    print("   TESTE CONCLUÍDO")
    print("=" * 60)
    
    if browser:
        print(f"\n✅ Bot configurado para usar cookies do {browser.title()}")
        print("✅ Reinicie o bot para aplicar as mudanças")
    else:
        print("\n⚠️  Nenhum navegador com cookies encontrado")
        print("📝 Faça login no YouTube pelo Chrome ou Edge e tente novamente")

if __name__ == "__main__":
    test_youtube()
    input("\nPressione ENTER para fechar...")
