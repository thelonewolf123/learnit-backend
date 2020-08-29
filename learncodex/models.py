from django.db import models
from django.contrib.auth.models import User
from datetime import datetime
from django.utils.text import slugify
from django.dispatch import receiver
from django.db.models.signals import post_delete
from django.shortcuts import reverse
from django.core.validators import FileExtensionValidator, MaxValueValidator, MinValueValidator

from LearnIT.dropbox import DropboxStorage


free_paid = [['free', 'free'], ['paid', 'paid']]

DROPBOX_STORAGE = DropboxStorage()


class Category(models.Model):
    name = models.CharField(max_length=200, unique=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name_plural = "Categories"


class Tag(models.Model):
    name = models.CharField(max_length=200, unique=True)

    def __str__(self):
        return self.name


class Author(models.Model):
    user = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='instructor')
    name = models.CharField(max_length=200)
    discription = models.TextField(max_length=600)
    profile = models.ImageField(
        upload_to='learncodex/profile/', storage=DROPBOX_STORAGE)

    def __str__(self):
        return self.name


class Course(models.Model):
    title = models.CharField(max_length=200, unique=True)
    slug = models.SlugField(max_length=200, unique=True)
    title_img = models.ImageField(
        null=False, upload_to='learnIT/images', storage=DROPBOX_STORAGE)
    author = models.ForeignKey(
        Author, on_delete=models.CASCADE, related_name='course_list')
    category = models.ForeignKey(Category, on_delete=models.DO_NOTHING)
    price = models.IntegerField(null=True)
    course_type = models.CharField(max_length=5, choices=free_paid)
    updated_on = models.DateTimeField(auto_now=True)
    tags = models.CharField(max_length=200, unique=True)
    short_disc = models.TextField(max_length=600)
    discription = models.TextField(max_length=10000)
    created_day = models.CharField(null=False, max_length=4)
    created_month = models.CharField(null=False, max_length=40)
    created_year = models.CharField(null=False, max_length=5)

    class Meta:
        ordering = ['-id']

    def __str__(self):
        return self.title

    def _get_unique_slug(self):
        slug = slugify(self.title)
        unique_slug = slug
        num = 1
        while Course.objects.filter(slug=unique_slug).exists():
            unique_slug = '{}-{}'.format(slug, num)
            num += 1
        return unique_slug

    def _get_month(self, month):
        monthDict = {1: 'Jan', 2: 'Feb', 3: 'Mar', 4: 'Apr', 5: 'May', 6: 'Jun',
                     7: 'Jul', 8: 'Aug', 9: 'Sep', 10: 'Oct', 11: 'Nov', 12: 'Dec'}

        return monthDict[int(month)]

    def get_absolute_url(self):
        return reverse('course-detail', args=(self.slug,))

    def seo_discription(self):

        if len(self.short_disc) > 155:

            return self.short_disc[:150] + '...'

        return self.short_disc

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = self._get_unique_slug()
        today = datetime.today()
        self.created_day = str(today.day)
        self.created_month = self._get_month(str(today.month))
        self.created_year = str(today.year)

        super().save(*args, **kwargs)

# class DropboxToken(models.Model):
#     course = models.ForeignKey(Course, on_delete=models.CASCADE)
#     db_oauth_token = models.CharField(max_length=200, unique=True)

#     def __str__(self):

#         return f"{self.db_oauth_token}   [ {self.course.title} ]"


class CoursePrerequisite(models.Model):
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    prerequisite = models.CharField(max_length=600, null=False)

    def __str__(self):

        return f"{self.prerequisite}   [ {course.title} ]"


class CourseSection(models.Model):
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    title = models.CharField(max_length=600, null=False)

    def __str__(self):

        return self.title


class Lesson(models.Model):

    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    slug = models.SlugField(max_length=650, unique=True)
    title = models.CharField(max_length=600, null=False)
    youtube_url = models.CharField(max_length=100, null=True)
    discription = models.TextField(max_length=10000, null=False)
    video_720p = models.FileField(upload_to='course/learnIT/video_720p', validators=[
                                  FileExtensionValidator(allowed_extensions=['mp4', 'webm'])], null=True, blank=True, storage=DROPBOX_STORAGE)
#     video_480p = models.FileField(upload_to='course/learnIT/video_480p/', validators=[
#                                   FileExtensionValidator(allowed_extensions=['mp4', 'webm'])])
#     video_260p = models.FileField(upload_to='course/learnIT/video_260p/', validators=[
#                                   FileExtensionValidator(allowed_extensions=['mp4', 'webm'])])

    def __str__(self):

        return f'{self.title} ({self.course.title})'

    # def get_storage(self):

    #     token = DropboxToken.objects.get(course=self.course)
    #     CustomDropboxStorage = DropboxStorage(token.db_oauth_token)
    #     return CustomDropboxStorage

    def _get_unique_slug(self):
        slug = slugify(self.title)
        unique_slug = slug
        num = 1
        while Lesson.objects.filter(slug=unique_slug).exists():
            unique_slug = '{}-{}'.format(slug, num)
            num += 1
        return unique_slug

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = self._get_unique_slug()

        super().save(*args, **kwargs)


class Comment(models.Model):
    lesson = models.ForeignKey(Lesson, on_delete=models.CASCADE)
    name = models.CharField(null=False, blank=False, max_length=30)
    email = models.EmailField(max_length=200)
    subject = models.CharField(null=False, blank=False, max_length=200)
    message = models.TextField(null=False, max_length=700)
    created_day = models.CharField(null=False, max_length=4)
    created_month = models.CharField(null=False, max_length=40)
    created_year = models.CharField(null=False, max_length=5)

    def _get_month(self, month):
        monthDict = {1: 'Jan', 2: 'Feb', 3: 'Mar', 4: 'Apr', 5: 'May', 6: 'Jun',
                     7: 'Jul', 8: 'Aug', 9: 'Sep', 10: 'Oct', 11: 'Nov', 12: 'Dec'}

        return monthDict[int(month)]

    def save(self, *args, **kwargs):
        today = datetime.today()
        self.created_day = str(today.day)
        self.created_month = self._get_month(str(today.month))
        self.created_year = str(today.year)

        super().save(*args, **kwargs)

    def __str__(self):
        return self.message


class Review(models.Model):

    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    comment = models.TextField(max_length=600, null=True)
    rating = models.FloatField(
        validators=[MinValueValidator(0.0), MaxValueValidator(10.0)], null=False, blank=False)
    created_date = models.DateField(auto_now_add=True)

    def __str__(self):

        return f'{self.rating} [ {self.course.title} ]'


class Subscription(models.Model):

    course = models.ForeignKey(Course, on_delete=models.DO_NOTHING)
    user = models.ForeignKey(User, on_delete=models.DO_NOTHING)
    created_date = models.DateField(auto_now_add=True)

    def __str__(self):

        return self.user.username


class Payment(models.Model):
    subscription = models.ForeignKey(Subscription, on_delete=models.DO_NOTHING)
    amount = models.IntegerField(null=False)
    currency = models.CharField(max_length=10, null=False)
    razorpay_payment_id = models.CharField(max_length=100, null=False)
    razorpay_order_id = models.CharField(max_length=100, null=False)

    def __str__(self):

        return f'{self.subscription.course.title} - Rs. { self.amount }'


@receiver(post_delete, sender=Lesson)
def submission_delete(sender, instance, **kwargs):
    instance.video_720p.delete(False)
#     instance.video_480p.delete(False)
#     instance.video_260p.delete(False)
