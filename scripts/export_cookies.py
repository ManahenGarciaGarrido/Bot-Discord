#!/usr/bin/env python3
"""
Script para exportar cookies de YouTube desde tu navegador local

Este script extrae las cookies de YouTube de tu navegador y las guarda
en un archivo cookies.txt que puedes subir a tu servidor.

REQUISITOS:
- Debes estar en tu PC local (no en el servidor)
- Debes tener un navegador instalado
- Debes estar autenticado en youtube.com en ese navegador

USO:
    python scripts/export_cookies.py [navegador]

EJEMPLOS:
    python scripts/export_cookies.py chrome
    python scripts/export_cookies.py firefox
    python scripts/export_cookies.py edge
"""

import sys
import os

try:
    import browser_cookie3
    HAS_BROWSER_COOKIE3 = True
except ImportError:
    HAS_BROWSER_COOKIE3 = False

try:
    from http.cookiejar import MozillaCookieJar
    HAS_COOKIEJAR = True
except ImportError:
    HAS_COOKIEJAR = False


def export_cookies_method_1(browser_name):
    """
    Método 1: Usar browser_cookie3 (más simple pero requiere instalación)
    """
    if not HAS_BROWSER_COOKIE3:
        print("❌ browser_cookie3 no está instalado")
        print("   Instálalo con: pip install browser-cookie3")
        return False

    print(f"🔍 Intentando extraer cookies de {browser_name}...")

    try:
        # Obtener cookies según el navegador
        if browser_name == 'chrome':
            cookies = browser_cookie3.chrome(domain_name='youtube.com')
        elif browser_name == 'firefox':
            cookies = browser_cookie3.firefox(domain_name='youtube.com')
        elif browser_name == 'edge':
            cookies = browser_cookie3.edge(domain_name='youtube.com')
        elif browser_name == 'brave':
            cookies = browser_cookie3.brave(domain_name='youtube.com')
        elif browser_name == 'opera':
            cookies = browser_cookie3.opera(domain_name='youtube.com')
        else:
            print(f"❌ Navegador no soportado: {browser_name}")
            print("   Navegadores soportados: chrome, firefox, edge, brave, opera")
            return False

        # Guardar cookies en formato Netscape
        output_file = 'cookies.txt'

        # Crear CookieJar y guardar
        cj = MozillaCookieJar(output_file)
        for cookie in cookies:
            cj.set_cookie(cookie)

        cj.save(ignore_discard=True, ignore_expires=True)

        print(f"✅ Cookies exportadas exitosamente a: {output_file}")
        print(f"📁 Ruta completa: {os.path.abspath(output_file)}")
        print()
        print("📋 Próximos pasos:")
        print("   1. Sube el archivo cookies.txt a tu servidor")
        print("   2. En tu servidor, añade a .env:")
        print("      YOUTUBE_COOKIES_FILE=/path/to/cookies.txt")
        print("   3. Reinicia el bot")

        return True

    except Exception as e:
        print(f"❌ Error extrayendo cookies: {e}")
        return False


def export_cookies_method_2():
    """
    Método 2: Usar extensión de navegador (manual pero más confiable)
    """
    print()
    print("=" * 70)
    print("🔧 MÉTODO ALTERNATIVO: Usar extensión de navegador")
    print("=" * 70)
    print()
    print("Este método es más confiable y funciona en todos los navegadores.")
    print()
    print("📋 PASOS:")
    print()
    print("1️⃣  Instala una extensión para exportar cookies:")
    print()
    print("   Para Chrome/Edge/Brave:")
    print("   https://chrome.google.com/webstore/detail/editthiscookie/")
    print()
    print("   Para Firefox:")
    print("   https://addons.mozilla.org/firefox/addon/cookies-txt/")
    print()
    print("2️⃣  Ve a youtube.com y asegúrate de estar autenticado")
    print()
    print("3️⃣  Haz clic en la extensión de cookies")
    print()
    print("4️⃣  Exporta las cookies en formato 'Netscape' o 'cookies.txt'")
    print()
    print("5️⃣  Guarda el archivo como 'cookies.txt'")
    print()
    print("6️⃣  Sube el archivo a tu servidor y configura en .env:")
    print("      YOUTUBE_COOKIES_FILE=/path/to/cookies.txt")
    print()
    print("=" * 70)


def main():
    print()
    print("=" * 70)
    print("🍪 EXPORTADOR DE COOKIES DE YOUTUBE")
    print("=" * 70)
    print()

    # Verificar si se especificó un navegador
    if len(sys.argv) > 1:
        browser_name = sys.argv[1].lower()
    else:
        print("💡 USO: python scripts/export_cookies.py [navegador]")
        print()
        print("   Navegadores disponibles:")
        print("   - chrome")
        print("   - firefox")
        print("   - edge")
        print("   - brave")
        print("   - opera")
        print()
        browser_name = input("Escribe el nombre de tu navegador: ").lower().strip()
        print()

    # Intentar método 1 (automático)
    if HAS_BROWSER_COOKIE3 and HAS_COOKIEJAR:
        success = export_cookies_method_1(browser_name)
        if success:
            return
    else:
        print("⚠️  Dependencias no instaladas para exportación automática")
        print()
        print("Para instalarlo:")
        print("   pip install browser-cookie3")
        print()

    # Si falla el método 1, mostrar método 2 (manual)
    export_cookies_method_2()


if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        print()
        print("❌ Cancelado por el usuario")
        sys.exit(1)
    except Exception as e:
        print()
        print(f"❌ Error inesperado: {e}")
        sys.exit(1)
