import os
from django.core.mail import send_mail
from django.core.mail import EmailMessage
from django.conf import settings
from django.template.loader import render_to_string

from celery import shared_task
from rest_framework import viewsets,status
from .models import Order

@shared_task
def order_created(order_id):
    """
    Task to send an e-mail notification when an order is
    successfully created.
    """
    order = Order.objects.get(id=order_id)
    subject = 'Order number {}'.format(order.id)
    message = 'Dear {},\n\nYou have successfully placed an order.\
                Your order id is {}.'.format(order.first_name,
                                             order.id)
    # mail_sent = send_mail(subject,
    #                       message,
    #                       'django-shop-tutorial@myshop.com',
    #                       [order.email])
    print(order)
    # 電子郵件內容樣板
    email_template = render_to_string(
        os.path.join(settings.BASE_DIR, 'orders/templates/order_success_email.html'),
        {'username': 'request.user.username'}
    )
    email = EmailMessage(
        '訂單成功通知信',  # 電子郵件標題
        email_template,  # 電子郵件內容
        settings.EMAIL_HOST_USER,  # 寄件者
        ['alanccl92@gmail.com']  # 收件者
    )
    email.fail_silently = False
    email.send()

    # return mail_sent
