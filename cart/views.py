from django.shortcuts import render, redirect, get_object_or_404
from django.views.decorators.http import require_POST
from food.models import Recipe, Restaurant, OrderItem, Offer
from .cart import Cart
from food.forms import OrderCreateForm


@require_POST
def cart_add(request, recipe_id):
    cart = Cart(request)
    recipe = get_object_or_404(Recipe, id=recipe_id)
    cart.add(recipe=recipe)
    res_details = Restaurant.objects.filter(name=recipe.restaurant_name)
    try:
        off = Offer.objects.get(name=recipe.restaurant_name)
    except Offer.DoesNotExist:
        off = None
    for i in res_details:
        name = i.name
    recipe_details = Recipe.objects.filter(restaurant_name__name=name)
    total = cart.get_total_price()
    return render(request, 'food/restaurantmenu.html', {'cart': cart , 'res_details': res_details,
                                                        'recipe_details': recipe_details, 'total':total,'offer_price':off})


def cart_remove(request, recipe_id):
    cart = Cart(request)
    recipe = get_object_or_404(Recipe, id=recipe_id)
    cart.remove(recipe)
    res_details = Restaurant.objects.filter(name=recipe.restaurant_name)
    try:
        off = Offer.objects.get(name=recipe.restaurant_name)
    except Offer.DoesNotExist:
        off = None
    if res_details:
        for i in res_details:
            name = i.name
        recipe_details = Recipe.objects.filter(restaurant_name__name=name)
    return render(request, 'food/restaurantmenu.html', {'cart': cart, 'res_details': res_details,
                                                        'recipe_details': recipe_details,'offer_price':off})


def checkout(request):
    cart = Cart(request)
    if request.method == 'POST':
        form = OrderCreateForm(request.POST)
        if form.is_valid():
            order = form.save(commit=False)
            order.first_name = request.user.first_name
            order.last_name = ' '
            order.email = request.user.email
            order.save()
            for item in cart:
                OrderItem.objects.create(order=order,
                                         product=item['recipe'],
                                         price=item['price'])
            # clear the cart

            return render(request, 'food/thank_order.html',{'order': order})
    else:
        form = OrderCreateForm()
    total = cart.get_total_price()
    return render(request, 'food/checkout.html', {'cart': cart, 'total': total,'form':form})