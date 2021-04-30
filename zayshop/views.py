from smtplib import SMTPException
from django.http import HttpResponse
from django.views import generic
from .models import Food, Drink, CartItem
from django.urls import reverse_lazy
from django.shortcuts import redirect, render
from django.contrib.auth import authenticate, login, logout
from django.views.generic import View
from .forms import UserForm, ProfileForm, EmailForm
from django.contrib.auth.models import User
from django.core.mail import send_mail
from django.http import Http404


class HomeView(generic.TemplateView):
    template_name = 'zayshop/home.html'


class OrderView(generic.TemplateView):
    template_name = 'zayshop/order.html'

    def get_context_data(self, **kwargs):
        context = super(OrderView, self).get_context_data(**kwargs)
        context['food_list'] = Food.objects.all()
        context['drink_list'] = Drink.objects.all()
        return context


class ContactUsFormView(View):
    form_email = EmailForm
    template_name = 'zayshop/contact_us.html'

    def get(self, request):
        form = self.form_email()
        return render(request, self.template_name, {'form_email': form})

    def post(self, request):
        form = self.form_email(request.POST)
        if form.is_valid():
            from_email = form.cleaned_data['from_email']
            subject = form.cleaned_data['subject']
            message = form.cleaned_data['message']
            try:
                send_mail(subject, message, from_email, ['bassfoodpizza@gmail.com'], fail_silently=False)
            except SMTPException:
                return HttpResponse('Invalid')

        return render(request, self.template_name, {'form_email': self.form_email(None),
                                                    'success_message': 'You successfully send your message. Thanks!'})


def add_to_cart(request, pk, name):
    template_name = 'zayshop/order.html'
    user = request.user
    food_list_name = [food.food_name for food in Food.objects.all()]
    drink_list_name = [drink.drink_name for drink in Drink.objects.all()]
    if user.is_authenticated:
        food_flag = False
        drink_flag = False
        try:
            food = Food.objects.get(id=pk)
            if name in food_list_name:
                cart_item_food = CartItem()
                cart_item_food.user = user
                cart_item_food.name = food.food_name
                cart_item_food.price = food.food_price
                cart_item_food.details = food.food_details
                cart_item_food.photo = food.food_photo
                cart_item_food.category = 'food'
                cart_item_food.save()
        except Food.DoesNotExist:
            food_flag = True

        try:
            drink = Drink.objects.get(id=pk)
            if name in drink_list_name:
                cart_item_drink = CartItem()
                cart_item_drink.user = user
                cart_item_drink.name = drink.drink_name
                cart_item_drink.price = drink.drink_price
                cart_item_drink.photo = drink.drink_photo
                cart_item_drink.category = 'drink'
                cart_item_drink.save()
        except Drink.DoesNotExist:
            drink_flag = True

        if food_flag and drink_flag:
            raise Http404
        else:
            return redirect('zayshop:order')
    else:
        return render(request, template_name, {'error_message': 'You must be logged in to make an order!',
                                               'food_list': Food.objects.all(),
                                               'drink_list': Drink.objects.all()})


def orderedRedirectView(request, pk):
    user = User.objects.get(id=pk)
    if user.is_active:
        if user.cartitem_set.all().count() != 0:
            try:
                send_mail('django test mail', 'test test', 'bassfoodpizza@gmail.com', [user.email])
            except SMTPException:
                return HttpResponse('Invalid')
            user.cartitem_set.all().delete()
            user.save()
        else:
            return render(request, 'zayshop/order_cart.html',
                          {'error_message': 'Please select your order first.'})

        return render(request, 'zayshop/order_succesfull.html')


class AddView(generic.TemplateView):
    template_name = 'zayshop/add.html'


class OrderCartView(generic.DetailView):
    template_name = 'zayshop/order_cart.html'
    model = User


class FoodView(generic.ListView):
    template_name = 'zayshop/food.html'
    model = Food
    context_object_name = 'food_list'
    paginate_by = 3


class FoodCreateView(generic.CreateView):
    model = Food
    fields = ['food_name', 'food_price', 'food_details', 'food_photo']
    template_name = 'zayshop/food_template.html'
    success_url = reverse_lazy('zayshop:add_food')


class FoodDeleteView(generic.DeleteView):
    model = Food
    success_url = reverse_lazy('zayshop:food')


class FoodUpdateView(generic.UpdateView):
    model = Food
    fields = ['food_name', 'food_price', 'food_details', 'food_photo']
    template_name = 'zayshop/food_template.html'
    success_url = reverse_lazy('zayshop:food')


class DrinkView(generic.ListView):
    template_name = 'zayshop/drink.html'
    model = Drink
    context_object_name = 'drink_list'
    paginate_by = 3


class DrinkCreateView(generic.CreateView):
    model = Drink
    fields = ['drink_name', 'drink_price', 'drink_photo']
    template_name = 'zayshop/drink_template.html'
    success_url = reverse_lazy('zayshop:add_drink')


class DrinkDeleteView(generic.DeleteView):
    model = Drink
    success_url = reverse_lazy('zayshop:drink')


class DrinkUpdateView(generic.UpdateView):
    model = Drink
    fields = ['drink_name', 'drink_price', 'drink_photo']
    template_name = 'zayshop/drink_template.html'
    success_url = reverse_lazy('zayshop:drink')


class PizzaView(generic.DetailView):
    template_name = 'zayshop/pizzadetail.html'
    model = Food


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
