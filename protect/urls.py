from django.urls import path
from .views import IndexView

urlpatterns = [
    path('account/profile/', IndexView.as_view()),
]