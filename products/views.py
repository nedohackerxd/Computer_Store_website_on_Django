from urllib.parse import quote, unquote
from django.shortcuts import render, redirect, get_object_or_404
from .models import Product, Cart, CartItem
from main.models import Account, User

def get_end(count):
    end = ""

    if count in range(1, 111, 10):
        if count in (11, 111):
            end = "s"
        else:
            end = ""
    else:
        end = "s"

    return end

def put_to_cart(request, product_id):
    referer_url = request.META.get('HTTP_REFERER', '/')

    try:
        email = request.COOKIES.get("email")
        if not email:
            return redirect(referer_url)

        acc = Account.objects.get(email=email)
        
        # Получаем или создаем корзину пользователя
        cart, _ = Cart.objects.get_or_create(user=acc.user)
        product = get_object_or_404(Product, id=product_id)

        # Добавляем товар в корзину или увеличиваем quantity
        cart_item, created = CartItem.objects.get_or_create(cart=cart, product=product)
        if not created:
            cart_item.quantity += 1
            cart_item.save(update_fields=['quantity'])

        return redirect(referer_url)

    except Exception:
        return redirect(referer_url)

def del_from_cart(request, product_id):
    # Возвращаем пользователя на ту же страницу, откуда был сделан клик (или в /user-data/)
    referer_url = request.META.get('HTTP_REFERER', '/user-data/')

    try:
        email = request.COOKIES.get("email")
        if not email:
            return redirect(referer_url)

        # 1. Получаем аккаунт и корзину пользователя
        acc = Account.objects.get(email=email)
        cart = Cart.objects.filter(user=acc.user).first()

        if cart:
            # 2. Ищем конкретную позицию товара в корзине пользователя
            cart_item = CartItem.objects.filter(cart=cart, product_id=product_id).first()

            if cart_item:
                if cart_item.quantity > 1:
                    # Если единиц товара больше 1 — уменьшаем счетчик
                    cart_item.quantity -= 1
                    cart_item.save(update_fields=['quantity'])
                else:
                    # Если осталась 1 штука — удаляем запись из БД полностью
                    cart_item.delete()

        return redirect(referer_url)

    except Exception:
        return redirect(referer_url)

def remove_from_cart(request, product_id):
    referer_url = request.META.get('HTTP_REFERER', '/user-data/')
    email = request.COOKIES.get("email")

    if email:
        acc = Account.objects.filter(email=email).first()
        if acc:
            # Находим и сразу удаляем позицию товара для текущего пользователя
            CartItem.objects.filter(cart__user=acc.user, product_id=product_id).delete()

    return redirect(referer_url)

def clear_cart(request):
    referer_url = request.META.get('HTTP_REFERER', '/user-data/')
    email = request.COOKIES.get("email")

    if email:
        try:
            acc = Account.objects.get(email=email)
            # Удаляем сразу все записи CartItem, привязанные к корзине пользователя
            CartItem.objects.filter(cart__user=acc.user).delete()
        except Exception:
            pass

    return redirect(referer_url)

def processors(request):
    pr = Product.objects.filter(type="Processor")
    
    # 1. Безопасно достаем данные пользователя из кук
    raw_name = request.COOKIES.get("name")
    email = request.COOKIES.get("email")
    
    udata = ""
    cart_product_ids = []

    if email:
        acc = Account.objects.filter(email=email).first()
        if acc:
            name = unquote(raw_name) if raw_name else acc.user.name
            udata = {"name": name}
            
            # 2. Получаем список ID всех товаров, которые лежат в корзине пользователя в БД
            cart = Cart.objects.filter(user=acc.user).first()
            if cart:
                # values_list дает список первичных ключей [1, 5, 12]
                cart_product_ids = cart.items.values_list('product_id', flat=True)

    count = pr.count()  # Использование count() на QuerySet работает быстрее, чем len()
    end = get_end(count)

    return render(request, "processors.html", {
        "pr": pr,
        "count": count,
        "end": end,
        "cart_product_ids": cart_product_ids,  # Теперь передаем список ID для проверки `i.id in cart_product_ids`
        "udata": udata
    })

def videocards(request):
    pr = Product.objects.filter(type="Videocard")
    
    # 1. Безопасно достаем данные пользователя из кук
    raw_name = request.COOKIES.get("name")
    email = request.COOKIES.get("email")
    
    udata = ""
    cart_product_ids = []

    if email:
        acc = Account.objects.filter(email=email).first()
        if acc:
            name = unquote(raw_name) if raw_name else acc.user.name
            udata = {"name": name}
            
            # 2. Получаем список ID всех товаров, которые лежат в корзине пользователя в БД
            cart = Cart.objects.filter(user=acc.user).first()
            if cart:
                # values_list дает список первичных ключей [1, 5, 12]
                cart_product_ids = cart.items.values_list('product_id', flat=True)

    count = pr.count()  # Использование count() на QuerySet работает быстрее, чем len()
    end = get_end(count)

    return render(request, "videocards.html", {
        "pr": pr,
        "count": count,
        "end": end,
        "cart_product_ids": cart_product_ids,  # Теперь передаем список ID для проверки `i.id in cart_product_ids`
        "udata": udata
    })

def ram(request):
    pr = Product.objects.filter(type="RAM")
    
    # 1. Безопасно достаем данные пользователя из кук
    raw_name = request.COOKIES.get("name")
    email = request.COOKIES.get("email")
    
    udata = ""
    cart_product_ids = []

    if email:
        acc = Account.objects.filter(email=email).first()
        if acc:
            name = unquote(raw_name) if raw_name else acc.user.name
            udata = {"name": name}
            
            # 2. Получаем список ID всех товаров, которые лежат в корзине пользователя в БД
            cart = Cart.objects.filter(user=acc.user).first()
            if cart:
                # values_list дает список первичных ключей [1, 5, 12]
                cart_product_ids = cart.items.values_list('product_id', flat=True)

    count = pr.count()  # Использование count() на QuerySet работает быстрее, чем len()
    end = get_end(count)

    return render(request, "ram.html", {
        "pr": pr,
        "count": count,
        "end": end,
        "cart_product_ids": cart_product_ids,  # Теперь передаем список ID для проверки `i.id in cart_product_ids`
        "udata": udata
    })

def ssd(request):
    pr = Product.objects.filter(type="SSD")
    
    # 1. Безопасно достаем данные пользователя из кук
    raw_name = request.COOKIES.get("name")
    email = request.COOKIES.get("email")
    
    udata = ""
    cart_product_ids = []

    if email:
        acc = Account.objects.filter(email=email).first()
        if acc:
            name = unquote(raw_name) if raw_name else acc.user.name
            udata = {"name": name}
            
            # 2. Получаем список ID всех товаров, которые лежат в корзине пользователя в БД
            cart = Cart.objects.filter(user=acc.user).first()
            if cart:
                # values_list дает список первичных ключей [1, 5, 12]
                cart_product_ids = cart.items.values_list('product_id', flat=True)

    count = pr.count()  # Использование count() на QuerySet работает быстрее, чем len()
    end = get_end(count)

    return render(request, "ssd.html", {
        "pr": pr,
        "count": count,
        "end": end,
        "cart_product_ids": cart_product_ids,  # Теперь передаем список ID для проверки `i.id in cart_product_ids`
        "udata": udata
    })

def motherboards(request):
    pr = Product.objects.filter(type="Motherboard")
    
    # 1. Безопасно достаем данные пользователя из кук
    raw_name = request.COOKIES.get("name")
    email = request.COOKIES.get("email")
    
    udata = ""
    cart_product_ids = []

    if email:
        acc = Account.objects.filter(email=email).first()
        if acc:
            name = unquote(raw_name) if raw_name else acc.user.name
            udata = {"name": name}
            
            # 2. Получаем список ID всех товаров, которые лежат в корзине пользователя в БД
            cart = Cart.objects.filter(user=acc.user).first()
            if cart:
                # values_list дает список первичных ключей [1, 5, 12]
                cart_product_ids = cart.items.values_list('product_id', flat=True)

    count = pr.count()  # Использование count() на QuerySet работает быстрее, чем len()
    end = get_end(count)

    return render(request, "motherboards.html", {
        "pr": pr,
        "count": count,
        "end": end,
        "cart_product_ids": cart_product_ids,  # Теперь передаем список ID для проверки `i.id in cart_product_ids`
        "udata": udata
    })

def powersupplies(request):
    pr = Product.objects.filter(type="PowerSupply")
    
    # 1. Безопасно достаем данные пользователя из кук
    raw_name = request.COOKIES.get("name")
    email = request.COOKIES.get("email")
    
    udata = ""
    cart_product_ids = []

    if email:
        acc = Account.objects.filter(email=email).first()
        if acc:
            name = unquote(raw_name) if raw_name else acc.user.name
            udata = {"name": name}
            
            # 2. Получаем список ID всех товаров, которые лежат в корзине пользователя в БД
            cart = Cart.objects.filter(user=acc.user).first()
            if cart:
                # values_list дает список первичных ключей [1, 5, 12]
                cart_product_ids = cart.items.values_list('product_id', flat=True)

    count = pr.count()  # Использование count() на QuerySet работает быстрее, чем len()
    end = get_end(count)

    return render(request, "powersupplies.html", {
        "pr": pr,
        "count": count,
        "end": end,
        "cart_product_ids": cart_product_ids,  # Теперь передаем список ID для проверки `i.id in cart_product_ids`
        "udata": udata
    })

def cooling(request):
    pr = Product.objects.filter(type="Cooling")
    
    # 1. Безопасно достаем данные пользователя из кук
    raw_name = request.COOKIES.get("name")
    email = request.COOKIES.get("email")
    
    udata = ""
    cart_product_ids = []

    if email:
        acc = Account.objects.filter(email=email).first()
        if acc:
            name = unquote(raw_name) if raw_name else acc.user.name
            udata = {"name": name}
            
            # 2. Получаем список ID всех товаров, которые лежат в корзине пользователя в БД
            cart = Cart.objects.filter(user=acc.user).first()
            if cart:
                # values_list дает список первичных ключей [1, 5, 12]
                cart_product_ids = cart.items.values_list('product_id', flat=True)

    count = pr.count()  # Использование count() на QuerySet работает быстрее, чем len()
    end = get_end(count)

    return render(request, "cooling.html", {
        "pr": pr,
        "count": count,
        "end": end,
        "cart_product_ids": cart_product_ids,  # Теперь передаем список ID для проверки `i.id in cart_product_ids`
        "udata": udata
    })

def cases(request):
    pr = Product.objects.filter(type="Case")
    
    # 1. Безопасно достаем данные пользователя из кук
    raw_name = request.COOKIES.get("name")
    email = request.COOKIES.get("email")
    
    udata = ""
    cart_product_ids = []

    if email:
        acc = Account.objects.filter(email=email).first()
        if acc:
            name = unquote(raw_name) if raw_name else acc.user.name
            udata = {"name": name}
            
            # 2. Получаем список ID всех товаров, которые лежат в корзине пользователя в БД
            cart = Cart.objects.filter(user=acc.user).first()
            if cart:
                # values_list дает список первичных ключей [1, 5, 12]
                cart_product_ids = cart.items.values_list('product_id', flat=True)

    count = pr.count()  # Использование count() на QuerySet работает быстрее, чем len()
    end = get_end(count)

    return render(request, "cases.html", {
        "pr": pr,
        "count": count,
        "end": end,
        "cart_product_ids": cart_product_ids,  # Теперь передаем список ID для проверки `i.id in cart_product_ids`
        "udata": udata
    })