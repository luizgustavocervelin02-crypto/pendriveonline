#!/usr/bin/env python3
"""
Otimizador de página para mobile - Remove bloqueios de renderização
"""
import re

def optimize_html():
    with open('index.html', 'r', encoding='utf-8') as f:
        html = f.read()

    print("Iniciando otimização mobile...")

    # 1. Remover Tailwind CDN (blocking render)
    html = re.sub(r'<script src="https://cdn\.tailwindcss\.com"></script>', '', html)
    print("✓ Tailwind CDN removido")

    # 2. Remover configuração inline do Tailwind
    html = re.sub(r'<script>\s*tailwind\.config = \{[^}]+\}\s*</script>', '', html)
    print("✓ Config Tailwind removida")

    # 3. Mover Facebook Pixel para async (não-crítico)
    html = html.replace(
        "!function (f, b, e, v, n, t, s)",
        "window.addEventListener('load',function(){!function (f, b, e, v, n, t, s)"
    )
    # Fechar a função após o último ponto e vírgula do pixel
    html = html.replace(
        "fbq('track', 'PageView');</script>",
        "fbq('track', 'PageView');}});</script>"
    )
    print("✓ Facebook Pixel movido para load event")

    # 4. Adicionar async ao Clarity
    html = html.replace(
        'y.parentNode.insertBefore(t, y); })(window',
        'y.parentNode.insertBefore(t, y); },2000); })(window'
    )

    # 5. Defer em scripts não-críticos
    html = html.replace(
        '<script src="https://cdn.utmify.com.br/scripts/utms/latest.js"',
        '<script defer src="https://cdn.utmify.com.br/scripts/utms/latest.js"'
    )
    print("✓ Scripts movidos para async/defer")

    # 6. Adicionar preload para imagens críticas
    preload_images = '''<link rel="preload" as="image" href="https://i.ibb.co/tMR4mJXt/1w1.jpg" fetchpriority="high">
<link rel="preload" as="image" href="assets/logo.png" fetchpriority="high">
<link rel="preload" as="image" href="assets/folders-list.jpg" fetchpriority="high">'''

    # Substituir preloads existentes
    html = re.sub(
        r'<link rel="preload"[^>]*fetchpriority="high"[^>]*>',
        '',
        html
    )
    html = html.replace(
        '<link rel="preconnect" href="https://fonts.googleapis.com">',
        preload_images + '\n  <link rel="preconnect" href="https://fonts.googleapis.com">'
    )
    print("✓ Preload de imagens otimizado")

    # 7. Carregar CSS crítico inline
    with open('critical.css', 'r', encoding='utf-8') as f:
        critical_css = f.read()

    critical_style = f'<style>{critical_css}</style>\n'
    html = html.replace('</head>', critical_style + '</head>')
    print("✓ CSS crítico injetado inline")

    # 8. Adicionar Tailwind CDN no final do body (non-blocking)
    tailwind_defer = '''<script defer src="https://cdn.tailwindcss.com"></script>
<script>window.addEventListener('DOMContentLoaded',function(){if(window.tailwind){tailwind.config={theme:{extend:{fontFamily:{sans:['Inter','sans-serif']}}}}}});</script>'''

    html = html.replace('</body>', tailwind_defer + '\n</body>')
    print("✓ Tailwind movido para final do body")

    # 9. Adicionar loading="lazy" em imagens não críticas (exceto hero)
    # Marcar primeira imagem como eager, resto lazy
    image_count = 0
    def replace_image_loading(match):
        nonlocal image_count
        image_count += 1
        img_tag = match.group(0)

        # Primeira 2 imagens (hero + folders) = eager
        if image_count <= 2:
            if 'loading=' not in img_tag:
                img_tag = img_tag.replace('<img', '<img loading="eager" fetchpriority="high"')
            return img_tag

        # Resto = lazy
        if 'loading="lazy"' not in img_tag:
            img_tag = re.sub(r'loading="[^"]*"', 'loading="lazy"', img_tag)
            if 'loading=' not in img_tag:
                img_tag = img_tag.replace('<img', '<img loading="lazy"')

        # Remover fetchpriority de imagens lazy
        img_tag = re.sub(r'fetchpriority="[^"]*"\s*', '', img_tag)
        return img_tag

    html = re.sub(r'<img[^>]*>', replace_image_loading, html)
    print(f"✓ Loading otimizado em {image_count} imagens")

    # 10. Adicionar dimensions às imagens sem width/height
    html = html.replace(
        '<img src="https://i.ibb.co/tMR4mJXt/1w1.jpg"',
        '<img width="1080" height="1920" src="https://i.ibb.co/tMR4mJXt/1w1.jpg"'
    )
    print("✓ Dimensões adicionadas às imagens")

    # 11. Minificar espaços em branco extras
    # html = re.sub(r'\s{2,}', ' ', html)
    # html = re.sub(r'>\s+<', '><', html)
    # print("✓ HTML minificado")

    # Salvar arquivo otimizado
    with open('index_optimized.html', 'w', encoding='utf-8') as f:
        f.write(html)

    print("\n✅ Otimização completa! Arquivo salvo em: index_optimized.html")
    print("\nMelhorias aplicadas:")
    print("  • Tailwind CDN movido para final (non-blocking)")
    print("  • Facebook Pixel carrega após load event")
    print("  • CSS crítico inline no head")
    print("  • Preload de imagens críticas")
    print("  • Lazy loading em imagens não-críticas")
    print("  • Scripts com async/defer")
    print("  • Dimensões explícitas em imagens")

if __name__ == '__main__':
    optimize_html()
