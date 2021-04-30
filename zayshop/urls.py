from django.urls import path
from . import views

app_name = 'zayshop'

urlpatterns = [
    path('', views.HomeView.as_view(), name=''),
    path('home/', views.HomeView.as_view(), name='home'),
    path('order/', views.OrderView.as_view(), name='order'),
    path('<int:pk>/ordered', views.orderedRedirectView, name='make_order'),
    path('<int:pk>/order-cart', views.OrderCartView.as_view(), name='order_cart'),
    path('<int:pk>/<str:name>/cart', views.add_to_cart, name='add_to_cart'),
    path('add/', views.AddView.as_view(), name='add_item'),
    path('food/', views.FoodView.as_view(), name='food'),
    path('add/add_food/', views.FoodCreateView.as_view(), name='add_food'),
    path('<int:pk>/delete-food', views.FoodDeleteView.as_view(), name='delete_food'),
    path('<int:pk>/edit_food/', views.FoodUpdateView.as_view(), name='edit_food'),
    path('food/<int:pk>/pizza-details', views.PizzaView.as_view(), name='pizza_details'),
    path('drink/', views.DrinkView.as_view(), name='drink'),
    path('add/add_drink/', views.DrinkCreateView.as_view(), name='add_drink'),
    path('<int:pk>/delete-drink', views.DrinkDeleteView.as_view(), name='delete_drink'),
    path('<int:pk>/edit_drink/', views.DrinkUpdateView.as_view(), name='edit_drink'),
    path('register/', views.UserRegisterFormView.as_view(), name='register'),
    path('login/', views.UserLoginFormView.as_view(), name='login'),
    path('logout/', views.UserLogoutView.as_view(), name='logout'),
    path('contact_us/', views.ContactUsFormView.as_view(), name='contact_us'),
    path('<int:pk>/profile-details', views.ProfileView.as_view(), name='profile'),

]
