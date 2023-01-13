from django.contrib import admin
from django.utils.safestring import mark_safe
from ckeditor_uploader.widgets import CKEditorUploadingWidget

from django import forms
from .models import News, Category, Comment, ReplyComment


class NewsAdminForm(forms.ModelForm):
    content = forms.CharField(widget=CKEditorUploadingWidget())

    class Meta:
        model = News
        fields = '__all__'


class NewsAdmin(admin.ModelAdmin):
    form = NewsAdminForm
    list_display = ("id", "title", "category", "created_at", "updated_at", "is_published", "get_photo")
    list_display_links = ("id", "title")
    search_fields = ("title", "content")
    list_editable = ("is_published",)
    list_filter = ("is_published", "category")

    fields = ("title", "category", "content", "photo", "get_photo", "is_published", "views", "likes", "created_at",
              "updated_at",)
    readonly_fields = ("get_photo", "created_at", "updated_at")
    save_on_top = True

    def get_photo(self, object):
        if object.photo:
            return mark_safe(f'<img src="{object.photo.url}" width="50">')
        return 'Фото не установлено'

    get_photo.short_description = "Фото"

    save_as = True


class CategoryAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug': ('title',)}

    list_display = ("id", "title")
    list_display_links = ("id", "title")
    search_fields = ("title",)

    save_as = True


class CommentAdmin(admin.ModelAdmin):
    list_display = ("id", "name", "comment", "created_at", "post")
    list_display_links = ("id", "name")
    fields = ("name", "comment", "created_at", "news", "likes")
    readonly_fields = ("created_at",)


class ReplyCommentAdmin(admin.ModelAdmin):
    list_display = ("id", "name", "comment", "created_at", "parent_comment")
    list_display_links = ("id", "name")
    fields = ("name", "comment", "parent_comment", "created_at", "likes")
    readonly_fields = ("created_at",)


admin.site.register(Comment, CommentAdmin)
admin.site.register(ReplyComment, ReplyCommentAdmin)
admin.site.register(News, NewsAdmin)
admin.site.register(Category, CategoryAdmin)

admin.site.site_title = "Управление новостями"
admin.site.site_header = "Управление новостями"
