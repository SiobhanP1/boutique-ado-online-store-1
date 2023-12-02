from django.http import HttpResponse


class StripeWH_Handler:
    """Handle Stripe webhooks"""
    def __init__(self, request):
        self.request = request #So can access any attributes of request if needed

    def handle_event(self, event):
        """Handle generic/unknown/unexpected webhook events"""
        return HttpResponse(
            content=f'Webhook received: {event['type']}',
            status=200)