import stripe
from django.conf import settings
from django.db.models import Sum
from django.http.response import JsonResponse
from django.views.generic.base import TemplateView, View

from stripe_app.models import Item, Order
import json


class BuyItemView(View):
    def get(self, request, item_id, *args, **kwargs):
        domain_url = request.build_absolute_uri('/')
        stripe.api_key = settings.STRIPE_SECRET_KEY
        item = Item.objects.get(id=item_id)
        try:
            checkout_session = stripe.checkout.Session.create(
                success_url=f'{domain_url}success-payment',
                cancel_url=f'{domain_url}item/{item_id}',
                payment_method_types=['card'],
                mode='payment',
                line_items=[
                    {
                        'name': item.name,
                        'quantity': 1,
                        'currency': item.currency,
                        'amount': item.price * 100 // 1,
                    },
                ]
            )
            return JsonResponse({'sessionId': checkout_session['id']})
        except Exception as e:
            return JsonResponse({'error': str(e)})


class BuyOrderView(View):
    def get(self, request, order_id, *args, **kwargs):
        domain_url = request.build_absolute_uri('/')
        stripe.api_key = settings.STRIPE_SECRET_KEY
        order = Order.objects.filter(id=order_id).prefetch_related('items', 'tax').select_related('discount').first()
        tax_id, coupon_id = None, None
        if order.tax:
            tax_id = [tax_obj.stripe_tax_id for tax_obj in order.tax.all()]
        if order.discount:
            coupon_id = order.discount.stripe_coupon_id
        order_items = order.items.all()
        line_items = [
            {'name': item.name, 'quantity': 1, 'tax_rates': tax_id, 'currency': item.currency,
             'amount': item.price * 100 // 1} for item in order_items]
        try:
            checkout_session = stripe.checkout.Session.create(
                success_url=domain_url + 'success-payment',
                cancel_url=domain_url + 'order/' + order_id,
                payment_method_types=['card'],
                mode='payment',
                line_items=line_items,
                discounts=[{'coupon': coupon_id}],
            )
            return JsonResponse({'sessionId': checkout_session['id']})
        except Exception as e:
            return JsonResponse({'error': str(e)})


class ItemPageView(TemplateView):
    template_name = "item.html"

    def get_context_data(self, item_id, **kwargs):
        item = Item.objects.get(id=item_id)
        context = {'item_name': item.name,
                   'item_description': item.description,
                   'item_price': item.price,
                   'item_currency': item.currency}
        return context


class OrderPageView(TemplateView):
    template_name = "order.html"

    def get_context_data(self, order_id, **kwargs):
        order = Order.objects.filter(id=order_id).first()
        order_items = order.items.all()
        total_sum = order.items.aggregate(Sum('price'))['price__sum']
        context = {'order_items': order_items, 'total_sum': total_sum}
        return context


class CreatePaymentIntentView(View):
    def post(self, request, *args, **kwargs):
        order_id = json.loads(request.body).get('order_id')
        order = Order.objects.filter(id=order_id).first()
        total_sum = order.items.aggregate(Sum('price'))['price__sum'] * 100 // 1
        stripe.api_key = settings.STRIPE_SECRET_KEY
        intent = stripe.PaymentIntent.create(
            amount=total_sum,
            currency='usd',
            payment_method_types=['card'],
        )
        try:
            return JsonResponse({'clientSecret': intent.client_secret})
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=403)


class OrderWithPaymentIntentPageView(TemplateView):
    template_name = "order-with-payment-intent.html"

    def get_context_data(self, order_id, **kwargs):
        order = Order.objects.filter(id=order_id).first()
        order_items = order.items.all()
        total_sum = order.items.aggregate(Sum('price'))['price__sum']
        context = {'order_items': order_items, 'total_sum': total_sum}
        return context


class SuccessPaymentView(TemplateView):
    template_name = 'success-payment.html'
