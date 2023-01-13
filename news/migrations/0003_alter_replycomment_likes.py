# Generated by Django 4.1.2 on 2023-01-11 08:16

from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('news', '0002_alter_category_options_alter_comment_news_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='replycomment',
            name='likes',
            field=models.ManyToManyField(blank=True, related_name='get_reply_comments_likes', to=settings.AUTH_USER_MODEL),
        ),
    ]