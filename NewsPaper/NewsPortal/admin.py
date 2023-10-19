from django.contrib import admin

from NewsPortal.models import *


class PostAdmin(admin.ModelAdmin):
    model = Post

    list_display = ('post_author', 'topic', 'article_news', 'creation_time', 'post_rating')
    list_filter = ('post_author', 'article_news', 'post_category')
    search_fields = ('post_author', 'post_category')


class AuthorAdmin(admin.ModelAdmin):
    model = Author

    list_display = ('user', 'author_rating')
    list_filter = ('user', 'author_rating')
    search_fields = ('user', 'author_rating')


admin.site.register(Author, AuthorAdmin)
admin.site.register(Post, PostAdmin)
admin.site.register(Category)
admin.site.register(Comment)
admin.site.register(PostCategory)
