from django.shortcuts import render, reverse, redirect
from django.contrib import messages

from .forms import OrderForm


def checkout(request):
    bag = request.session.get('bag', {})
    if not bag:
        messages.error(request, 'Nothing in bag')
        return redirect(reverse('products'))

    order_form = OrderForm()
    template = 'checkout/check_out.html'
    context = {
        'order_form': order_form,
        'stripe_public_key': 'pk_test_51OHuq7B93WdcdSYuxhoUQzkacDz38iQQwFUwS3Ml9kP1nHSbNwg77meRFHs6w7gE2nYgP1wvCY2M5bXpuPxBeEqa00YckBBfTt',
        'client_secret': 'test secret key',
    }

    return render(request, template, context)