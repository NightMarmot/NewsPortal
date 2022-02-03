from django.urls import path
from .views import PostList, PostDetail, FilterPostView, PostCreateView, PostDeleteView, PostUpdateView,\
    IndexView, add_subscribe

urlpatterns = [
    path('', PostList.as_view(), name='news'),
    path('<int:pk>', PostDetail.as_view(), name='news_detail'),
    path('search/', FilterPostView.as_view(), name='search'),
    path('create/', PostCreateView.as_view(), name='news_create'),
    path('create/<int:pk>', PostUpdateView.as_view(), name='news_update'),
    path('delete/<int:pk>', PostDeleteView.as_view(), name='news_delete'),
]