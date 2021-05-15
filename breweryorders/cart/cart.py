from decimal import Decimal
from django.conf import settings
from orders.models import Stock


class Cart(object):

    def __init__(self, request):

        """
        Inicjalizacja koszyka na zakupy
        """
        self.session = request.session
        cart = self.session.get(settings.CART_SESSION_ID)
        if not cart:
            # zapis pustego koszyka na zakupy w sesji
            cart = self.session[settings.CART_SESSION_ID] = {}
        self.cart = cart

    def add(self, product, quantity=1, update_quantity=False):
        """
        Dodawanie produktu do koszyka lub zmiana jego ilości
        """
        product_id = str(product.id)
        if product_id not in self.cart:
            self.cart[product_id] = {'quantity': 0, 'price': str(product.distribution.price)}
        if update_quantity:
            self.cart[product_id]['quantity'] = quantity
        else:
            self.cart[product_id]['quantity'] += quantity
        self.save()

    def save(self):
        # Oznaczenie sesji jako zmodyfikowana, aby upewnić się o jej zapisaniu
        self.session.modified = True

    def remove(self, product):
        """
        Usunięcie produktu z koszyka
        """
        product_id = str(product.id)

        if product_id in self.cart:
            del self.cart[product_id]
            self.save()

    def __iter__(self):
        """
        Iteracja przez elementy koszyka i pobieranie produktów z bazy danych
        """
        product_ids = self.cart.keys()
        # pobieranie obiektów produktów i dodanie ich do koszyka
        products = Stock.objects.filter(id__in=product_ids)

        cart = self.cart.copy()
        for product in products:
            cart[str(product.id)]['product'] = product
        for item in cart.values():
            item['price'] = Decimal(item['price'])
            item['total_price'] = item['price'] * item['quantity']
            yield item

    def __len__(self):
        """
        Obliczanie liczby wszystkich elementów w koszyku na zakupy
        """
        return sum(item['quantity'] for item in self.cart.values())

    def get_total_price(self):
        return sum(Decimal(item['price']) * item['quantity'] for item in self.cart.values())

    def clear(self):
        # Usunięcie koszyka z sesji
        del self.session[settings.CART_SESSION_ID]
        self.save()
