from django.shortcuts import render, redirect, get_object_or_404
from .models import Producto

def agregar_al_carrito(request, producto_id):
    producto = get_object_or_404(Producto, pk=producto_id)
    carrito = request.session.get('carrito', {})

    if str(producto_id) in carrito:
        carrito[str(producto_id)]['cantidad'] += 1
    else:
        carrito[str(producto_id)] = {
            'nombre': producto.nombre,
            'precio': str(producto.precio),
            'cantidad': 1,
        }

    request.session['carrito'] = carrito
    return redirect('ver_carrito')

def ver_carrito(request):
    carrito = request.session.get('carrito', {})
    total = sum(float(item['precio']) * item['cantidad'] for item in carrito.values())
    return render(request, 'tienda/carrito.html', {'carrito': carrito, 'total': total})

def lista_productos(request):
    productos = Producto.objects.all()
    return render(request, 'tienda/productos.html', {'productos': productos})
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



