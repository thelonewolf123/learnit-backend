from django.contrib import admin

from django_summernote.admin import SummernoteModelAdmin
from .models import FreeCourse, FreeLesson, Author, Category, Tag

# Apply summernote to all TextField in model.


class CourseModelAdmin(SummernoteModelAdmin):  # instead of ModelAdmin
    summernote_fields = ('discription',)
    exclude = ('slug', 'created_day', 'created_month', 'created_year',)

class LessonModel(SummernoteModelAdmin):
    summernote_fields = ('discription',)
    exclude = ('slug', )

admin.site.register(FreeCourse, CourseModelAdmin)
admin.site.register(FreeLesson,LessonModel)
admin.site.register(Author)
admin.site.register(Category)
admin.site.register(Tag)