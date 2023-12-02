from django.conf import settings
from django.http import HttpResponse
from django.views.decorators.http import require_POST
from django.views.decorators.csrf import csrf_exempt

from checkout.webhook_handler import StripeWH_Handler

import stripe

@require_POST
@csrf_exempt
def webhook(request):
    """"""
    #Set up
    wh_secret = settings.STRIPE_WH_SECRET
    stripe.api_key = settings.STRIPE_API_KEY

    # Get webhook data and verify signature
    payload = request.body
    sig_header = request.META['HTTP_STRIPE_SIGNATURE']
    event = None

    try: 
        event = stripe.webhook.construct_event(
            payload, sig_header, wh_secret)
    except ValueError as e:
        # Invalid payload
        return HttpResponse(status=400)
    except stripe.error.SignatureVerificationError as e:
        # Invalid signature
        return HttpResponse(status=400)
    except Exception as e:
        return HttpResponse(content=e, status=400)

    # print('Success')
    # return HttpResponse(status=200)

    # Set up webhook handler
    handler = StripeWH_Handler(request)

    # Map webhook events to relevant handler functions
    event_map = {
        'payment_intent.succeeded': handler.handle_payment_intent_succeeded,
        'payment_intent.payment_failed': handler.handle_payment_intent_payment_failed,
    }

    # Get webhook type from Stripe
    event_type = event['type']

    # if handler exists for that type, get it from event_map (using event_type)
    # Use generic handler by default (default option=handler.handle_event)
    # Default used if first not successful / not there
    event_handler = event_map.get(event_type, handler.handle_event)

    # Call event handler with event
    response = event_handler(event)
    return response
