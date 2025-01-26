from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.shortcuts import render, get_object_or_404, redirect
from django.views.decorators.http import require_POST
from .cart import Cart
from store.models import Product
from .forms import InvoiceForm
from .models import Order, OrderItem

from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.conf import settings
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt
import requests
import logging


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
                return JsonResponse({'success': True, 'total_price': cart.get_total_price(), 'item_count': len(cart)})
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


logger = logging.getLogger(__name__)


def add_address(request):
    if request.method == "POST":
        form = InvoiceForm(request.POST)
        if form.is_valid():
            address = form.save(commit=False)
            address.user = request.user
            address.save()

            cart = Cart(request)

            description = ''
            for item in cart:
                description += str(item['product'].name) + ', '

            data = {
                "merchant_id": settings.MERCHANT,
                "amount": cart.get_final_price(),
                "callback_url": settings.ZARINPAL_CALLBACK_URL,
                "description": description,
            }
            headers = {"Content-Type": "application/json"}

            try:
                response = requests.post(settings.ZARINPAL_REQUEST_URL, json=data, headers=headers)
                response_data = response.json()
                print(response_data)  # چاپ پاسخ برای بررسی جزئیات

                if response_data.get('data') and response_data['data']['code'] == 100:
                    return redirect(f"https://sandbox.zarinpal.com/pg/StartPay/{response_data['data']['authority']}")
                else:
                    return JsonResponse({'success': False, 'message': f"خطا در درخواست پرداخت: {response_data.get('errors', 'جزئیات خطا موجود نیست')}"})
            except Exception as e:
                return JsonResponse({'success': False, 'message': f"خطا در ارسال درخواست: {e}"})

    else:
        form = InvoiceForm()

    return render(request, 'cart/invoice.html', {'form': form})


@login_required
def order(request, order_id):
    orders = get_object_or_404(Order, pk=order_id, buyer=request.user, paid=True)
    return render(request, 'cart/order.html', {'orders': orders})


@csrf_exempt
def verify(request):
    print(40 * '_____')
    authority = request.GET.get('Authority')
    status = request.GET.get('Status')

    if not authority or not status:
        return HttpResponse("درخواست نامعتبر است.")

    if status == 'OK':
        cart = Cart(request)
        data = {
            "merchant_id": settings.MERCHANT,
            "amount": cart.get_final_price(),  # مطمئن شوید مبلغ درست استفاده می‌شود
            "authority": authority,
        }
        headers = {"Content-Type": "application/json"}

        try:
            response = requests.post(settings.ZARINPAL_VERIFY_URL, json=data, headers=headers)
            response_data = response.json()

            if response_data.get('data') and response_data['data']['code'] == 100:
                order = Order.objects.create(
                    buyer=request.user,
                    address=request.user.addresses.last(),
                    paid=True
                )

                for item in cart:
                    OrderItem.objects.create(
                        orders=order,
                        product=item['product'],
                        price=item['price'],
                        quantity=item['quantity'],
                        weight=item['weight']
                    )

                    product = item['product']
                    quantity = item['quantity']

                    if product.inventory > quantity:
                        product.inventory -= quantity
                        product.sell += quantity
                        product.save()
                    else:
                        return render(request, 'cart/order.html', {'success': False, 'message': 'موجودی ناکافی'})

                cart.clear()  # پاک کردن سبد خرید
                return render(request, 'cart/order.html', {'success': True, 'message': f"پرداخت موفق! شماره تراکنش: {response_data['data']['ref_id']}", 'orders': order})
            else:
                return render(request, 'cart/order.html', {'success': False, 'message': 'خطا در تایید پرداخت'})
        except Exception as e:
            return render(request, 'cart/order.html', {'success': False, 'message': "خطا در تایید پرداخت"})
    else:
        return render(request, 'cart/order.html', {'success': False, 'message': "پرداخت توسط کاربر لغو شد."})
