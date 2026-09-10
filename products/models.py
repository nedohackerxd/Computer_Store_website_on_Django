from django.db import models
from main import models as mm

class Product(models.Model):
    name = models.TextField()
    price = models.IntegerField()
    in_sell = models.CharField(max_length=15)
    type = models.CharField(max_length=30)

class Cart(models.Model):
    user = models.OneToOneField(mm.User, on_delete=models.CASCADE, related_name='cart')
    created_at = models.DateTimeField(auto_now_add=True)

    def get_total_price(self):
        # Оптимизация select_related('product') ускоряет расчет цены без лишних запросов к БД
        return sum(item.get_cost() for item in self.items.select_related('product').all())

    def get_total_quantity(self):
        return sum(item.quantity for item in self.items.all())


class CartItem(models.Model):
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE, related_name='items')
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)

    class Meta:
        # Уникальность по паре (корзина, товар)
        unique_together = ('cart', 'product')

    def __str__(self):
        # Доступ к имени пользователя через корзину
        return f"{self.cart.user.name} — {self.product.name} ({self.quantity} шт.)"

    def get_cost(self):
        return self.product.price * self.quantity