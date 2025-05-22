from django.contrib import admin
from django.urls import path
from home import views
from .views import dashboard, edit_profile
from .views import add_product, manage_products, edit_product, delete_product, product_list, product_detail
from django.contrib.auth import views as auth_views
from .views import CustomPasswordResetCompleteView
from .views import update_cart
from .views import payment_success
from .views import invoice_view
from .views import invoice_view





admin.site.site_header = "Kisan Login"
admin.site.site_title = "KISAN Admin Portal"
admin.site.index_title = "Welcome to KISAN Researcher Portal"

urlpatterns = [
    path("", views.splash, name='splash'),
    path("h", views.index, name='index'),
    path("LOGIN", views.farmer_login, name='farmer_login'),
    path('consumer_login', views.consumer_login, name='consumer_login'),
    path("signup", views.signup, name='signup'),
    path("logout", views.logout, name='logout'),
    path("product", views.product, name='product'),
    path("aboutus", views.aboutus, name='aboutus'),
    path('farmer-dashboard/', views.farmer_dashboard, name='farmer_dashboard'),
     path('farmer-orders/', views.farmer_orders, name='farmer_orders'),
    path("consumer_dashboard", views.consumer_dashboard, name='consumer_dashboard'),
    path('dashboard/', dashboard, name='dashboard'),
    path('edit-profile/', edit_profile, name='edit_profile'),
    path('dashboard_base', views.dashboard_base, name='dashboard_base'),
    path('consumer_dashboard', views.consumer_dashboard, name='consumer_dashboard'),
    path('consumer_order', views.consumer_order, name='consumer_order'),
    path('add-product/', add_product, name='add_product'),
    path('manage-products/', manage_products, name='manage_products'),
    path('edit-product/<int:product_id>/', edit_product, name='edit_product'),
    path('delete-product/<int:product_id>/', delete_product, name='delete_product'),
    path('products/', product_list, name='product_list'),
    path('products/<int:product_id>/', product_detail, name='product_detail'),
    path('product_management_guid', views.product_management_guid, name='product_management_guid'),

    # Password reset URLs
    path('password_reset/', auth_views.PasswordResetView.as_view(), name='password_reset'),
    path('password_reset/done/', auth_views.PasswordResetDoneView.as_view(), name='password_reset_done'),
    path('reset/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(), name='password_reset_confirm'),
    path('reset/done/', CustomPasswordResetCompleteView.as_view(), name='password_reset_complete'),
    path('add-to-cart/<int:product_id>/', views.add_to_cart, name='add_to_cart'),
    


    path('cart/', views.view_cart, name='cart_view'),
    path('cart/add/<int:product_id>/', views.add_to_cart, name='add_to_cart'),
    path('cart/remove/<int:cart_item_id>/', views.remove_from_cart, name='remove_from_cart'),
    path('cart/update/<int:cart_item_id>/', update_cart, name='update_cart'), 
    path('checkout/', views.checkout, name='checkout'),
    path('order-summary/', views.order_summary, name='order_summary'),
       path('payment/', views.payment_page, name='payment_page'),
    path('payment-success/', payment_success, name='payment_success'),
    path('track-order/<int:order_id>/', views.track_order, name='track_order'),
        path('help/', views.help_page, name='help'),
        path('cart/', views.view_cart, name='cart_view'),

    path('invoice/<int:order_id>/', invoice_view, name='invoice'),


        








 



    


    

    path('login/', views.login_redirect, name='login'),  # A view to redirect based on user type

]


