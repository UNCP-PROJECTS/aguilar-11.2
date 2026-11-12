from django.test import TestCase
from django.urls import reverse
from .models import Producto

class CatalogoTests(TestCase):
    def setUp(self):
        self.p1 = Producto.objects.create(
            nombre="Laptop ThinkPad T14 Gen 4",
            descripcion="Portátil empresarial AMD Ryzen 7 PRO",
            precio=4899.00,
            categoria="Computadoras",
            stock=12
        )
        self.p2 = Producto.objects.create(
            nombre="Teclado Mecánico Keychron Q1 Pro",
            descripcion="Switches mecánicos inalámbrico",
            precio=780.00,
            categoria="Periféricos",
            stock=0
        )

    def test_modelo_producto_str(self):
        self.assertEqual(str(self.p1), "Laptop ThinkPad T14 Gen 4 (S/. 4899.00)")

    def test_url_reversa_resolucion(self):
        self.assertEqual(reverse('home'), '/')
        self.assertEqual(reverse('catalogo'), '/catalogo/')

    def test_vista_fbv_home(self):
        response = self.client.get(reverse('home'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'home.html')
        self.assertEqual(response.context['total_productos'], 2)
        self.assertEqual(response.context['total_stock'], 12)

    def test_vista_cbv_catalogo_listview(self):
        response = self.client.get(reverse('catalogo'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'catalogo.html')
        self.assertIn('productos', response.context)
        self.assertEqual(len(response.context['productos']), 2)

    def test_filtrado_por_categoria(self):
        response = self.client.get(reverse('catalogo'), {'categoria': 'Periféricos'})
        self.assertEqual(response.status_code, 200)
        productos = response.context['productos']
        self.assertEqual(len(productos), 1)
        self.assertEqual(productos[0].nombre, "Teclado Mecánico Keychron Q1 Pro")
