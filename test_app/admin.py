from django.contrib import admin
from .models import Rubric, Article


class CommentRubric(admin.ModelAdmin):
    list_display = ("name", "parent")


class CommentArticle(admin.ModelAdmin):
    list_display = ("name", "category")


admin.site.register(Rubric, CommentRubric)
admin.site.register(Article, CommentArticle)
