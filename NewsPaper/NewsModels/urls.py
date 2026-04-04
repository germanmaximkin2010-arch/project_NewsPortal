from django.urls import path
from .views import *


urlpatterns = [
    path('', PostList.as_view(), name = 'post_list'),
    path('news/create/', PostCreate.as_view()),
    path('articles/create/', PostCreate.as_view()),
    path('news/<int:pk>/update/', PostUpdate.as_view()),
    path('articles/<int:pk>/update/', PostUpdate.as_view()),
    path('news/<int:pk>/delete/', PostDelete.as_view()),
    path('articles/<int:pk>/delete/', PostDelete.as_view()),
    path('<int:pk>', OnePost.as_view(), name = 'post_detail'),
]