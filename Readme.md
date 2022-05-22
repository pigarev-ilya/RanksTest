# Ranks Test App

## Инструкция по запуску (Используется Docker):
Добавить 'Publishable key' в static/js/stripe_payment_intent.js и static/js/stripe_session.js.  
Добавить. 'Secret key' в 'RanksTest/settings.py' необходимого аккаунта системы Stripe.  

Выполнить следующие комманды:  
1. Создайть образ и запустить контейнеры:  
docker-compose up -d --build  
2. Выполнить миграции:  
docker-compose exec web python manage.py makemigrations  
docker-compose exec web python manage.py migrate  
3. Создать супер-пользователя:  
docker-compose exec web python manage.py createsuperuser

### Демонстрация приложения онлайн.

Ссылка: https://ranks-test-pi.herokuapp.com/  
Superuser: login-admin, password-admin.

Функции:  
https://ranks-test-pi.herokuapp.com/item/1 - Покупка одного товара.  
https://ranks-test-pi.herokuapp.com/order/1 - Покупка нескольких товаров в одном заказе.  
https://ranks-test-pi.herokuapp.com/order/pi/1 - Покупка заказа с помощью Stripe Payment Intent.

