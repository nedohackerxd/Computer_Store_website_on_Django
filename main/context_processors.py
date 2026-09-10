# main/context_processors.py
from .models import Account
from products.models import Cart  

def cart_context(request):
    """
    Возвращает объект корзины и общее количество товаров 
    для всех шаблонов сайта.
    """
    email = request.COOKIES.get("email")
    if not email:
        return {'cart': None, 'cart_total_quantity': 0}

    acc = Account.objects.filter(email=email).first()
    if not acc:
        return {'cart': None, 'cart_total_quantity': 0}

    # Получаем или создаем корзину пользователя
    # (предполагается связь с User или Account)
    user_obj = getattr(acc, 'user', acc)
    cart, _ = Cart.objects.get_or_create(user=user_obj)

    # Вычисляем количество товаров
    total_qty = cart.get_total_quantity() if hasattr(cart, 'get_total_quantity') else 0

    return {
        'cart': cart,
        'cart_total_quantity': total_qty
    }