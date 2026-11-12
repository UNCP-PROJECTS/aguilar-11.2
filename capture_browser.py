import os
import time
import subprocess
import shutil
from playwright.sync_api import sync_playwright

BASE_DIR = r"C:\Users\USUARIO\Documents\!UNCP-DESARROLLO\aguilar-11.2"
ASSETS_DIR = os.path.join(BASE_DIR, "assets")
INFORME_ASSETS_DIR = os.path.join(BASE_DIR, "informe", "assets")
PROYECTO_DIR = os.path.join(BASE_DIR, "proyecto")
PROYECTO_ASSETS_DIR = os.path.join(PROYECTO_DIR, "assets")
PYTHON_EXE = os.path.join(PROYECTO_DIR, ".venv", "Scripts", "python.exe")

os.makedirs(ASSETS_DIR, exist_ok=True)
os.makedirs(INFORME_ASSETS_DIR, exist_ok=True)
os.makedirs(PROYECTO_ASSETS_DIR, exist_ok=True)

def save_multilocation(src_path, filename):
    for d in [ASSETS_DIR, INFORME_ASSETS_DIR, PROYECTO_ASSETS_DIR]:
        dest = os.path.join(d, filename)
        shutil.copy(src_path, dest)
    print(f"[OK] Captura de interfaz guardada: {filename}")

def capture():
    server_process = subprocess.Popen(
        [PYTHON_EXE, "manage.py", "runserver", "127.0.0.1:8000", "--noreload"],
        cwd=PROYECTO_DIR,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE
    )
    time.sleep(2.5)

    try:
        with sync_playwright() as p:
            browser = p.chromium.launch(headless=True)
            context = browser.new_context(viewport={'width': 1280, 'height': 820}, device_scale_factor=1.5)
            page = context.new_page()

            # 1. Home FBV
            page.goto("http://127.0.0.1:8000/")
            page.wait_for_load_state("networkidle")
            time.sleep(1)
            tmp1 = os.path.join(ASSETS_DIR, "_tmp_home.png")
            page.screenshot(path=tmp1)
            save_multilocation(tmp1, "interfaz_home_fbv.png")
            if os.path.exists(tmp1): os.remove(tmp1)

            # 2. Catalogo CBV
            page.goto("http://127.0.0.1:8000/catalogo/")
            page.wait_for_load_state("networkidle")
            time.sleep(1)
            tmp2 = os.path.join(ASSETS_DIR, "_tmp_cat.png")
            page.screenshot(path=tmp2)
            save_multilocation(tmp2, "interfaz_catalogo_cbv.png")
            if os.path.exists(tmp2): os.remove(tmp2)

            # 3. Catalogo Filtrado
            page.goto("http://127.0.0.1:8000/catalogo/?categoria=Perif%C3%A9ricos")
            page.wait_for_load_state("networkidle")
            time.sleep(1)
            tmp3 = os.path.join(ASSETS_DIR, "_tmp_filt.png")
            page.screenshot(path=tmp3)
            save_multilocation(tmp3, "interfaz_catalogo_filtrado.png")
            if os.path.exists(tmp3): os.remove(tmp3)

            browser.close()
    finally:
        server_process.terminate()
        server_process.wait()
        print("[OK] Servidor Django detenido.")

if __name__ == '__main__':
    capture()
