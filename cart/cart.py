from store.models import Product

class Cart:
    def __init__(self, request):
        self.session = request.session
        cart = self.session.get('cart')
        if not cart:
            cart = self.session['cart'] = {}
        self.cart = cart

    def save(self):
        self.session.modified = True

    def add(self, product):
        product_id = str(product.id)

        if product.inventory > 0:
            if product_id in self.cart:
                if self.cart[product_id]['quantity'] < product.inventory:
                    self.cart[product_id]['quantity'] += 1
                    self.save()
                    return {'success': True, 'message': 'added product'}
                else:
                    return {'success': False, 'message': 'no inventory'}
            else:
                self.cart[product_id] = {'quantity': 1, 'weight': product.weight}
                self.save()
                return {'success': True, 'message': 'added product'}
        else:
            return {'success': False, 'message': 'no inventory'}

    def decrease(self, product):
        product_id = str(product.id)

        if self.cart[product_id]['quantity'] > 1:
            self.cart[product_id]['quantity'] -= 1
        else:
            del self.cart[product_id]

        self.save()

    def remove(self, product):
        product_id = str(product.id)
        if product_id in self.cart:
            del self.cart[product_id]
        self.save()

    def clear(self):
        del self.session['cart']
        self.save()

    def get_total_price(self):
        price = 0
        product_ids = self.cart.keys()
        products = Product.objects.filter(id__in=product_ids)

        for item in products:
            price += item.price * self.cart[str(item.id)]['quantity']

        return price

    def get_total_post(self):
        weight = sum([item['quantity'] * item['weight'] for item in self.cart.values()])

        if weight < 10000:
            return 200000
        else:
            return 500000

    def get_final_price(self):
        return self.get_total_price() + self.get_total_post()

    def __len__(self):
        return sum([i['quantity'] for i in self.cart.values()])

    def __iter__(self):
        product_ids = self.cart.keys()
        products = Product.objects.filter(id__in=product_ids)
        cart_dict = self.cart.copy()

        for product in products:
            cart_dict[str(product.id)]['price'] = product.price
            cart_dict[str(product.id)]['product'] = product

        for item in cart_dict.values():
            item['total'] = item['price'] * item['quantity']
            yield item
