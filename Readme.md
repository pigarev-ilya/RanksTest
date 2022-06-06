# Ranks Test App
## Задача:
Реализовать Django + Stripe API бэкенд со следующим функционалом и условиями:  
-Django Модель Item с полями (name, description, price).   
-API с двумя методами:  
GET /buy/{id}, c помощью которого можно получить Stripe Session Id для оплаты выбранного Item. При выполнении этого метода c бэкенда с помощью python библиотеки stripe должен выполняться запрос stripe.checkout.Session.create(...) и полученный session.id выдаваться в результате запроса.  
GET /item/{id}, c помощью которого можно получить простейшую HTML страницу, на которой будет информация о выбранном Item и кнопка Buy. По нажатию на кнопку Buy должен происходить запрос на /buy/{id}, получение session_id и далее  с помощью JS библиотеки Stripe происходить редирект на Checkout форму stripe.redirectToCheckout(sessionId=session_id).  
-Запуск используя Docker.  
-Использование environment variables.  
-Просмотр Django Моделей в Django Admin панели.  
-Запуск приложения на удаленном сервере, доступном для тестирования.  
-Модель Order, в которой можно объединить несколько Item и сделать платёж в Stripe на содержимое Order c общей стоимостью всех Items.
-Модели Discount, Tax, которые можно прикрепить к модели Order и связать с соответствующими атрибутами при создании платежа в Stripe - в таком случае они корректно отображаются в Stripe Checkout форме.   
-Добавить поле Item.currency, создать 2 Stripe Keypair на две разные валюты и в зависимости от валюты выбранного товара предлагать оплату в соответствующей валюте
Реализовать не Stripe Session, а Stripe Payment Intent.


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

