from django.shortcuts import render, redirect
from .models import Articulo, Taller
from django.db.models import Count, Sum, Q
from .forms import ArticuloForm
# Create your views here.


def index(request):

    articulo = request.GET.get('pk')
    importe_articulo = None
    q = request.GET.get('q') if request.GET.get('q') else ''
    if articulo:
        articulo = Articulo.objects.get(pk=articulo)
        importe_articulo = round(
            articulo.cantidad_producida_en_el_mes*articulo.costo, 2)

    talleres = Taller.objects.all()
    articulos = Articulo.objects.all()

    articulos_encontrados = articulos.filter(
        Q(nombre__icontains=q) |
        Q(codigo__icontains=q) |
        Q(costo__icontains=q) |
        Q(taller__codigo__icontains=q)
    )

    importe = articulos_encontrados.aggregate(
        importe=Sum('costo')*Sum('cantidad_producida_en_el_mes'))
    importe = round(importe['importe'], 2) if articulos_encontrados else 0

    articulos_rechazados = articulos.aggregate(
        rechazados=Sum('cantidad_rechazada'))
    articulos_rechazados = articulos_rechazados['rechazados'] if articulos else 0
    articulos_aceptados = articulos.aggregate(
        aceptados=Sum('cantidad_producida_en_el_mes'))
    articulos_aceptados = articulos_aceptados['aceptados'] - \
        articulos_rechazados if articulos else 0

    importe_articulos_rechazados = articulos.aggregate(
        importe=Sum('costo') * Sum('cantidad_rechazada'))
    importe_articulos_rechazados = round(
        importe_articulos_rechazados['importe'], 2) if articulos else 0

    importe_articulos_aceptados = articulos.aggregate(importe=Sum(
        'costo') * (Sum('cantidad_producida_en_el_mes') - Sum('cantidad_rechazada')))
    importe_articulos_aceptados = round(
        importe_articulos_aceptados['importe'], 2) if articulos else 0

    return render(request, 'index.html', context={'talleres': talleres,
                                                  'articulos': articulos,
                                                  'articulos_encontrados': articulos_encontrados,
                                                  'articulos_rechazados': articulos_rechazados,
                                                  'articulos_aceptados': articulos_aceptados,
                                                  'articulo': articulo,
                                                  'importe': importe,
                                                  'importe_articulo': importe_articulo,
                                                  'importe_articulos_rechazados': importe_articulos_rechazados,
                                                  'importe_articulos_aceptados': importe_articulos_aceptados
                                                  })


def agregar_articulo(request):
    form = ArticuloForm()

    if request.method == 'POST':
        form = ArticuloForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('main:index')

    context = {'form': form}

    return render(request, 'articulo_form.html', context=context)


def actualizar_articulo(request, pk):
    articulo = Articulo.objects.get(pk=pk)
    form = ArticuloForm(instance=articulo)

    if request.method == 'POST':
        form = ArticuloForm(request.POST, instance=articulo)
        if form.is_valid():
            form.save()
            return redirect(to=f'/?pk={pk}')

    context = {'form': form}
    return render(request, 'articulo_form.html', context)


def eliminar_articulo(request, pk):
    articulo = Articulo.objects.get(pk=pk)

    if request.method == 'POST':
        articulo.delete()
        return redirect('main:index')

    return render(request, 'articulo_delete.html', {'articulo': articulo})


def taller(request, pk):
    taller = Taller.objects.get(pk=pk)
    articulos = Articulo.objects.filter(taller=taller)
    importe = articulos.aggregate(importe=Sum(
        'costo') * Sum('cantidad_producida_en_el_mes'))
    importe = round(importe['importe'], 2) if articulos else 0

    importe_articulos_rechazados = articulos.aggregate(
        importe=Sum('costo') * Sum('cantidad_rechazada'))
    importe_articulos_rechazados = round(
        importe_articulos_rechazados['importe'], 2) if articulos else 0

    importe_articulos_aceptados = articulos.aggregate(importe=Sum(
        'costo') * (Sum('cantidad_producida_en_el_mes') - Sum('cantidad_rechazada')))
    importe_articulos_aceptados = round(
        importe_articulos_aceptados['importe'], 2) if articulos else 0

    return render(request, 'taller.html', context={'taller': taller,
                                                   'articulos': articulos,
                                                   'importe': importe,
                                                   'importe_articulos_rechazados': importe_articulos_rechazados,
                                                   'importe_articulos_aceptados': importe_articulos_aceptados
                                                   })


def acerca_de(request):
    return render(request, 'acerca_de.html')


def buscar_rango_fecha(request):
    start = request.GET.get('start') if request.GET.get('start') else ''
    end = request.GET.get('end') if request.GET.get('end') else ''
    articulos = Articulo.objects.all()
    if start and end:
        articulos = articulos.filter(mes_proceso__range=[start, end])

    importe = articulos.aggregate(importe=Sum(
        'costo') * Sum('cantidad_producida_en_el_mes'))
    importe = round(importe['importe'], 2) if articulos else 0

    importe_articulos_rechazados = articulos.aggregate(
        importe=Sum('costo') * Sum('cantidad_rechazada'))
    importe_articulos_rechazados = round(
        importe_articulos_rechazados['importe'], 2) if articulos else 0

    importe_articulos_aceptados = articulos.aggregate(importe=Sum(
        'costo') * (Sum('cantidad_producida_en_el_mes') - Sum('cantidad_rechazada')))
    importe_articulos_aceptados = round(
        importe_articulos_aceptados['importe'], 2) if articulos else 0

    return render(request, 'buscar_rango_fecha.html', context={"articulos": articulos,
                                                               'importe': importe,
                                                               'importe_articulos_rechazados': importe_articulos_rechazados,
                                                               'importe_articulos_aceptados': importe_articulos_aceptados})
