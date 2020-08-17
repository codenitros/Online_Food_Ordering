from decimal import Decimal
from django.conf import settings
from food.models import Recipe,Offer
from django.shortcuts import  get_object_or_404
from django.core.exceptions import ObjectDoesNotExist
import json



'''
# Usage:
d = Decimal("42.5")
json.dumps(d, cls=DecimalEncoder)'''


class Cart(object):
    def __init__(self, request):
        """
        Initialize the cart.
        """
        self.session = request.session
        cart = self.session.get(settings.CART_SESSION_ID)
        if not cart:
            # save an empty cart in the session
            cart = self.session[settings.CART_SESSION_ID] = {}
        self.cart = cart

    def add(self, recipe):
        """
        Add a product to the cart or update its quantity.
        """
        recipe_id = str(recipe.id)
        res = get_object_or_404(Recipe, id=recipe_id)
        try:
            off = Offer.objects.get(name=res.restaurant_name)
        except Offer.DoesNotExist:
            off = None

        if off is not None:
            if recipe_id not in self.cart:
                self.cart[recipe_id] = {'name': str(recipe.recipe_name),'price': str(recipe.recipe_price - ((off.value/100) * recipe.recipe_price))}
        else:
            if recipe_id not in self.cart:
                self.cart[recipe_id] = {'name': str(recipe.recipe_name),'price': str(recipe.recipe_price)}
        self.save()

    def save(self):
        # mark the session as "modified" to make sure it gets saved
        self.session.modified = True

    def remove(self, recipe):
        """
        Remove a product from the cart.
        """
        recipe_id = str(recipe.id)
        if recipe_id in self.cart:
            del self.cart[recipe_id]
        self.save()

    def __iter__(self):
        """
        Iterate over the items in the cart and get the products
        from the database.
        """

        recipe_ids = self.cart.keys()
        # get the product objects and add them to the cart
        recipes = Recipe.objects.filter(id__in=recipe_ids)
        cart = self.cart.copy()
        for recipe in recipes:
            cart[str(recipe.id)]['recipe'] = recipe
        for item in cart.values():
            item['price'] = Decimal(item['price'])
            item['total_price'] = item['price']
            yield item

    def get_total_price(self):
        return sum(Decimal(item['price']) for item in self.cart.values())

    def clear(self):
        # remove cart from session
        del self.session[settings.CART_SESSION_ID]
        self.save()
