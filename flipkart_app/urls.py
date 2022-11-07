from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.auth import views as auth_views
from .forms import LoginForm,MyPasswordChangeForm,MyPasswordResetForm,SetPasswordForm

urlpatterns = [
    # path('',views.home),
    path('',views.ProductView.as_view(), name='home'),
    # path('product-detail/',views.product_detail, name='product-detail'),
    path('product-detail/<int:pk>', views.ProductDetailView.as_view(), name='product-detail'),
    path('add-to-cart/',views.add_to_cart, name='add-to-cart'),
    path('cart/',views.show_cart, name='showcart'),
    path('pluscart/',views.plus_cart, name='pluscart'),
    path('minuscart/',views.minus_cart, name='minuscart'),
    path('removecart/',views.remove_cart, name='removecart'),
    path('buy/',views.buy_now, name='buy-now'),
    path('checkout/',views.checkout, name='checkout'),
    path('paymentdone/',views.payment_done, name='paymentdone'),
    # path('login/',views.login, name='login'),
    path('accounts/login/', auth_views.LoginView.as_view(template_name ='login.html', authentication_form=LoginForm), name='login'),
    path('logout/',auth_views.LogoutView.as_view(next_page='login'), name='logout'),
    path('passwordchange/',auth_views.PasswordChangeView.as_view(template_name='password-change.html', form_class=MyPasswordChangeForm, success_url='/passwordchangedone/'), name='passwordchange'),
    path('passwordchangedone/',auth_views.PasswordChangeView.as_view(template_name='passwordchangedone.html'),name='passwordchangedone'),
    path('passwordreset/',auth_views.PasswordResetView.as_view(template_name='password-reset.html', form_class=MyPasswordResetForm), name='passwordreset'),
    path('passwordreset/done', auth_views.PasswordResetDoneView.as_view(template_name='password-reset-done.html'),name='password_reset_done'),
    path('passwordreset-confirm/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(template_name='password-reset-confirm.html', form_class=SetPasswordForm),name='password_reset_confirm'),
    path('passwordreset-complete',auth_views.PasswordResetCompleteView.as_view(template_name='password-reset-complete.html'),name='password_reset_complete'),

    # path('customer-registration/',views.customer_registration, name='customer-registration'),
    path('customer-registration/',views.CustomerRegistrationView.as_view(), name='customer-registration'),
    # path('profile/',views.profile, name='profile'),
    path('profile/',views.CustomerProfileView.as_view(), name='profile'),
    path('search/',views.search, name='search'),
    path('product//<int:pk>',views.ProductDetailView.as_view(), name='product'),
    path('address/',views.address, name='address'),
    path('order/',views.order, name='order'),
    path('mobile/',views.mobile, name='mobile'),
    path('mobile/<slug:data>',views.mobile, name='mobile_data'),
    path('laptop/', views.laptop, name='laptop'),
    path('laptop/<slug:data>', views.laptop, name='laptop_data'),
    path('topwears/', views.topwear, name='topwears'),
    path('topwears/<slug:data>', views.topwear, name='topwears_data'),
    path('bottomwears/', views.bottomwear, name='bottomwears'),
    path('bottomwears/<slug:data>', views.bottomwear, name='bottomwears_data'),


    ] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)