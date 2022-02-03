
from django.urls import path
# Импорт представлений из "коробки" для реализации аутентификации
# Для его использования достаточно в файле конфигурации URL
# (приложения sign в этом примере) импортировать его и вставить в urlpatterns:
from django.contrib.auth.views import LoginView, LogoutView

from .views import upgrade_me, not_author


urlpatterns = [
    path('login/', LoginView.as_view(template_name='sign/login.html'),name='login'),
    path('logout/', LogoutView.as_view(template_name='sign/logout.html'), name='logout'),
    path('upgrade_me/', upgrade_me, name='author'),
    path('not_author/', not_author, name='not_author')
]