from django.urls import path
from .views import PostsList, PostsDetail

urlpatterns = [
   path('news', PostsList.as_view()),
   path('news/<int:pk>', PostsDetail.as_view()),
]