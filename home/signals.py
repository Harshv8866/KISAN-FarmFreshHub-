from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import Order, CartItem

# Signal that is triggered when an Order is created (saved)
@receiver(post_save, sender=Order)
def mark_cart_items_as_ordered(sender, instance, created, **kwargs):
    if created:
        # When an order is created, mark related cart items as ordered
        for cart_item in instance.cart.cart_items.all():
            cart_item.is_ordered = True
            cart_item.save()
