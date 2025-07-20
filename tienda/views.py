from django.shortcuts import render, redirect, get_object_or_404
from .models import Producto
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST
from django.http import HttpResponseRedirect
from django.urls import reverse

def agregar_al_carrito(request, producto_id):
    producto = get_object_or_404(Producto, pk=producto_id)
    carrito = request.session.get('carrito', {})

    cantidad = int(request.POST.get('cantidad', 1))
    if str(producto_id) in carrito:
        carrito[str(producto_id)]['cantidad'] += cantidad
        
    else:
        carrito[str(producto_id)] = {
            'nombre': producto.nombre,
            'precio': str(producto.precio),
            'cantidad': cantidad,
            
        }

    request.session['carrito'] = carrito
    request.session['agregados_count'] = len(carrito)
    return redirect('ver_carrito')
def ver_carrito(request):
    carrito = request.session.get('carrito', {})
    total = 0
    items = []

    for key, item in carrito.items():
        precio = float(item['precio'])
        cantidad = item['cantidad']
        subtotal = precio * cantidad
        total += subtotal
        items.append({
            'id': key,  # Este 'id' se usa en los botones + y -
            'nombre': item['nombre'],
            'precio': f"{precio:.2f}",
            'cantidad': cantidad,
            'subtotal': f"{subtotal:.2f}",
        })

    return render(request, 'tienda/carrito.html', {
        'items': items,
        'total': f"{total:.2f}",
        'agregados_count': len(carrito),
    })



def lista_productos(request):
    productos = Producto.objects.all()
    carrito = request.session.get('carrito', {})
    request.session['agregados_count'] = len(carrito)  # ✅

    return render(request, 'tienda/productos.html', {
        'productos': productos,
        'agregados_count': len(carrito),
    })

#mensaje de whastapp
from urllib.parse import quote

def finalizar_pedido(request):
    carrito = request.session.get('carrito', {})
    if not carrito:
        return redirect('ver_carrito')

    mensaje = "🛍️ *Nuevo Pedido*\n"
    total = 0

    for item in carrito.values():
        subtotal = float(item['precio']) * item['cantidad']
        total += subtotal
        mensaje += f"- {item['nombre']} x{item['cantidad']} = Bs {subtotal:.2f}\n"

    mensaje += f"\n💰 *Total a pagar:* Bs {total:.2f}"
    mensaje += "\n\n📍 Dirección: [Agrega aquí la dirección del cliente]"
    mensaje += "\n📞 Teléfono: [Agrega aquí el número del cliente]"
    mensaje += "\n👤 Nombre: [Agrega aquí el nombre del cliente]"

    # Número del vendedor (cambia 5917xxxxxxx por uno real)
    numero_vendedor = "59179730325"
    enlace = f"https://wa.me/{numero_vendedor}?text={quote(mensaje)}"
    return redirect(enlace)

#bacia el carrito despues pedido

@require_POST
def actualizar_cantidad(request):
    producto_id = str(request.POST.get('producto_id'))  # Convertido a str

    try:
        nueva_cantidad = int(request.POST.get('cantidad'))
    except (ValueError, TypeError):
        return redirect('ver_carrito')

    carrito = request.session.get('carrito', {})

    if producto_id in carrito:
        if nueva_cantidad > 0:
            carrito[producto_id]['cantidad'] = nueva_cantidad
        else:
            del carrito[producto_id]  # Si es 0, se elimina
        request.session['carrito'] = carrito

    return redirect('ver_carrito')

@require_POST
def eliminar_producto(request):
    nombre = request.POST.get('nombre')
    carrito = request.session.get('carrito', {})
    
    # Elimina producto por nombre
    producto_id_a_eliminar = None
    for producto_id, item in carrito.items():
        if item['nombre'] == nombre:
            producto_id_a_eliminar = producto_id
            break

    if producto_id_a_eliminar:
        del carrito[producto_id_a_eliminar]
        request.session['carrito'] = carrito
        request.session['agregados_count'] = len(carrito)

    return redirect('ver_carrito')
# cuenta
def cuenta(request):
    return render(request, 'tienda/cuenta.html')
def panel_vendedor(request):
    return render(request, 'tienda/vendedor.html')

