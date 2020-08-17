from django.db import models
from django.conf import settings
import uuid

# from phonenumber_field.modelfields import PhoneNumberField


class UserProfile(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    phone = models.CharField(max_length=10)
    address = models.CharField(max_length=30)

    def __str__(self):
        return format(self.user.username)


class Favourite(models.Model):
    user_name = models.ForeignKey('UserProfile', on_delete=models.CASCADE)
    res_name = models.ForeignKey('Restaurant', on_delete=models.CASCADE)
    is_favourite = models.BooleanField(default=False)

    @classmethod
    def create(cls, is_favourite):
        fav = cls(is_favourite=is_favourite)
        return fav

    class Meta:
        unique_together = ("user_name", "res_name")


class Restaurant(models.Model):
    name = models.CharField(max_length=20, unique=True)
    rating = models.IntegerField(default=0)
    image = models.ImageField(upload_to='restoimgs', blank=True)
    phone = models.CharField(max_length=10)
    address = models.CharField(max_length=30)

    def __str__(self):
        return format(self.name)


class Offer(models.Model):
    name = models.OneToOneField('Restaurant', on_delete=models.CASCADE)
    value = models.IntegerField(default=0)

    def __str__(self):
        return format(self.name)


class Recipe(models.Model):
    restaurant_name = models.ForeignKey('Restaurant', on_delete=models.CASCADE)
    recipe_name = models.CharField(max_length=20)
    recipe_description = models.CharField(max_length=20)
    recipe_price = models.IntegerField(default=0)
    recipe_image = models.ImageField(upload_to='recipe_imgs', blank=True)
    category = models.CharField(max_length=20, default=' ')

    class Meta:
        verbose_name_plural = "recipes"


class Order(models.Model):
    Oid = models.UUIDField(default=uuid.uuid4,unique=True, editable=False)
    first_name = models.CharField(max_length=50,default='')
    last_name = models.CharField(max_length=50,default='')
    email = models.EmailField(null=True)
    address = models.CharField(max_length=250,default='')
    postal_code = models.CharField(max_length=20,default='')
    city = models.CharField(max_length=100,default='')
    paid = models.BooleanField(default=False)

    class Meta:
        verbose_name_plural = "orders"

    def __str__(self):
        return format(self.first_name)


class OrderItem(models.Model):
    order = models.ForeignKey(Order, related_name='items', on_delete=models.CASCADE)
    product = models.ForeignKey(Recipe, related_name='order_items', on_delete=models.CASCADE)
    price = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return '{}'.format(self.id)

    def get_cost(self):
        return self.price


class Delivery(models.Model):
    Delivery_no = models.IntegerField(primary_key=True)
    Dname = models.CharField(max_length=20)
    Drating = models.IntegerField(default=0)
    contact = models.CharField(max_length=10)

    class Meta:
        verbose_name_plural = "deliveries"


class PaymentInfo(models.Model):
    Cid = models.ForeignKey('UserProfile', on_delete=models.CASCADE)
    Pid = models.CharField(max_length=40)
    mode = models.CharField(max_length=20)
    NetPrice = models.IntegerField(default=0)

    @classmethod
    def create(cls,mode):
        payment = cls(mode=mode)
        return payment

    class Meta:
        verbose_name_plural = "payments"




