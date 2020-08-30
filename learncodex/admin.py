from django.contrib import admin

from django_summernote.admin import SummernoteModelAdmin
from .models import Course, Lesson, Author, Category, Tag, Subscription, CoursePrerequisite, Payment, CourseSection

# Apply summernote to all TextField in model.


class CourseModelAdmin(SummernoteModelAdmin):  # instead of ModelAdmin
    summernote_fields = ('discription',)
    exclude = ('slug', 'created_day', 'created_month', 'created_year',)

class LessonModel(SummernoteModelAdmin):
    summernote_fields = ('discription',)
    exclude = ('slug', )

admin.site.register(Course, CourseModelAdmin)
admin.site.register(Lesson,LessonModel)
admin.site.register(Subscription)
admin.site.register(Author)
admin.site.register(Category)
admin.site.register(Tag)
admin.site.register(CoursePrerequisite)
admin.site.register(Payment)
admin.site.register(CourseSection)