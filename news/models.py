from django.contrib.auth.models import User
from django.db import models
from django.urls import reverse


class ReplyComment(models.Model):
    parent_comment = models.ForeignKey("Comment", related_name="get_parent_comments", on_delete=models.CASCADE)

    name = models.CharField(max_length=50, verbose_name="Имя_отвечающего")
    comment = models.CharField(max_length=700, verbose_name="Коментарий_отвечающего")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Дата создания")

    likes = models.ManyToManyField(User, related_name="get_reply_comments_likes", blank=True)

    def __str__(self):
        return f'{self.name} - {self.comment}'

    class Meta:
        verbose_name = "Ответный_Коментарий"
        verbose_name_plural = "Ответные_Коментарии"
        ordering = ["name"]


class Comment(models.Model):
    news = models.ForeignKey("News", related_name="get_comments", on_delete=models.CASCADE)

    name = models.CharField(max_length=50, verbose_name="Имя")
    comment = models.CharField(max_length=700, verbose_name="Коментарий")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Дата создания")

    likes = models.ManyToManyField(User, related_name="likes_comments", blank=True)

    def __str__(self):
        return f'{self.name} - {self.comment}'

    class Meta:
        verbose_name = "Коментарий"
        verbose_name_plural = "Коментарии"
        ordering = ["name"]


class Category(models.Model):
    title = models.CharField(max_length=150, db_index=True, verbose_name="Наименование категории")
    slug = models.SlugField(max_length=255, verbose_name='Url_of_Slug', unique=True)

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse("category", kwargs={"slug": self.slug})

    class Meta:
        verbose_name = "Категория(ю)"
        verbose_name_plural = "Категории"
        ordering = ["title"]


class News(models.Model):
    title = models.CharField(max_length=150, verbose_name="Наименование")
    content = models.TextField(verbose_name="Материал", blank=True)
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Дата Публикации")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="Обновлено")
    photo = models.ImageField(upload_to='photos/%Y/%m/%d/', verbose_name="Фото", blank=True)
    is_published = models.BooleanField(default=True, verbose_name="Опубликовано")
    category = models.ForeignKey(Category, on_delete=models.PROTECT, null=True, verbose_name="Категория")
    views = models.ManyToManyField(User, related_name="views_news", blank=True)
    likes = models.ManyToManyField(User, related_name="get_likes", blank=True)

    def get_absolute_url(self):
        return reverse("detail_news", kwargs={"pk": self.pk})

    def total_likes(self):
        return self.likes.count()

    def total_views(self):
        return self.views.count()

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = "Новость"
        verbose_name_plural = "Новости"
        ordering = ["-created_at"]
