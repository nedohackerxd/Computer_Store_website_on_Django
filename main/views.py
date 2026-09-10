from urllib.parse import quote, unquote
from django.shortcuts import render, redirect
from products.models import *
from .forms import *
from .models import *

forb = "Incorrect email or password. Try again."
forb2 = "User with this email already exist. Try again."

uform = UserForm()
aform = AccountForm()

def index(request):
    try:
        raw_name = request.COOKIES["name"]
        name = unquote(raw_name)
        udata = {"name": name}
        return render(request, "index.html", {"udata": udata})
    except:
        return render(request, "index.html", {"udata": ""})

def about(request):
    try:
        raw_name = request.COOKIES["name"]
        name = unquote(raw_name)
        udata = {"name": name}
        return render(request, "about.html", {"udata": udata})
    except:
        return render(request, "about.html", {"udata": ""})

def contacts(request):
    try:
        raw_name = request.COOKIES["name"]
        name = unquote(raw_name)
        udata = {"name": name}
        email = "compstore@example.com"
        return render(request, "contacts.html", {"udata": udata, "email": email})
    except:
        return render(request, "contacts.html", {"udata": "", "email": email})


def user_data(request):
    # Безопасно получаем email из куков
    email = request.COOKIES.get("email")
    if not email:
        return redirect('/sign-in/')

    # Получаем аккаунт пользователя из БД
    acc = Account.objects.filter(email=email).first()
    if not acc:
        return redirect('/sign-in/')


    # Декодируем имя из куков или берем прямо из БД
    raw_name = request.COOKIES.get("name", "")
    name = unquote(raw_name) if raw_name else acc.user.name

    udata = {
        "name": name,
        "email": acc.email
    }

    return render(request, "user-data.html", {
        "udata": udata # Передаем объект корзины со всеми элементами CartItem
    })

def sign_in(request):
    return render(request, "sign-in.html", 
        {"text": "Sign in", "form": uform}
    )

def try_sign_in(request):
    if request.method == "POST":
        usform = UserForm(request.POST)
        if usform.is_valid():
            accounts = Account.objects.all()
            email = usform.cleaned_data["email"]
            password = usform.cleaned_data["password"]
            data_checked = False

            for i in accounts:
                if i.email == email and\
                    i.password == password:
                        data_checked = True
                        resp = redirect("/")
                        resp.set_cookie("name", quote(i.user.name))
                        resp.set_cookie("email", i.email)
                        resp.set_cookie("products", i.user.products)
                        return resp
                
            if data_checked == False:
                return render(request, "sign-in.html", 
                    {"text": forb, "form": uform},
                    status=403
                )

def sign_out(request):
    resp = redirect("/")
    resp.delete_cookie("name")
    resp.delete_cookie("email")
    resp.delete_cookie("products")
    return resp

def sign_up(request):
    return render(request, "sign-up.html", 
        {"text": "Sign up", "form": aform}
    )

def try_sign_up(request):
    if request.method == "POST":
        usform = AccountForm(request.POST)
        if usform.is_valid():
            email = usform.cleaned_data["email"]
            password = usform.cleaned_data["password"]
            name = usform.cleaned_data["name"]

            if not Account.objects.filter(email=email).exists():
                user = User.objects.create(name=name, products="")
                account = Account.objects.create(
                    email=email, 
                    password=password,
                    user=user
                )
                print("Registered: ", email, password, name)

                resp = redirect("/")
                resp.set_cookie("name", quote(name))
                resp.set_cookie("email", email)
                resp.set_cookie("products", user.products)                  
                return resp
            else:
                return render(request, "sign-up.html",
                    {"text": forb2, "form": aform}, status=403
                )
            
def cart_view(request):
    try:
        raw_name = request.COOKIES.get("name", "")
        name = unquote(raw_name) if raw_name else acc.user.name
    
        udata = {"name": name}
    except:
        udata = ""

    email = request.COOKIES.get("email")
    if not email:
        return redirect('/sign-in/')

    acc = Account.objects.filter(email=email).first()
    if not acc:
        return redirect('/sign-in/')

    cart, _ = Cart.objects.get_or_create(user=acc.user)

    return render(request, "cart.html", {
        "cart": cart,
        "udata": udata
    })  