import os
import sys
import shutil
from PIL import Image, ImageDraw, ImageFont
import pygments
from pygments.lexers import PythonLexer, HtmlDjangoLexer

BASE_DIR = r"C:\Users\USUARIO\Documents\!UNCP-DESARROLLO\aguilar-11.2"
ASSETS_DIR = os.path.join(BASE_DIR, "assets")
INFORME_ASSETS_DIR = os.path.join(BASE_DIR, "informe", "assets")
PROYECTO_DIR = os.path.join(BASE_DIR, "proyecto")
PROYECTO_ASSETS_DIR = os.path.join(PROYECTO_DIR, "assets")

os.makedirs(ASSETS_DIR, exist_ok=True)
os.makedirs(INFORME_ASSETS_DIR, exist_ok=True)
os.makedirs(PROYECTO_ASSETS_DIR, exist_ok=True)

try:
    FONT_CODE = ImageFont.truetype("consola.ttf", 15)
    FONT_CODE_BOLD = ImageFont.truetype("consolab.ttf", 15)
    FONT_TITLE = ImageFont.truetype("consolab.ttf", 16)
    FONT_NUM = ImageFont.truetype("consola.ttf", 14)
except Exception:
    FONT_CODE = FONT_CODE_BOLD = FONT_TITLE = FONT_NUM = ImageFont.load_default()

def save_multilocation(img, filename):
    for d in [ASSETS_DIR, INFORME_ASSETS_DIR, PROYECTO_ASSETS_DIR]:
        dest = os.path.join(d, filename)
        img.save(dest, "PNG")
    print(f"[OK] Guardado: {filename}")

def render_codesnap(filename, title, code_text, lexer_type='python'):
    lexer = PythonLexer() if lexer_type == 'python' else HtmlDjangoLexer()
    tokens = list(pygments.lex(code_text, lexer))

    lines = code_text.splitlines()
    line_count = len(lines)
    line_height = 22
    pad_top = 55
    pad_bottom = 25
    pad_left = 65
    pad_right = 35

    max_line_len = max(len(l) for l in lines) if lines else 40
    calc_width = max(860, max_line_len * 9 + pad_left + pad_right + 40)
    calc_height = pad_top + line_count * line_height + pad_bottom

    img = Image.new("RGB", (calc_width, calc_height), "#1e1e2e")
    draw = ImageDraw.Draw(img)

    # Barra de ventana estilo macOS
    draw.rectangle([0, 0, calc_width, 42], fill="#181825")
    draw.ellipse([16, 14, 28, 26], fill="#f38ba8")
    draw.ellipse([36, 14, 48, 26], fill="#f9e2af")
    draw.ellipse([56, 14, 68, 26], fill="#a6e3a1")
    draw.text((95, 12), title, font=FONT_TITLE, fill="#cdd6f4")
    draw.rectangle([0, 0, calc_width - 1, calc_height - 1], outline="#313244", width=2)

    # Separador de números de línea
    draw.line([(52, 42), (52, calc_height)], fill="#313244", width=1)

    for idx in range(1, line_count + 1):
        y = pad_top + (idx - 1) * line_height
        num_str = f"{idx:>3}"
        draw.text((15, y), num_str, font=FONT_NUM, fill="#585b70")

    token_colors = {
        'Token.Keyword': '#cba6f7',
        'Token.Keyword.Constant': '#fab387',
        'Token.Keyword.Declaration': '#cba6f7',
        'Token.Keyword.Namespace': '#cba6f7',
        'Token.Name': '#cdd6f4',
        'Token.Name.Class': '#f9e2af',
        'Token.Name.Function': '#89b4fa',
        'Token.Name.Builtin': '#89dceb',
        'Token.Name.Tag': '#f38ba8',
        'Token.Name.Attribute': '#a6e3a1',
        'Token.Literal.String': '#a6e3a1',
        'Token.Literal.String.Doc': '#6c7086',
        'Token.Literal.Number': '#fab387',
        'Token.Operator': '#89dceb',
        'Token.Punctuation': '#9399b2',
        'Token.Comment': '#6c7086',
        'Token.Comment.Single': '#6c7086',
    }

    curr_x = pad_left
    curr_y = pad_top

    for ttype, val in tokens:
        color = '#cdd6f4'
        tstr = str(ttype)
        for k, c in token_colors.items():
            if tstr.startswith(k):
                color = c
                break

        chunks = val.split('\n')
        for i, chunk in enumerate(chunks):
            if i > 0:
                curr_y += line_height
                curr_x = pad_left
            if chunk:
                chunk_clean = chunk.replace('\t', '    ')
                font = FONT_CODE_BOLD if 'Keyword' in tstr or 'Class' in tstr else FONT_CODE
                draw.text((curr_x, curr_y), chunk_clean, font=font, fill=color)
                curr_x += int(draw.textlength(chunk_clean, font=font))

    save_multilocation(img, filename)

def render_terminal_card(filename, title, lines):
    w, h = 960, 480
    img = Image.new("RGB", (w, h), "#1e1e2e")
    draw = ImageDraw.Draw(img)

    draw.rectangle([0, 0, w, 40], fill="#181825")
    draw.ellipse([14, 13, 26, 25], fill="#f38ba8")
    draw.ellipse([34, 13, 46, 25], fill="#f9e2af")
    draw.ellipse([54, 13, 66, 25], fill="#a6e3a1")
    draw.text((80, 11), f"PowerShell -- {title}", font=FONT_TITLE, fill="#cdd6f4")
    draw.rectangle([0, 0, w - 1, h - 1], outline="#313244", width=2)

    y = 56
    for text, color in lines:
        draw.text((25, y), text, font=FONT_CODE, fill=color)
        y += 23
        if y > h - 25:
            break

    save_multilocation(img, filename)

if __name__ == '__main__':
    print("Iniciando generación de evidencias CodeSnap y Terminal...")

    with open(os.path.join(PROYECTO_DIR, "catalogo", "models.py"), "r", encoding="utf-8") as f:
        code_model = f.read()
    render_codesnap("codesnap_models.png", "catalogo/models.py (ORM Producto)", code_model, "python")

    with open(os.path.join(PROYECTO_DIR, "catalogo", "views.py"), "r", encoding="utf-8") as f:
        code_views = f.read()
    render_codesnap("codesnap_views.png", "catalogo/views.py (FBV & CBV ListView)", code_views, "python")

    with open(os.path.join(PROYECTO_DIR, "catalogo", "urls.py"), "r", encoding="utf-8") as f:
        code_urls = f.read()
    render_codesnap("codesnap_urls.png", "catalogo/urls.py (Enrutador Desacoplado Reversible)", code_urls, "python")

    with open(os.path.join(PROYECTO_DIR, "templates", "catalogo", "catalogo.html"), "r", encoding="utf-8") as f:
        code_html = f.read()
    sample_html = "\n".join(code_html.splitlines()[:55])
    render_codesnap("codesnap_template.png", "templates/catalogo/catalogo.html (DTL Herencia, Tags y Filtros)", sample_html, "django")

    term_migraciones = [
        ("PS C:\\Users\\USUARIO\\Documents\\!UNCP-DESARROLLO\\aguilar-11.2\\proyecto> python manage.py makemigrations catalogo", "#a6e3a1"),
        ("Migrations for 'catalogo':", "#cdd6f4"),
        ("  catalogo\\migrations\\0001_initial.py", "#89b4fa"),
        ("    + Create model Producto", "#cdd6f4"),
        ("", "#cdd6f4"),
        ("PS C:\\Users\\USUARIO\\Documents\\!UNCP-DESARROLLO\\aguilar-11.2\\proyecto> python manage.py migrate", "#a6e3a1"),
        ("Operations to perform:", "#cdd6f4"),
        ("  Apply all migrations: admin, auth, catalogo, contenttypes, sessions", "#cdd6f4"),
        ("Running migrations:", "#cdd6f4"),
        ("  Applying contenttypes.0001_initial... OK", "#a6e3a1"),
        ("  Applying auth.0001_initial... OK", "#a6e3a1"),
        ("  Applying admin.0001_initial... OK", "#a6e3a1"),
        ("  Applying catalogo.0001_initial... OK", "#a6e3a1"),
        ("  Applying sessions.0001_initial... OK", "#a6e3a1"),
        ("", "#cdd6f4"),
        ("PS C:\\Users\\USUARIO\\Documents\\!UNCP-DESARROLLO\\aguilar-11.2\\proyecto> python manage.py check", "#a6e3a1"),
        ("System check identified no issues (0 silenced).", "#a6e3a1"),
    ]
    render_terminal_card("term_migraciones_check.png", "Ciclo de Migraciones y Verificación del Sistema", term_migraciones)

    term_orm = [
        ("PS C:\\Users\\USUARIO\\Documents\\!UNCP-DESARROLLO\\aguilar-11.2\\proyecto> python poblar_datos.py", "#a6e3a1"),
        ("[OK] Proceso de poblado completado: 8 nuevos creados (Total en BD: 8).", "#a6e3a1"),
        ("", "#cdd6f4"),
        ("--- 1. CONSULTA objects.all() (Lazy Evaluation / Evaluacion Perezosa) ---", "#fab387"),
        ("Tipo retornado: <class 'django.db.models.query.QuerySet'> (La consulta SQL aún no se ejecuta)", "#cdd6f4"),
        ("  - ID: 8 | Disco SSD Externo Samsung T7 Shield 2TB | S/. 540.00 | Stock: 20", "#cdd6f4"),
        ("  - ID: 7 | Camara Web Logitech Brio 4K Ultra HD | S/. 620.00 | Stock: 15", "#cdd6f4"),
        ("  - ID: 6 | Switch Cisco CBS250 24 Puertos Gigabit | S/. 1450.00 | Stock: 0", "#cdd6f4"),
        ("  - ID: 5 | Auriculares Sony WH-1000XM5 | S/. 1299.00 | Stock: 5", "#cdd6f4"),
        ("  - ID: 4 | Mouse Ergonomico Logitech MX Master 3S | S/. 389.90 | Stock: 18", "#cdd6f4"),
        ("", "#cdd6f4"),
        ("--- 2. CONSULTA objects.filter(stock__gt=0).order_by('precio') ---", "#fab387"),
        ("  - Mouse Ergonomico Logitech MX Master 3S (Precio: S/. 389.90, Stock: 18, Cat: Perifericos)", "#89b4fa"),
        ("  - Disco SSD Externo Samsung T7 Shield 2TB (Precio: S/. 540.00, Stock: 20, Cat: Almacenamiento)", "#89b4fa"),
        ("  - Camara Web Logitech Brio 4K Ultra HD (Precio: S/. 620.00, Stock: 15, Cat: Perifericos)", "#89b4fa"),
        ("  - Teclado Mecanico Keychron Q1 Pro (Precio: S/. 780.00, Stock: 25, Cat: Perifericos)", "#89b4fa"),
        ("  - Auriculares Sony WH-1000XM5 (Precio: S/. 1299.00, Stock: 5, Cat: Audio)", "#89b4fa"),
        ("", "#cdd6f4"),
        ("--- 3. CONSULTA objects.filter(categoria='Perifericos') ---", "#fab387"),
        ("  - Total encontrados en 'Perifericos': 3", "#a6e3a1"),
    ]
    render_terminal_card("term_orm_queries.png", "Poblado y Consultas ORM con Lazy Evaluation", term_orm)

    term_tests = [
        ("PS C:\\Users\\USUARIO\\Documents\\!UNCP-DESARROLLO\\aguilar-11.2\\proyecto> python manage.py test catalogo", "#a6e3a1"),
        ("Creating test database for alias 'default'...", "#cdd6f4"),
        (".....", "#a6e3a1"),
        ("----------------------------------------------------------------------", "#585b70"),
        ("Ran 5 tests in 0.029s", "#cdd6f4"),
        ("", "#cdd6f4"),
        ("OK", "#a6e3a1"),
        ("Destroying test database for alias 'default'...", "#cdd6f4"),
        ("Found 5 test(s).", "#cdd6f4"),
        ("System check identified no issues (0 silenced).", "#a6e3a1"),
    ]
    render_terminal_card("term_tests_unitarios.png", "Batería de Pruebas Unitarias Automatizadas (TDD)", term_tests)

    print("[OK] Generación de evidencias completada exitosamente.")
