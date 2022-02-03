from django.core.mail import EmailMultiAlternatives
# импортируем сигнал, который будет срабатывать после сохранения объекта в базу данных
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.shortcuts import redirect
from django.template.loader import render_to_string
from .models import Post, Category
from .views import sending_emails_to_subscribers


# создание сигнала
# оборачиваем в декоратор и выбираем тип сигнала и модель
@receiver(post_save, sender=Post)
# описываем функцию сигнала и передаем экземпляр модели
def send_emails_on_signal(sender, created, instance, **kwargs):
    # запускаем функцию представление
    sending_emails_to_subscribers(instance)