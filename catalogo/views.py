from django.shortcuts import render
from django.views.generic import ListView
from django.db.models import Sum, F
from .models import Producto

def home(request):
    total_productos = Producto.objects.count()
    total_stock = Producto.objects.aggregate(total=Sum('stock'))['total'] or 0
    valor_inventario = Producto.objects.aggregate(
        valor=Sum(F('precio') * F('stock'))
    )['valor'] or 0.0
    destacados = Producto.objects.filter(stock__gt=0)[:4]

    context = {
        'total_productos': total_productos,
        'total_stock': total_stock,
        'valor_inventario': valor_inventario,
        'destacados': destacados,
    }
    return render(request, 'catalogo/home.html', context)

class ProductoListView(ListView):
    model = Producto
    template_name = 'catalogo/catalogo.html'
    context_object_name = 'productos'
    paginate_by = 8

    def get_queryset(self):
        queryset = Producto.objects.all()
        categoria = self.request.GET.get('categoria')
        q = self.request.GET.get('q')
        orden = self.request.GET.get('orden')

        if categoria:
            queryset = queryset.filter(categoria=categoria)
        if q:
            queryset = queryset.filter(nombre__icontains=q)
        if orden == 'precio_asc':
            queryset = queryset.order_by('precio')
        elif orden == 'precio_desc':
            queryset = queryset.order_by('-precio')
        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['categorias'] = Producto.objects.values_list('categoria', flat=True).distinct()
        context['categoria_actual'] = self.request.GET.get('categoria', '')
        context['busqueda_actual'] = self.request.GET.get('q', '')
        context['orden_actual'] = self.request.GET.get('orden', '')
        return context
