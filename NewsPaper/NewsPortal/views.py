from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.http import HttpResponseRedirect, HttpResponse
from django.shortcuts import render, get_object_or_404

# Create your views here.

from datetime import datetime

from django.urls import reverse_lazy, reverse
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView, TemplateView

from .filters import PostFilter
from .forms import ArticleNewsForm
from .models import Post, Category
from django.contrib.auth.models import User, Group
from .models import BaseRegisterForm
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect


class PostsList(ListView):
    model = Post
    ordering = 'creation_time'
    template_name = 'posts.html'
    context_object_name = 'posts'
    paginate_by = 4

    def get_queryset(self):
        queryset = super().get_queryset()
        self.filterset = PostFilter(self.request.GET, queryset)
        return self.filterset.qs

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['filterset'] = self.filterset
        return context


class PostDetail(DetailView):
    model = Post
    template_name = 'post.html'
    context_object_name = 'post'


class NewsCreate(PermissionRequiredMixin, CreateView):
    permission_required = 'NewsPortal.add_post'
    form_class = ArticleNewsForm
    model = Post
    template_name = 'post_create_edit.html'

    def form_valid(self, form):
        post = form.save(commit=False)
        post.article_news = 'NOV'
        return super().form_valid(form)


class NewsEdit(LoginRequiredMixin, PermissionRequiredMixin, UpdateView):
    permission_required = 'NewsPortal.change_post'
    form_class = ArticleNewsForm
    model = Post
    template_name = 'post_create_edit.html'

    def form_valid(self, form):
        post = form.save(commit=False)
        if post.article_news == 'STA':
            return HttpResponse('Такой статьи не существует')
        post.save()
        return super().form_valid(form)


class ArticleCreate(PermissionRequiredMixin, CreateView):
    permission_required = 'NewsPortal.add_post'
    form_class = ArticleNewsForm
    model = Post
    template_name = 'article_create_edit.html'

    def form_valid(self, form):
        post = form.save(commit=False)
        post.article_news = 'STA'
        return super().form_valid(form)


class ArticleEdit(LoginRequiredMixin, PermissionRequiredMixin, UpdateView):
    permission_required = 'NewsPortal.change_post'
    form_class = ArticleNewsForm
    model = Post
    template_name = 'article_create_edit.html'

    def form_valid(self, form):
        post = form.save(commit=False)
        if post.article_news == 'NOV':
            return HttpResponse('Такой новости не существует')
        post.save()
        return super().form_valid(form)


def PostDelete(request, pk):
    article = Post.objects.get(id=pk)
    article.delete()
    return HttpResponseRedirect(reverse('post_list'))


class BaseRegisterView(CreateView):
    model = User
    form_class = BaseRegisterForm
    success_url = '/news'


@login_required
def upgrade_me(request):
    user = request.user
    premium_group = Group.objects.get(name='authors')
    if not request.user.groups.filter(name='authors').exists():
        premium_group.user_set.add(user)
    return redirect('news/')


class IndexView(LoginRequiredMixin, TemplateView):
    template_name = 'posts.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['is_not_author'] = not self.request.user.groups.filter(name='authors').exists()
        return context


class CategoryListView(PostsList):
    model = Post
    template_name = 'templates/category_list.html'
    context_object_name = 'category_news_list'

    def get_queryset(self):
        self.category = get_object_or_404(Category, id=self.kwargs['pk'])
        queryset = Post.objects.filter(category=self.category).order_by('-created_at')
        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['is_not_subscriber'] = self.request.user not in self.category.subscribers.all()
        context['category'] = self.category
        return context


@login_required
def subscribe(request, pk):
    user = request.user
    category = Category.objects.get(id=pk)
    category.subscribers.add(user)

    message = 'Вы успешно подписались на рассылку новостей категории'
    return render(request, 'templates/subscribe.html', {'category': category, 'message': message})