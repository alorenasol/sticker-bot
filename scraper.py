import os
import random
import time
import requests
from bs4 import BeautifulSoup

# =====================================================================
# CONFIGURACIÓN DEL ENLACE DE JOTFORM (Ya configurado para ti)
# =====================================================================
URL = "https://form.jotform.com/paninipointcr/colecciones"
# =====================================================================


def check_form():
    # 1. EVITAR BLOQUEO DEL CRONJOB: Espera un tiempo al azar antes de hacer la petición.
    # Elige un número de segundos aleatorio entre 10 y 150 (hasta 2 minutos y medio).
    retraso = random.randint(10, 150)
    print(
        f"Cronjob iniciado. Esperando {retraso} segundos para romper el patrón de tráfico..."
    )
    time.sleep(retraso)

    # 2. SIMULAR NAVEGADOR HUMANO: Encabezados modernos para evadir firewalls.
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126.0.0.0 Safari/537.36",
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8",
        "Accept-Language": "es-ES,es;q=0.9,en;q=0.8",
        "Cache-Control": "no-cache",
        "Pragma": "no-cache",
    }

    try:
        print(f"Conectando a la página: {URL}")
        response = requests.get(URL, headers=headers, timeout=15)

        # Verificar si la página respondió correctamente
        if response.status_code == 200:
            print("¡Éxito! Conexión establecida con código 200.")

            # Extraer el texto de la página y pasarlo a minúsculas
            soup = BeautifulSoup(response.text, "html.parser")
            page_text = soup.get_text().lower()

            # Palabras clave a buscar en el formulario
            keywords = ["coca-cola", "coca cola", "cocacola", "coca-", "cc1"]

            # Buscar si alguna palabra clave está en el texto
            for keyword in keywords:
                if keyword in page_text:
                    print(f"¡¡¡ALERTA!!! Se encontró la palabra: '{keyword}'")

                    # =========================================================
                    # HISTORIAL E IMPRESIÓN GRANDE EN GITHUB ACTIONS
                    # =========================================================
                    print("*" * 50)
                    print("  LOS STICKERS DE COCA-COLA YA ESTÁN DISPONIBLES  ")
                    print("*" * 50)

                    return True

            print("Revisión completada: Aún no están disponibles los stickers.")
            return False

        else:
            # Si el servidor responde con error 500 u otro, te lo avisará aquí
            print(
                f"ERROR: El servidor respondió con código de estado {response.status_code}"
            )
            return False

    except Exception as e:
        print(f"Ocurrió un error inesperado al conectar: {e}")
        return False


# Ejecutar la función principal una sola vez (ideal para GitHub Actions)
if __name__ == "__main__":
    check_form()

