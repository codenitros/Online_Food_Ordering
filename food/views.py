from django.shortcuts import render, get_object_or_404
from .models import (Restaurant, 
					UserProfile, 
					Favourite, 
					Offer,
					OrderItem,
					Recipe,
					Order,
					Delivery,
					PaymentInfo)

from django.contrib.auth.models import User
from .forms import UserRegistrationForm
from django.contrib.auth.decorators import login_required
from cart.cart import Cart

list_fav = []


@login_required
def home(request):
	if request.method == 'GET':
		pop_restaurants = Restaurant.objects.all().filter(rating__range=(4,5))
		avg_restaurants = Restaurant.objects.all().filter(rating__range=(1,3))
		offer_zone = Offer.objects.all()
		return render(request,'main/home.html',{'pop_restaurants':pop_restaurants,'avg_restaurants':avg_restaurants,'offer_zone':offer_zone })


def index(request):
	if request.method == 'GET':
		return render(request,'main/index.html')


def register(request):
	if request.method == 'POST':
		user_form = UserRegistrationForm(request.POST)
		if user_form.is_valid():
			new_user = user_form.save(commit=False)
# Set the chosen password
			new_user.set_password(
			user_form.cleaned_data['password'])
# Save the User object
			new_user.save()
			UserProfile.objects.create(user=new_user)
			return render(request, 'account/register_done.html', {'new_user': new_user})
	else:
		user_form = UserRegistrationForm()
	return render(request, 'account/register.html',{'user_form': user_form})


def contact(request):
	if request.method == 'GET':
		return render(request,'contact.html')


@login_required
def restaurants_view(request):
	if request.method == 'GET':
		favourites = Favourite.objects.filter(user_name__user=request.user)
		restaurants = Restaurant.objects.order_by('-rating').exclude(name__in=list_fav)
		return render(request, 'food/restaurants.html', {'restaurants': restaurants, 'favourites': favourites})


@login_required
def menu(request, parameter):
	if request.method == 'GET':
		res_details = Restaurant.objects.filter(name=parameter)
		res_name = Restaurant.objects.get(name=parameter)
		try:
			off = Offer.objects.get(name__name=res_name.name)
		except Offer.DoesNotExist:
			off = None
		cart = Cart(request)
		for i in res_details:
			name = i.name
		recipe_details = Recipe.objects.filter(restaurant_name__name=name)
		return render(request, 'food/restaurantmenu.html', {'cart': cart, 'res_details': res_details, 'recipe_details': recipe_details,'offer_price':off})


@login_required
def profile(request):
	if request.method == 'GET':
		pres_user = request.user
		fav_res = Favourite.objects.filter(user_name__user=pres_user)
		orders = OrderItem.objects.filter(order__first_name=request.user.first_name)
		return render(request, 'account/profile.html', {'fav_res': fav_res,'orders':orders})


@login_required
def offers(request):
	if request.method == 'GET':
		restaurants = Restaurant.objects.all()
		my_offers = Offer.objects.all()
		return render(request, 'food/offers.html', {'my_offers': my_offers, 'restaurants': restaurants})


@login_required
def search(request):
	query = request.GET.get("q")
	if query:
		queryset_list = Restaurant.objects.filter(name__istartswith=query)
	else:
		queryset_list = {}
	return render(request, 'food/search_result.html', {'queryset_list': queryset_list})


@login_required
def place(request, parameter):
	if request.method == 'GET':
		place_resto = Restaurant.objects.filter(address__icontains=parameter)
	return render(request, 'food/brands_place.html', {'place_resto': place_resto})


@login_required
def pay(request, parameter):
	cart = Cart(request)
	order = get_object_or_404(Order, Oid=parameter)
	total = cart.get_total_price()
	if request.method == 'POST':
		method = request.POST.get("pay")
		obj = get_object_or_404(UserProfile, user=request.user)
		#user = request.user.first_name
		new = PaymentInfo.create(mode=method)
		new.Cid = obj
		new.Pid = parameter
		new.NetPrice = total
		new.save()
		order.paid = True
		order.save()
		delivery = Delivery.objects.order_by("?").first()
		cart.clear()
		return render(request, 'food/order_cooking.html',{'delivery':delivery})
	return render(request, 'food/pay.html',{'order':order,'total':total})


def fav_add(request, parameter):

	favorite = get_object_or_404(Restaurant, name=parameter)

	if request.method == 'POST':
		obj = get_object_or_404(UserProfile, user=request.user)
		new = Favourite.create(is_favourite=True)
		new.res_name = favorite
		new.user_name = obj
		new.save()
		list_fav.append(parameter)
		favourites = Favourite.objects.filter(user_name__user = request.user)
		restaurants = Restaurant.objects.order_by('-rating').exclude(name__in=list_fav)
		return render(request,'food/restaurants.html', {'restaurants':restaurants,'favourites':favourites})


def fav_del(request,parameter):
	if request.method =='POST':
		rem = Favourite.objects.filter(res_name__name=parameter)
		rem.delete()
		list_fav.remove(parameter)
		favourites = Favourite.objects.filter(user_name__user = request.user)
		restaurants = Restaurant.objects.order_by('-rating').exclude(name__in=list_fav)
		return render(request,'food/restaurants.html', {'restaurants':restaurants,'favourites':favourites})


