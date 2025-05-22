from django.shortcuts import render , HttpResponse , redirect
from django.shortcuts import get_object_or_404

from django.contrib import messages
from django.contrib.auth import authenticate , login
from .models import CustomUser 
from django.contrib.auth import get_user_model
User = get_user_model()



# Create your views here.

def splash(request):
   
    return render(request, 'splash.html')
    #return HttpResponse("this is home page")
    
def index(request):
   
    products = Product.objects.all()[:10]  # show first 8 products
    return render(request, 'index.html', {'products': products})


from django.shortcuts import render, redirect
from django.contrib import messages
from .models import CustomUser

def signup(request):
    if request.method == 'POST':
        # Extract form data
        username = request.POST.get('username')
        first_name = request.POST.get('fname')
        last_name = request.POST.get('lname')
        email = request.POST.get('email')
        password = request.POST.get('password')
        password2 = request.POST.get('password2')
        user_type = request.POST.get('user_type')

        # Debug print to check if values are being captured
        print(f"Username: {username}, First Name: {first_name}, Last Name: {last_name}, Email: {email}, User Type: {user_type}")

        # Check if passwords match
        if password != password2:
            messages.error(request, "Passwords do not match.")
            return redirect('signup')  # Redirect to signup page if passwords don't match

        # Check if username already exists
        if CustomUser.objects.filter(username=username).exists():
            messages.error(request, "Username already taken. Please choose a different one.")
            return redirect('signup')  # Redirect back to the signup page

        try:
            # Create user
            user = CustomUser.objects.create_user(
                username=username,
                password=password,
                email=email,
                first_name=first_name,
                last_name=last_name,
                user_type=user_type
            )
            user.save()
            messages.success(request, "Account created successfully!")
            return redirect('login')  # Redirect to login page after successful signup
        except Exception as e:
            messages.error(request, f"Error: {e}")
            return redirect('signup')  # Redirect back if there's an error

    return render(request, 'signup.html')




from .models import Product

def product(request):
    products = Product.objects.all()
    return render(request, 'product.html', {'products': products})


 

def farmer_login(request):
    if request.method == "POST":
        username = request.POST["username"]
        password = request.POST["password"]

        user = authenticate(username=username, password=password)
        
        if user is not None:
            # Check if user is a farmer
            if user.user_type == "farmer":
                login(request, user)
                return redirect('farmer_dashboard')  # Redirect to the farmer dashboard
            else:
                messages.error(request, "You are not a farmer. Please use the consumer login page.")
                return redirect('consumer_login')  # Redirect to the consumer login page
        else:
            messages.error(request, "Invalid credentials. Please try again.")
            return redirect('farmer_login')  # Redirect back to the farmer login page

    return render(request, 'farmer_login.html')



def consumer_login(request):
    if request.method == "POST":
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(username=username, password=password)

        if user is not None:
            if user.user_type == "consumer":
                login(request, user)
                print(f"User {user.username} logged in successfully with first name: {user.first_name}")  # Debug print
                return redirect('consumer_dashboard')  
            else:
                messages.error(request, "You are not a consumer. Please use the farmer login page.")
                return redirect('farmer_login')  
        else:
            messages.error(request, "Invalid credentials. Please try again.")
            return redirect('consumer_login')  

    return render(request, 'consumer_login.html')




def aboutus(request):
    return render(request, 'aboutus.html', )

def dashboard_base(request):
    return render(request, 'dashboard_base.html', )

from django.shortcuts import render, redirect
from .models import Product, Order, ShippingAddress, Review
from .forms import ShippingAddressForm, ReviewForm

def consumer_dashboard(request):
    all_products = list(Product.objects.all())
    shipping_address = ShippingAddress.objects.filter(user=request.user).first()
    orders = Order.objects.filter(user=request.user).order_by('-created_at')
    address = ShippingAddress.objects.filter(user=request.user).first()

    index = request.session.get('product_index', 0)
    products_to_show = all_products[index:index + 4]

    if index + 4 >= len(all_products):
        request.session['product_index'] = 0
    else:
        request.session['product_index'] = index + 4

    # ✅ Always define the forms initially
    form = ShippingAddressForm(instance=shipping_address)
    review_form = ReviewForm()

    if request.method == 'POST':
        if 'update_address' in request.POST:
            if shipping_address:
                form = ShippingAddressForm(request.POST, instance=shipping_address)
            else:
                form = ShippingAddressForm(request.POST)

            if form.is_valid():
                address = form.save(commit=False)
                address.user = request.user
                address.save()
                return redirect('checkout')

        elif 'submit_review' in request.POST:
            review_form = ReviewForm(request.POST)
            if review_form.is_valid():
                review = review_form.save(commit=False)
                review.user = request.user
                review.save()
                return redirect('consumer_dashboard')

    return render(request, 'consumer_dashboard.html', {
        'products': products_to_show,
        'orders': orders,
        'address': address,
        'form': form,
        'review_form': review_form,
    })

def consumer_order(request):
        orders = Order.objects.filter(user=request.user).order_by('-created_at')

        return render(request, 'consumer_order.html', { 'orders': orders})

def logout(request):
    return render(request,  )

from django.shortcuts import render
from .models import Order, Cart
from django.contrib.auth.decorators import login_required

@login_required
def farmer_orders(request):
    # Get the logged-in farmer
    farmer = request.user
    products = Product.objects.filter(farmer=farmer)
    
 # Get all cart items where the product belongs to this farmer
    cart_items = CartItem.objects.filter(product__farmer=farmer)

    # Get unique orders associated with the farmer's products
    orders = Order.objects.all().order_by('-created_at')

    context = {
        'products': products,
        'cart_items': cart_items,
        'orders': orders,
    }
    return render(request, 'farmer_orders.html', context)





from django.shortcuts import render
from .models import Product, CartItem, Order
from django.contrib.auth.decorators import login_required

from django.shortcuts import render
from .models import Product, CartItem, Order
from django.contrib.auth.decorators import login_required

from django.db.models import Prefetch

@login_required
def farmer_dashboard(request):
    farmer = request.user

    products = Product.objects.filter(farmer=farmer)

    cart_items = CartItem.objects.filter(product__farmer=farmer)

    # Efficiently fetch related orders
    orders = Order.objects.all().order_by('-created_at')


    context = {
        'products': products,
        'cart_items': cart_items,
        'orders': orders,
    }

    return render(request, 'farmer_dashboard.html', context)




    





# views.py
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .forms import ProfileUpdateForm

def dashboard(request):
    user = request.user
    context = {'user': user}
    if user.user_type == 'farmer':
        return render(request, 'farmer_dashboard.html', context)
    else:
        return render(request, 'consumer_dashboard.html', context)

@login_required
def edit_profile(request):
    if request.method == 'POST':
        form = ProfileUpdateForm(request.POST, request.FILES, instance=request.user)
        if form.is_valid():
            form.save()
            return redirect('dashboard')
    else:
        form = ProfileUpdateForm(instance=request.user)
    return render(request, 'edit_profile.html', {'form': form})



# product add farmer
from .forms import ProductForm

@login_required
def add_product(request):
    if request.method == "POST":
        form = ProductForm(request.POST, request.FILES)
        if form.is_valid():
            product = form.save(commit=False)
            product.farmer = request.user  # Assign logged-in farmer
            product.save()
            return redirect('manage_products')  # Redirect after successful submission
    else:
        form = ProductForm()
    return render(request, 'add_product.html', {'form': form})


# for manage the products


from .models import Product

@login_required
def manage_products(request):
    if request.user.user_type != "farmer":
        return render(request, '403.html')  # Restrict access if not a farmer

    products = Product.objects.filter(farmer=request.user)
    return render(request, 'manage_products.html', {'products': products})


# edit product



@login_required
def edit_product(request, product_id):
    product = get_object_or_404(Product, id=product_id, farmer=request.user)  # Ensure only the owner can edit
    
    if request.method == "POST":
        form = ProductForm(request.POST, request.FILES, instance=product)
        if form.is_valid():
            form.save()
            return redirect('manage_products')  # Redirect to product management page
    else:
        form = ProductForm(instance=product)

    return render(request, 'edit_product.html', {'form': form, 'product': product})


# delete product

@login_required
def delete_product(request, product_id):
    product = get_object_or_404(Product, id=product_id, farmer=request.user)  # Only allow deletion if owned
    
    if request.method == "POST":
        product.delete()
        return redirect('manage_products')

    return render(request, 'confirm_delete.html', {'product': product})


#product list 


from django.shortcuts import render
from .models import Product

def product_list(request):
    category_filter = request.GET.get('category')
    
    vegetables = Product.objects.filter(category='vegetables')
    fruits = Product.objects.filter(category='fruits')
    seeds = Product.objects.filter(category='seeds')
    fertilizer = Product.objects.filter(category='fertilizer')

    if category_filter:
        # Filter products based on the selected category
        products_by_category = {
            'vegetables': vegetables,
            'fruits': fruits,
            'seeds': seeds,
            'fertilizer': fertilizer
        }
from django.shortcuts import render
from .models import Product

def product_list(request):
    category_filter = request.GET.get('category')  # Get category from URL parameter

    # If a category is selected, filter products by that category
    if category_filter:
        filtered_products = Product.objects.filter(category=category_filter)
    else:
        # Show all products if no category filter is applied
        filtered_products = Product.objects.all()

    return render(request, 'product_list.html', {
        'filtered_products': filtered_products,  # Pass filtered products (all if no filter)
        'category_filter': category_filter,  # Pass the current category filter
    })


# product detail 


from django.shortcuts import render, get_object_or_404
from .models import Product

def product_detail(request, product_id):
    # Get the product object by its ID
    product = get_object_or_404(Product, id=product_id)
    
    return render(request, 'product_detail.html', {
        'product': product,
    })







# product_,management_guid

def product_management_guid(request):
    return render(request, 'product_management_guid.html', )




from django.contrib.auth.tokens import default_token_generator
from django.utils.http import urlsafe_base64_encode
from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.conf import settings
from django.shortcuts import render, redirect
from django.contrib.auth.models import User

from django.core.mail import send_mail, BadHeaderError
from django.http import HttpResponse

def send_password_reset_email(user):
    try:
        context = {
            'user': user,
            'protocol': 'http',
            'domain': '127.0.0.1:8000',
            'uid': urlsafe_base64_encode(force_bytes(user.pk)), # type: ignore
            'token': default_token_generator.make_token(user),
        }

        html_message = render_to_string('password_reset_email.html', context)
        plain_message = f"Reset your password: http://127.0.0.1:8000/reset/{context['uid']}/{context['token']}"

        send_mail(
            subject="Password Reset Request",
            message=plain_message,
            from_email=settings.EMAIL_HOST_USER,
            recipient_list=[user.email],
            html_message=html_message,
        )
    except BadHeaderError:
        return HttpResponse('Invalid header found.')
    except Exception as e:
        print(f"Email Error: {e}")  # Debugging




# views.py (add a new view)
from django.shortcuts import render

def password_reset_done(request):
    return render(request, 'password_reset_done.html')




from django.contrib.auth.views import PasswordResetCompleteView
from django.urls import reverse_lazy

class CustomPasswordResetCompleteView(PasswordResetCompleteView):
    def get_success_url(self):
        return reverse_lazy('farmer_login')  # Or 'consumer_login' depending on your use case

from django.shortcuts import redirect

def login_redirect(request):
    # Redirect users based on their type
    if request.user.user_type == 'farmer':
        return redirect('farmer_login')  # Redirect to farmer login
    else:
        return redirect('consumer_login')  # Redirect to consumer login


from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .models import Product, Cart, CartItem

@login_required
def add_to_cart(request, product_id):
    product = get_object_or_404(Product, id=product_id)

    if request.method == 'POST':
        try:
            quantity_requested = int(request.POST.get('quantity', 1))  # Default to 1 if no quantity is provided
        except (ValueError, TypeError):
            messages.error(request, "Please enter a valid quantity.")
            return redirect('product_detail', product_id=product.id)

        print(f"Quantity Requested: {quantity_requested}")  # Print the value here to debug

        # Check if the quantity is at least 1
        if quantity_requested < 1:
            messages.error(request, "Quantity must be at least 1.")
            return redirect('product_detail', product_id=product.id)

        # Check if the quantity requested is greater than available stock
        cart, created = Cart.objects.get_or_create(user=request.user)

        # Calculate the total quantity of this product in the cart
        total_quantity_in_cart = sum(
            item.quantity for item in cart.cart_items.filter(product=product)
        )

        # Check if adding this quantity exceeds the available stock
        if total_quantity_in_cart + quantity_requested > product.quantity:
            messages.error(
                request,
                f"Only {product.quantity - total_quantity_in_cart} Kg of {product.name} is available. Please enter a lower quantity."
            )
            return redirect('product_detail', product_id=product.id)

        # If product exists in the cart, update its quantity, else create a new CartItem
        cart_item, created = CartItem.objects.get_or_create(cart=cart, product=product)

        if not created:
            cart_item.quantity += quantity_requested
        else:
            cart_item.quantity = quantity_requested
            cart_item.price = product.price  # Set the price for the new CartItem

        # Save the CartItem
        cart_item.save()

        # Success message
        messages.success(request, f"{quantity_requested} Kg of {product.name} added to your cart.")
        return redirect('cart_view')  # Redirect to the cart page or any other page


from django.shortcuts import render
from .models import Cart

from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from .models import Cart

@login_required
def view_cart(request):
    cart, created = Cart.objects.get_or_create(user=request.user)
    cart_items = cart.cart_items.all()
    total_price = sum(item.total_price() for item in cart_items)

    return render(request, 'cart/view_cart.html', {
        'cart': cart,
        'cart_items': cart_items,
        'total_price': total_price
    })

# views.py
from django.shortcuts import redirect
from .models import CartItem

from django.shortcuts import redirect, get_object_or_404
from django.contrib import messages
from .models import CartItem, Product

def update_cart(request, cart_item_id):
    cart_item = get_object_or_404(CartItem, id=cart_item_id)
    new_quantity = int(request.POST.get('quantity', 1))  # Get new quantity from form input
    available_stock = cart_item.product.quantity  # Get available stock from Product model

    if new_quantity > available_stock:
        messages.error(request, f"Only {available_stock} {cart_item.product.name}(s) are available.")
    else:
        cart_item.quantity = new_quantity
        cart_item.save()
        messages.success(request, "Cart updated successfully.")

    return redirect("cart_view")  # Redirect back to the cart page



# views.py
from django.shortcuts import redirect
from .models import CartItem

@login_required
def remove_from_cart(request, cart_item_id):
    cart_item = CartItem.objects.get(id=cart_item_id)
    cart_item.delete()
    return redirect('cart_view')




from django.shortcuts import render, redirect
from .models import Cart, CartItem, ShippingAddress  # Ensure all relevant models are imported
from .forms import ShippingAddressForm  # Import form if needed



@login_required
def checkout(request):
    shipping_address = ShippingAddress.objects.filter(user=request.user).first()
    is_update = request.GET.get('update') == 'true'

    if request.method == 'POST':
        if shipping_address:
            form = ShippingAddressForm(request.POST, instance=shipping_address)
        else:
            form = ShippingAddressForm(request.POST)

        if form.is_valid():
            address = form.save(commit=False)
            address.user = request.user  # ✅ Assign the user to avoid IntegrityError
            address.save()
            return redirect('checkout')
    else:
        form = ShippingAddressForm(instance=shipping_address) if shipping_address else ShippingAddressForm()

    cart = Cart.objects.filter(user=request.user).first()
    if cart:
        cart_items = cart.cart_items.filter(is_ordered=False)
        total_price = sum(item.total_price() for item in cart_items)

        for item in cart_items:
            item.is_ordered = True
            item.save()

        cart.is_ordered = True
        cart.save()
    else:
        cart_items = []
        total_price = 0

    context = {
        'form': form,
        'shipping_address': shipping_address,
        'is_update': is_update,
        'cart_items': cart_items,
        'total_price': total_price,
    }

    return render(request, 'checkout.html', context)



from django.shortcuts import render
from .models import Cart

def order_summary(request):
    cart = Cart.objects.filter(user=request.user).first()

    if not cart:
        return render(request, 'order_summary.html', {'message': 'Your cart is empty.'})

    total_price = sum(item.total_price() for item in cart.cart_items.all())

    return render(request, 'order_summary.html', {
        'cart': cart,
        'total_price': total_price
    })   







import razorpay
from django.conf import settings
from django.shortcuts import render
from .models import Cart

import razorpay
from django.conf import settings
from django.shortcuts import render, redirect
from .models import Cart
from django.contrib.auth.decorators import login_required

from django.shortcuts import render, redirect
from django.conf import settings
from django.http import HttpResponseBadRequest
import razorpay
from .models import Cart, CartItem
from django.shortcuts import render, redirect
from django.http import HttpResponse
from .models import Cart
import razorpay
from django.conf import settings

import razorpay
from django.conf import settings
from django.http import HttpResponse

def payment_page(request):
    user = request.user
    cart = Cart.objects.filter(user=user).first()

    if not cart or not cart.cart_items.exists():
        return redirect('cart')

    total = cart.total_price()

    if total is None or total < 1:
        return HttpResponse("⚠️ Cart total must be at least ₹1 to proceed with payment.")

    client = razorpay.Client(auth=(settings.RAZORPAY_KEY_ID, settings.RAZORPAY_KEY_SECRET))

    try:
        razorpay_order = client.order.create({
            "amount": int(total * 100),  # Razorpay expects paise
            "currency": "INR",
            "payment_capture": "1"
        })
    except razorpay.errors.BadRequestError as e:
        # Log the error response for better troubleshooting
        print("Razorpay Error:", e)
        return HttpResponse(f"Razorpay Error: {e}")
    except Exception as e:
        # Catch any other general errors
        print("Error during Razorpay order creation:", e)
        return HttpResponse(f"An unexpected error occurred: {e}")

    context = {
        "cart": cart,
        "total": total,
        "razorpay_key_id": settings.RAZORPAY_KEY_ID,
        "razorpay_order": razorpay_order,
        "user": user
    }

    return render(request, 'payment/payment_page.html', context)





from django.shortcuts import render, redirect
from .models import Order, Cart, ShippingAddress
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse

@login_required
def payment_success(request):
    payment_id = request.GET.get('payment_id')

    try:
        cart = Cart.objects.get(user=request.user)
        shipping_address = ShippingAddress.objects.filter(user=request.user).last()
        amount = cart.total_price()

        # ✅ Create the order
        order = Order.objects.create(
            user=request.user,
            cart=cart,
            shipping_address=shipping_address,
            amount=amount,
            payment_id=payment_id,
            is_paid=True,
        )

        # ✅ Mark items as ordered and clear cart items
        for item in cart.cart_items.all():
            item.is_ordered = True
            item.save()
        
        # ✅ Clear cart items after order placed
        cart.cart_items.all().delete()

        return render(request, 'payment/payment_success.html', {'order': order})

    except Cart.DoesNotExist:
        return HttpResponse("No cart found for user.", status=404)


from django.shortcuts import get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import Order

@login_required
def track_order(request, order_id):
    order = get_object_or_404(Order, id=order_id, user=request.user)
    return render(request, 'track_order.html', {'order': order})

from django.shortcuts import render

def help_page(request):
    return render(request, 'help.html')



from django.shortcuts import render, get_object_or_404
from .models import Order

def invoice_view(request, order_id):
    order = get_object_or_404(Order, id=order_id, user=request.user)
    return render(request, 'invoice.html', {'order': order})



