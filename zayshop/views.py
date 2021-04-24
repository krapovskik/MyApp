from django.views import generic
from .models import Food, Drink, CartItemFood, CartItemDrink
from django.urls import reverse_lazy
from django.shortcuts import redirect, render
from django.contrib.auth import authenticate, login, logout
from django.views.generic import View
from .forms import UserForm, ProfileForm
from django.contrib.auth.models import User


class HomeView(generic.TemplateView):
    template_name = 'zayshop/home.html'


class OrderView(generic.TemplateView):
    template_name = 'zayshop/order.html'

    def get_context_data(self, **kwargs):
        context = super(OrderView, self).get_context_data(**kwargs)
        context['food_list'] = Food.objects.all()
        context['drink_list'] = Drink.objects.all()
        return context


def add_to_cart(request, pk, name):
    template_name = 'zayshop/order.html'
    user = request.user
    food_list_name = [food.food_name for food in Food.objects.all()]
    drink_list_name = [drink.drink_name for drink in Drink.objects.all()]
    if user.is_authenticated:
        try:
            food = Food.objects.get(id=pk)
            if name in food_list_name:
                cart_item_food = CartItemFood()
                cart_item_food.user = user
                cart_item_food.food_id = food.id
                cart_item_food.save()
        except Food.DoesNotExist:
            pass
        try:
            drink = Drink.objects.get(id=pk)
            if name in drink_list_name:
                cart_item_drink = CartItemDrink()
                cart_item_drink.user = user
                cart_item_drink.drink_id = drink.id
                cart_item_drink.save()
        except Drink.DoesNotExist:
            pass
        return redirect('zayshop:order')
    else:
        return render(request, template_name, {'error_message': 'You must be logged in to make a order!',
                                               'food_list': Food.objects.all(),
                                               'drink_list': Drink.objects.all()})


class OrderCartView(generic.DetailView):
    template_name = 'zayshop/order_cart.html'
    model = User


class FoodView(generic.ListView):
    template_name = 'zayshop/food.html'
    model = Food
    context_object_name = 'food_list'
    paginate_by = 3


class DrinkView(generic.ListView):
    template_name = 'zayshop/drink.html'
    model = Drink
    context_object_name = 'drink_list'
    paginate_by = 3


class PizzaView(generic.DetailView):
    template_name = 'zayshop/pizzadetail.html'
    model = Food


class FoodDeleteView(generic.DeleteView):
    model = Food
    success_url = reverse_lazy('zayshop:food')


class DrinkDeleteView(generic.DeleteView):
    model = Drink
    success_url = reverse_lazy('zayshop:drink')


class ProfileView(generic.DetailView):
    template_name = 'zayshop/user_details.html'
    model = User


class UserRegisterFormView(View):
    form_class_user = UserForm
    form_class_profile = ProfileForm
    template_name = 'zayshop/register.html'

    def get(self, request):
        form_user = self.form_class_user(None)
        form_profile = self.form_class_profile(None)
        return render(request, self.template_name, {'form_user': form_user, 'form_profile': form_profile})

    def post(self, request):
        form_user = self.form_class_user(request.POST)
        form_profile = self.form_class_profile(request.POST)

        if form_user.is_valid() and form_profile.is_valid():

            user_form = form_user.save(commit=False)
            profile_form = form_profile.save(commit=False)

            username = form_user.cleaned_data['username']
            password = form_user.cleaned_data['password']
            user_form.set_password(password)
            user_form.save()
            profile_form.user = user_form
            profile_form.save()

            user = authenticate(username=username, password=password)

            if user is not None:
                if user.is_active:
                    login(request, user)
                    return redirect('zayshop:home')

        return render(request, self.template_name, {'form_user': form_user, 'form_profile': form_profile})


class UserLoginFormView(View):
    template_name = 'zayshop/login.html'

    def get(self, request):
        return render(request, self.template_name)

    def post(self, request):
        user = authenticate(username=request.POST['username'], password=request.POST['password'])
        if user is not None:
            if user.is_active:
                login(request, user)
                return redirect('zayshop:home')
        else:
            return render(request, self.template_name, {'error_message': 'Invalid login'})


class UserLogoutView(View):
    template_name = 'zayshop/logout.html'

    def get(self, request):
        user = request.user
        if user.is_authenticated:
            logout(request)
            return render(request, self.template_name, {'user': user})
