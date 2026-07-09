import os
import random
import time
import requests
from bs4 import BeautifulSoup

# =====================================================================
# CONFIGURACIÓN COMPLETA
# =====================================================================
URL = "https://form.jotform.com/paninipointcr/colecciones"
DISCORD_WEBHOOK_URL = "https://discord.com/api/webhooks/1524458335489753110/pjajjh8WGeF_GerMwPjWwwda_-2KRXEgVhoSSZKzkWvFg1zG7JO2a8_S3ccMqqukYd7p"
# =====================================================================


def send_discord_alert(keyword_found):
    """Envía una notificación inmediata a tu canal de Discord."""
    payload = {
        "content": (
            f"🚨 **¡¡¡ALERTA MÁXIMA DE COCA-COLA!!!** 🚨\n"
            f"Se ha detectado la opción **'{keyword_found}'** dentro del catálogo del Mundial 2026.\n"
            f"¡Las postales ya están activas en el formulario!\n"
            f"👉 **Entra de inmediato a comprar aquí:** {URL}"
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

    # 2. SIMULAR CLICS HUMANOS (Datos de la primera página)
    # Selecciona automáticamente 'Lincoln Plaza' y la colección 'Mundial 2026'
    form_data = {
        "q3_dondeRetira": "Panini Point - Lincoln Plaza",
        "q5_coleccionesPanini[0]": "MUNDIAL 2026",
        "simple_spc": "241085025732854-241085025732854",
        "formID": "241085025732854",
    }

    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126.0.0.0 Safari/537.36",
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8",
        "Accept-Language": "es-ES,es;q=0.9,en;q=0.8",
        "Origin": "https://jotform.com",
        "Referer": URL,
    }

    try:
        print("Simulando selección de Lincoln Plaza y Mundial 2026...")
        # Enviamos un HTTP POST para avanzar de página forzadamente
        response = requests.post(URL, data=form_data, headers=headers, timeout=15)

        if response.status_code == 200:
            print("¡Éxito! Avanzado a la página de stickers del Mundial 2026.")

            soup = BeautifulSoup(response.text, "html.parser")
            page_text = soup.get_text().lower()

            # Palabras clave a rastrear
            keywords = ["coca-cola", "coca cola", "cocacola", "coca-", "cc1"]

            for keyword in keywords:
                if keyword in page_text:
                    print(f"¡¡¡ALERTA!!! Encontrado: '{keyword}'")
                    send_discord_alert(keyword)
                    return True

            print(
                "Revisión completada: Se ingresó al catálogo del Mundial 2026 con éxito, pero aún no hay opciones de Coca-Cola."
            )
            return False

        else:
            print(
                f"ERROR: El servidor de Jotform respondió con código {response.status_code}"
            )
            return False

    except Exception as e:
        print(f"Ocurrió un error inesperado al conectar: {e}")
        return False


if __name__ == "__main__":
    check_form()
