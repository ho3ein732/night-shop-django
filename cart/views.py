from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.shortcuts import render, get_object_or_404, redirect
from django.views.decorators.http import require_POST
from .cart import Cart
from store.models import Product
from .forms import InvoiceForm
from .models import Order, OrderItem


# Create your views here.

@require_POST
def add_to_cart(request, product_id):
    try:
        cart = Cart(request)
        product = get_object_or_404(Product, id=product_id)
        result = cart.add(product)

        if not result['success']:
            return JsonResponse({'error': result['message']}, status=400)

        return JsonResponse({
            'success': True,
            'item_count': len(cart),
            'total_price': cart.get_total_price(),
            'message': result['message']
        })

    except Product.DoesNotExist:
        return JsonResponse({'error': 'محصول یافت نشد.'}, status=404)
    except Exception as e:
        return JsonResponse({'error': f'خطا: {str(e)}'}, status=400)


def cart_status(request):
    cart = Cart(request)

    response = {
        'item_count': len(cart),
        'total_price': cart.get_total_price(),
    }

    return JsonResponse(response)


def remove_item(request):
    if request.method == 'POST':
        product_id = request.POST.get('item_id')
        cart = Cart(request)
        try:
            if product_id:
                product = get_object_or_404(Product, id=product_id)
                cart.remove(product)
                return JsonResponse({'success': True, 'total_price': cart.get_total_price()})
        except Exception as e:
            return JsonResponse({'error': str(e)})
    return JsonResponse({'error': 'Invalid request method'})


def cart_detail(request):
    cart = Cart(request)
    return render(request, 'cart/cart.html', {'cart': cart})


def update_quantity(request):
    try:
        item_id = request.POST.get('item_id')
        action = request.POST.get('action')

        if not item_id or not action:
            return JsonResponse({'success': False, 'error': 'Invalid input.'}, status=400)

        cart = Cart(request)
        product = get_object_or_404(Product, id=item_id)

        if action == 'decrease':
            cart.decrease(product)
        elif action == 'add':
            cart.add(product)
        else:
            return JsonResponse({'success': False, 'error': 'Invalid action.'}, status=400)

        context = {
            'total_price': cart.get_total_price(),
            'quantity': cart.cart[str(product.id)]['quantity'],
            'success': True,
        }
        return JsonResponse(context)

    except Exception as e:
        return JsonResponse({'success': False, 'error': str(e)}, status=500)


@login_required
def add_address(request):
    # region add address
    if request.method == "POST":
        form = InvoiceForm(request.POST)
        if form.is_valid():
            address = form.save(commit=False)
            address.user = request.user
            address.save()
    # endregion
            # region create Order
            order = Order.objects.create(
                buyer=request.user,
                address=address,
            )
            # endregion

            # region create Order Item
            cart = Cart(request)
            for item in cart:
                OrderItem.objects.create(
                    orders=order,
                    product=item['product'],
                    price=item['price'],
                    quantity=item['quantity'],
                    weight=item['weight'],
                )
            # endregion
            cart.clear()
            return redirect('cart:order', order_id=order.id)
        else:
            print(form.errors)
    else:
        form = InvoiceForm()

    return render(request, 'cart/invoice.html', {'form': form})


def order(request, order_id):
    orders = get_object_or_404(Order, pk=order_id, buyer=request.user)
    return render(request, 'cart/order.html', {'orders': orders})