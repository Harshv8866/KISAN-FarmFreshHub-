from django import forms
from django.contrib.auth.forms import UserCreationForm, PasswordResetForm  # Import PasswordResetForm here
from .models import CustomUser, Product

# Custom User Creation Form
class CustomUserCreationForm(UserCreationForm):












    
    class Meta:
        model = CustomUser
        fields = ['username', 'first_name', 'last_name', 'email', 'user_type', 'profile_picture']

# Profile Update Form
class ProfileUpdateForm(forms.ModelForm):
    remove_picture = forms.BooleanField(required=False, label="Remove Profile Picture", initial=False)

    class Meta:
        model = CustomUser
        fields = ['profile_picture', 'first_name', 'last_name', 'email', 'remove_picture']

    def clean(self):
        cleaned_data = super().clean()
        remove_picture = cleaned_data.get('remove_picture')

        if remove_picture:
            self.instance.delete_profile_picture()

        return cleaned_data

# Product Form
class ProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = ['name', 'description', 'price', 'quantity', 'category','image']

    def clean_price(self):
        price = self.cleaned_data.get('price')
        if price <= 0:
            raise forms.ValidationError("Price must be a positive value.")
        return price

    def clean_quantity(self):
        quantity = self.cleaned_data.get('quantity')
        if quantity <= 0:
            raise forms.ValidationError("Quantity must be greater than zero.")
        return quantity

# Custom Password Reset Form
class CustomPasswordResetForm(PasswordResetForm):
    pass



# forms.py
from django import forms
from .models import ShippingAddress

class ShippingAddressForm(forms.ModelForm):
    class Meta:
        model = ShippingAddress
        fields = ['full_name', 'email', 'phone', 'country', 'city', 'address', 'postal_code']



from django import forms
from .models import Review, Product

class ReviewForm(forms.ModelForm):
    class Meta:
        model = Review
        fields = ['product', 'rating', 'comment']
        widgets = {
            'product': forms.Select(choices=[('', 'Overall Website Experience')] + [(product.id, product.name) for product in Product.objects.all()], attrs={'class': 'form-control'}),
            'rating': forms.Select(choices=[(i, str(i)) for i in range(1, 6)], attrs={'class': 'form-control'}),
            'comment': forms.Textarea(attrs={'class': 'form-control', 'rows': 3, 'placeholder': 'Write your review...'}),
        }

    product = forms.ModelChoiceField(queryset=Product.objects.all(), required=False, empty_label="Overall Website Experience")
