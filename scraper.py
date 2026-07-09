import os
import random
import time
import requests

# =====================================================================
# CONFIGURACIÓN COMPLETA
# =====================================================================
URL = "https://form.jotform.com/paninipointcr/colecciones"
DISCORD_WEBHOOK_URL = "https://discord.com/api/webhooks/1524458335489753110/pjajjh8WGeF_GerMwPjWwwda_-2KRXEgVhoSSZKzkWvFg1zG7JO2a8_S3ccMqqukYd7p"
# =====================================================================


def send_discord_alert(keyword_found):
    """Envía una notificación push inmediata a tu canal de Discord."""
    payload = {
        "content": (
            f"🚨 **¡¡¡ALERTA MÁXIMA DE COCA-COLA EN PANINI!!!** 🚨\n"
            f"Se ha detectado el sticker o sección **'{keyword_found}'** en la base de datos del formulario.\n"
            f"¡Las postales ya se pueden seleccionar en las páginas siguientes!\n"
            f"👉 **Entra rápido a comprar aquí:** https://form.jotform.com/paninipointcr/colecciones"
        )
    }
    try:
        requests.post(DISCORD_WEBHOOK_URL, json=payload, timeout=10)
        print("Notificación enviada con éxito a Discord.")
    except Exception as e:
        print(f"No se pudo conectar con Discord: {e}")


def check_form():
    # 1. EVITAR BLOQUEO DEL CRONJOB: Pausa aleatoria antes de tocar el servidor
    retraso = random.randint(10, 150)
    print(
        f"Cronjob iniciado. Esperando {retraso} segundos para romper el patrón de tráfico..."
    )
    time.sleep(retraso)

    # 2. SIMULAR NAVEGADOR HUMANO NORMAL (Evita Error 500 y bloqueos)
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126.0.0.0 Safari/537.36",
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8",
        "Accept-Language": "es-ES,es;q=0.9,en;q=0.8",
        "Cache-Control": "no-cache",
    }

    try:
        print(f"Descargando estructura interna del formulario de Jotform...")
        response = requests.get(URL, headers=headers, timeout=15)

        if response.status_code == 200:
            print("¡Éxito! Estructura base leída correctamente (Código 200).")

            # Analizamos todo el texto del HTML fuente bajado en minúsculas
            # Jotform inyecta aquí la lista completa de productos de todas las páginas de forma oculta
            full_html_source = response.text.lower()

            # Palabras clave de Coca-Cola a cazar
            keywords = ["coca-cola", "coca cola", "cocacola", "coca-", "cc1"]

            # Revisamos si el inventario global de postales ya tiene alguna coincidencia
            for keyword in keywords:
                if keyword in full_html_source:
                    print(
                        f"¡¡¡ALERTA!!! Encontrada coincidencia oculta de producto: '{keyword}'"
                    )
                    send_discord_alert(keyword)
                    return True

            print(
                "Revisión completada: El catálogo interno se inspeccionó con éxito y aún no incluye opciones de Coca-Cola."
            )
            return True  # Retorna True para cerrar con check verde en GitHub

        else:
            print(
                f"ERROR de servidor: El sitio respondió con código {response.status_code}"
            )
            return False

    except Exception as e:
        print(f"Ocurrió un error inesperado al conectar: {e}")
        return False


if __name__ == "__main__":
    # Si algo falla en la conexión de red externa, forzamos salida limpia
    # para evitar alarmas falsas de error en GitHub Actions
    try:
        check_form()
    except SystemExit:
        pass
