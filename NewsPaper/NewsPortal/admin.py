from django.contrib import admin

from NewsPortal.models import *

admin.site.register(Author)
admin.site.register(Post)
admin.site.register(Category)
admin.site.register(Comment)
admin.site.register(PostCategory)
