from django.contrib.auth.views import LogoutView, LoginView
from django.urls import path
from .views import PostsList, PostDetail, NewsCreate, NewsEdit, ArticleCreate, ArticleEdit, PostDelete, BaseRegisterView

urlpatterns = [
   path('news/', PostsList.as_view(), name='post_list'),
   path('news/<int:pk>/', PostDetail.as_view(), name='post_detail'),
   path('news/create/', NewsCreate.as_view(), name='news_create'),
   path('news/<int:pk>/edit/', NewsEdit.as_view(), name='news_edit'),
   path('news/<int:pk>/delete/', PostDelete, name='news_delete'),
   path('articles/create/', ArticleCreate.as_view(), name='article_create'),
   path('articles/<int:pk>/edit/', ArticleEdit.as_view(), name='article_edit'),
   path('articles/<int:pk>/delete/', PostDelete, name='article_delete'),
   path('login/',
        LoginView.as_view(template_name='sign/login.html'),
        name='login'),
   path('logout/',
        LogoutView.as_view(template_name='sign/logout.html'),
        name='logout'),
   path('signup/',
        BaseRegisterView.as_view(template_name='sign/signup.html'),
        name='signup'),
]