"""RanksTest URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from django.views.decorators.csrf import csrf_exempt

from stripe_app.views import ItemPageView, SuccessPaymentView, BuyOrderView, OrderPageView, \
    CreatePaymentIntentView, OrderWithPaymentIntentPageView, BuyItemView

app_name = "stripe_app"

urlpatterns = [
    path('admin/', admin.site.urls),
    path('buy/<item_id>', BuyItemView.as_view()),
    path('item/<item_id>', ItemPageView.as_view()),
    path('success-payment/', SuccessPaymentView.as_view()),
    path('order/buy/<order_id>', BuyOrderView.as_view()),
    path('order/<order_id>', OrderPageView.as_view()),
    path('order/pi/<order_id>', OrderWithPaymentIntentPageView.as_view()),
    path('create-payment-intent/', csrf_exempt(CreatePaymentIntentView.as_view())),
]
