/*
* Core logic/payment flow comes from 
* https://stripe.com/docs/payments/accept-a-payment
* 
* CSS comes from
* https://stripe.com/docs/js
*/

var stripePublicKey = $('#id_stripe_public_key').text().slice(1, -1);
var clientSecret = $('#id_client_secret').text().slice(1, -1);
var stripe = Stripe(stripePublicKey);
var elements = stripe.elements();

/* Must define style before creating card if doing this way*/
/* var style = {...}*/
/* var card = elements.create('card', {style: style});*/

/* CSS below directly from stripe.com */
var card = elements.create('card', {
    style: {
      base: {
        iconColor: '#000',
        color: '#000',
        fontWeight: '500',
        fontFamily: 'Roboto, Open Sans, Segoe UI, sans-serif',
        fontSize: '16px',
        fontSmoothing: 'antialiased',
        ':-webkit-autofill': {
          color: '#000',
        },
        '::placeholder': {
          color: '#000',
        },
      },
      invalid: {
        iconColor: '#FF0000',
        color: '#FF0000',
      },
    },
  });


// Handle realtime validation errors on card element

card.addEventListener('change', function(event) {
    var errorDiv = document.getElementById('card-errors');
    if (event.error) {
        var html = 
            `<span>${event.error.message}</span>`
        $(errorDiv).html(html);
    } else {
        errorDiv.textContent = '';
    }
    }
)

// Handle form submit event

var form = document.getElementById('payment-form');

form.addEventListener('submit', function(ev) {
  ev.preventDefault();
  card.update({'disabled': true});
  $('#submit-button').attr('disabled', true);
  $('#payment-form').fadeToggle(100);
  $('#loading-overlay').fadeToggle(100);
  stripe.confirmCardPayment(clientSecret, {
    payment_method: {
      card: card,
    }
  }).then(function(result) {
    if (result.error) {
      var errorDiv = document.getElementById('card-errors');
      var html = 
        `<span>${result.error.message}</span>`
      $(errorDiv).html(html);
      $('#payment-form').fadeToggle(100);
      $('#loading-overlay').fadeToggle(100);
      card.update({'disabled': false});
      $('#submit-button').attr('disabled', false);
    } else {
      if (result.paymentIntent.status === 'succeeded') {
        form.submit();
      }
    }
  })
})

card.mount('#card-element');