from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, redirect, render

from .forms import PaymentForm
from .models import Product, Cart, CartItem
from .services import process_payment, send_files_to_email


@login_required
def add_to_cart(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    cart, created = Cart.objects.get_or_create(user=request.user)
    cart_item, created = CartItem.objects.get_or_create(
        cart=cart,
        product=product
    )
    if not created:
        cart_item.quantity += 1
        cart_item.save()
    cart.total_price = sum(item.get_total_price() for item in cart.items.all())
    cart.save()
    return redirect('cart_detail')


@login_required
def cart_detail(request):
    cart, created = Cart.objects.get_or_create(user=request.user)
    if request.method == 'POST':
        form = PaymentForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data.get('email')
            payment_data = {
                'card_number': form.cleaned_data.get('card_number'),
                'card_expiry': form.cleaned_data.get('card_expiry'),
                'card_cvc': form.cleaned_data.get('card_cvc'),
            }
            success = process_payment(cart.total_price, payment_data)
            if success:
                send_files_to_email(cart, email)
                cart.items.all().delete()
                cart.total_price = 0
                cart.save()
                return render(request, 'success.html', {'email': email})
            else:
                form.add_error(None,
                               'Ошибка при обработке платежа. Пожалуйста, '
                               'проверьте введенные данные.')
    else:
        form = PaymentForm()
    return render(request, 'cart_detail.html', {'cart': cart, 'form': form})
