
from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.auth import views as auth_views
from .forms import LoginForm, MyPasswordChangeForm, MyPasswordResetForm, MySetPasswordForm

urlpatterns = [
    #path('', views.my_home, name='home'),
    path('', views.ProductView.as_view(), name='home'),
    path('about/', views.my_about, name='about'),
    path('profile/', views.ProfileView.as_view(), name='profile'),
    path('orders/', views.orders, name='orders'),
    path('add-to-cart/', views.add_to_cart, name='add-to-cart'),
    path('cart/', views.show_cart, name='showcart'),
    path('pluscart/', views.plus_cart, name='plus_cart'),
    path('minuscart/', views.minus_cart, name='minus_cart'),
    path('removecart/', views.remove_cart, name='remove_cart'),




    path('accounts/login/', auth_views.LoginView.as_view(template_name='home/login.html', authentication_form=LoginForm), name='login'),
    path('logout/', auth_views.LogoutView.as_view(next_page='login'), name='logout'),
    path('registration/', views.CustomerRegistrationView.as_view(), name='customerregistration'),


    path('passwordchange/', auth_views.PasswordChangeView.as_view(template_name='home/passwordchange.html', form_class=MyPasswordChangeForm, success_url='/passwordchangedone/'), name='change_password'),
    path('passwordchangedone/', auth_views.PasswordChangeView.as_view(template_name='home/passwordchangedone.html'), name='passwordchangedone'),
    path('password-reset/', auth_views.PasswordResetView.as_view(template_name='home/password_reset.html', form_class=MyPasswordResetForm), name='password_reset'),
    path('password-reset/done/', auth_views.PasswordResetDoneView.as_view(template_name='home/password_reset_done.html'), name='password_reset_done'),
    path('password-reset-confirm/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(template_name='home/password_reset_confirm.html', form_class=MySetPasswordForm), name='password_reset_confirm'),
    path('password-reset-complete/', auth_views.PasswordResetCompleteView.as_view(template_name='home/password_reset_complete.html'), name='password_reset_complete'),



    path('paymentdone/', views.payment_done, name='paymentdone'),
    path('address/', views.address, name='address'),
    path('checkout/', views.checkout, name='checkout'),
    path('product-detail/<int:pk>', views.ProductDetailView.as_view(), name='product-detail'),
    path('buy/', views.buy_now, name='buy-now'),
    path('dryirons/', views.dry_irons, name='dryirons'),
    path('sandwitchmakers/', views.sandwitch_maker, name='sandwitchmakers'),
    path('handblender/', views.hand_blender, name='handblender'),
    path('juicers/', views.juicers, name='juicers'),
    path('mixersgrinders/', views.mixers_grinders, name='mixersgrinders'),
    path('foodprocessor/', views.food_processor, name='foodprocessor'),
    path('electrickettel/', views.electric_kettel, name='electrickettel'),
    path('services/', views.services, name='services'),
    path('contactus/', views.contactus, name='contactus'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
