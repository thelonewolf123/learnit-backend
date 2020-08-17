from django.contrib import admin

from django_summernote.admin import SummernoteModelAdmin
from .models import Post, Author, Category, Comment, Tag

# Apply summernote to all TextField in model.


class PostModelAdmin(SummernoteModelAdmin):  # instead of ModelAdmin
    summernote_fields = ('content',)
    exclude = ('slug', 'created_day', 'created_month', 'created_year',)


admin.site.register(Post, PostModelAdmin)
admin.site.register(Author)
admin.site.register(Comment)
admin.site.register(Category)
admin.site.register(Tag)
