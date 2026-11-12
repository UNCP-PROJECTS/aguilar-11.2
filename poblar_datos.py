import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

from catalogo.models import Producto

PRODUCTOS_SEEDS = [
    {
        'nombre': 'Laptop ThinkPad T14 Gen 4',
        'descripcion': 'Procesador AMD Ryzen 7 PRO 7840U, 32GB RAM DDR5, 1TB SSD NVMe, Pantalla 14" IPS WUXGA 400 nits.',
        'precio': 4899.00,
        'categoria': 'Computadoras',
        'stock': 12,
    },
    {
        'nombre': 'Monitor Dell UltraSharp U2724D',
        'descripcion': 'Pantalla 27" QHD 2560x1440, panel IPS Black con contraste 2000:1, tasa de refresco 120Hz y cobertura sRGB 100%.',
        'precio': 1850.00,
        'categoria': 'Monitores',
        'stock': 8,
    },
    {
        'nombre': 'Teclado Mecánico Keychron Q1 Pro',
        'descripcion': 'Chasis de aluminio mecanizado CNC, conectividad inalámbrica Bluetooth 5.1 y cableada, switches mecánicos Gateron Brown.',
        'precio': 780.00,
        'categoria': 'Periféricos',
        'stock': 25,
    },
    {
        'nombre': 'Mouse Ergonómico Logitech MX Master 3S',
        'descripcion': 'Sensor Darkfield 8000 DPI con seguimiento sobre cristal, clics silenciosos y rueda de desplazamiento MagSpeed.',
        'precio': 389.90,
        'categoria': 'Periféricos',
        'stock': 18,
    },
    {
        'nombre': 'Auriculares Sony WH-1000XM5',
        'descripcion': 'Cancelación activa de ruido Noise Cancelling con procesador V1 y HD QN1, códec LDAC de alta fidelidad y 30h de batería.',
        'precio': 1299.00,
        'categoria': 'Audio',
        'stock': 5,
    },
    {
        'nombre': 'Switch Cisco CBS250 24 Puertos Gigabit',
        'descripcion': 'Switch gestionable de capa 2/3 con 24 puertos 10/100/1000 y 4 enlaces ascendentes SFP de 1G para infraestructura empresarial.',
        'precio': 1450.00,
        'categoria': 'Redes',
        'stock': 0,
    },
    {
        'nombre': 'Cámara Web Logitech Brio 4K Ultra HD',
        'descripcion': 'Grabación y streaming 4K HDR a 30fps o 1080p a 60fps, sensor con zoom digital 5x y soporte para Windows Hello.',
        'precio': 620.00,
        'categoria': 'Periféricos',
        'stock': 15,
    },
    {
        'nombre': 'Disco SSD Externo Samsung T7 Shield 2TB',
        'descripcion': 'Almacenamiento portátil resistente a caídas y agua IP65, velocidades de transferencia secuencial de hasta 1050 MB/s.',
        'precio': 540.00,
        'categoria': 'Almacenamiento',
        'stock': 20,
    },
]

def poblar():
    creados = 0
    for p_data in PRODUCTOS_SEEDS:
        prod, created = Producto.objects.get_or_create(
            nombre=p_data['nombre'],
            defaults=p_data
        )
        if created:
            creados += 1

    total = Producto.objects.count()
    print(f"[OK] Proceso de poblado completado: {creados} nuevos creados (Total en BD: {total}).")

    print("\n--- 1. CONSULTA objects.all() (Lazy Evaluation / Evaluacion Perezosa) ---")
    qs1 = Producto.objects.all()
    print(f"Tipo retornado: {type(qs1)} (La consulta SQL aún no se ejecuta)")
    for p in qs1[:5]:
        print(f"  - ID: {p.id} | {p.nombre} | S/. {p.precio:.2f} | Stock: {p.stock}")

    print("\n--- 2. CONSULTA objects.filter(stock__gt=0).order_by('precio') ---")
    qs2 = Producto.objects.filter(stock__gt=0).order_by('precio')
    for p in qs2[:5]:
        print(f"  - {p.nombre} (Precio: S/. {p.precio:.2f}, Stock: {p.stock}, Cat: {p.categoria})")

    print("\n--- 3. CONSULTA objects.filter(categoria='Periféricos') ---")
    qs3 = Producto.objects.filter(categoria='Periféricos')
    print(f"  - Total encontrados en 'Periféricos': {qs3.count()}")

if __name__ == '__main__':
    poblar()
