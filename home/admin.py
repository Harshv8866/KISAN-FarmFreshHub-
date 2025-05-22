from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import CustomUser, Product, Cart, CartItem, ShippingAddress

class CustomUserAdmin(UserAdmin):
    model = CustomUser
    list_display = ('username', 'email', 'first_name', 'last_name', 'user_type')
    search_fields = ('username', 'email')
    ordering = ('username',)
    fieldsets = UserAdmin.fieldsets + (
        (None, {'fields': ('user_type',)}),
    )
    add_fieldsets = UserAdmin.add_fieldsets + (
        (None, {'fields': ('user_type',)}),
    )

admin.site.register(CustomUser, CustomUserAdmin)

class ProductAdmin(admin.ModelAdmin):
    list_display = ('name', 'farmer', 'price', 'quantity', 'created_at', 'image', 'quantity')
    list_filter = ('farmer',)
    search_fields = ('name', 'description')
    ordering = ('-created_at',)

admin.site.register(Product, ProductAdmin)

# Make Cart read-only in admin
class CartAdmin(admin.ModelAdmin):
    readonly_fields = [f.name for f in Cart._meta.fields]
    list_display = ('user', 'created_at')

    def has_add_permission(self, request):
        return False

    def has_delete_permission(self, request, obj=None):
        return False

admin.site.register(Cart, CartAdmin)

# Make CartItem read-only in admin
class CartItemAdmin(admin.ModelAdmin):
    readonly_fields = [f.name for f in CartItem._meta.fields]
    list_display = ('cart', 'product', 'quantity')

    def has_add_permission(self, request):
        return False

    def has_delete_permission(self, request, obj=None):
        return False

admin.site.register(CartItem, CartItemAdmin)

# Make ShippingAddress read-only in admin
from django.contrib import admin
from .models import CustomUser, Product, Cart, CartItem, ShippingAddress

class ShippingAddressAdmin(admin.ModelAdmin):
    readonly_fields = [f.name for f in ShippingAddress._meta.fields]
    list_display = ('user', 'full_name', 'email', 'phone', 'country', 'city','address', 'postal_code')
    
    def has_add_permission(self, request):
        return False

    def has_delete_permission(self, request, obj=None):
        return False

admin.site.register(ShippingAddress, ShippingAddressAdmin)



from .models import Review  # ADD THIS

class ReviewAdmin(admin.ModelAdmin):  # ADD THIS BLOCK
    list_display = ('user', 'product', 'rating', 'comment', 'created_at')
    list_filter = ('rating', 'created_at', 'product')
    search_fields = ('user__username', 'product__name', 'comment')
    ordering = ('-created_at',)

admin.site.register(Review, ReviewAdmin)  # ADD THIS


from django.contrib import admin
from .models import Order  # Make sure the path is correct

class OrderAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'amount', 'is_paid', 'created_at')
    list_filter = ('is_paid', 'created_at')
    search_fields = ('user__username', 'payment_id')
    readonly_fields = [f.name for f in Order._meta.fields]

    def has_add_permission(self, request):
        return False  # Optional: prevent manual addition from admin

    def has_delete_permission(self, request, obj=None):
        return False  # Optional: prevent deletion from admin

admin.site.register(Order, OrderAdmin)
