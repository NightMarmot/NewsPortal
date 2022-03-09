from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.views.generic.edit import CreateView
from django.contrib.auth.models import Group
from django.contrib.auth.decorators import login_required

# импортируем нашу модель-форму для регистрации
from .models import BaseRegisterForm
from News.models import Author


class BaseRegisterView(CreateView):
    model = User  # модель формы, которую реализует данный дженерик;
    form_class = BaseRegisterForm  # форма, которая будет заполняться пользователем;
    success_url = '/'  # URL, на который нужно направить пользователя после успешного ввода данных в форму.


@login_required
def upgrade_me(request):
    # мы получили объект текущего пользователя из переменной запроса
    user = request.user
    # Вытащили author-группу из модели Group
    author_group = Group.objects.get(name='authors')
    # проверяем, находится ли пользователь в этой группе
    if not request.user.groups.filter(name='authors').exists():
        # если он все-таки еще не в ней — смело добавляем.
        author_group.user_set.add(user)
        Author.objects.create(authors_user=user)
    return redirect('/')


@login_required
def not_author(request):
    user = request.user
    user_id = request.user.pk
    print(user_id)
    author_delete = Author.objects.get(authors_user=user)
    authors_group = Group.objects.get(name='authors')
    if request.user.groups.filter(name='authors').exists():
        authors_group.user_set.remove(user)
        author_delete.delete()
    return redirect('/account/profile/')