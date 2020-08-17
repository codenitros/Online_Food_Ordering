from django.contrib import admin
from food.models import  (UserProfile,
                          Restaurant,
                          Offer,
                          Favourite,
                          Recipe,
                          Order ,
                          OrderItem,
                          Delivery,
                          PaymentInfo)


@admin.register(UserProfile)
class UserProfileAdmin(admin.ModelAdmin):
    list_display = ['user','phone', 'address']


@admin.register(Restaurant)
class RestaurantAdmin(admin.ModelAdmin):
    list_display = ['name','address','phone','rating', 'image']


@admin.register(Favourite)
class FavouriteAdmin(admin.ModelAdmin):
    list_display = ['user_name','res_name']




@admin.register(Offer)
class OfferAdmin(admin.ModelAdmin):
    list_display = ['name','value']


@admin.register(Recipe)
class RecipeAdmin(admin.ModelAdmin):
    list_display = ['restaurant_name','recipe_name','category','recipe_description','recipe_price', 'recipe_image']


class OrderItemInline(admin.TabularInline):
    model = OrderItem
    raw_id_fields = ['product']


@admin.register(Order)
class RecipeAdmin(admin.ModelAdmin):
    list_display = ['Oid','first_name', 'last_name', 'email',
                    'address', 'postal_code', 'city', 'paid']
    list_filter = ['paid']
    inlines = [OrderItemInline]

@admin.register(Delivery)
class RecipeAdmin(admin.ModelAdmin):
    list_display = ['Delivery_no','Dname','Drating','contact']


@admin.register(PaymentInfo)
class RecipeAdmin(admin.ModelAdmin):
    list_display = ['Pid','Cid','NetPrice']
