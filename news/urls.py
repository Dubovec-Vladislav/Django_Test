from django.urls import path
from .views import *
# from django.views.decorators.cache import cache_page

urlpatterns = [

    # path('', index, name="home"),
    # path('test/', test, name='test'),

    path('register/', RegisterUser.as_view(), name='register'),
    # path('register/', register, name='register'),

    # path('login/', user_login, name='login'),
    path('login/', Login.as_view(), name='login'),

    # path('logout/', user_logout, name='logout'),
    path('logout/', Logout.as_view(), name='logout'),

    # path('', cache_page(60)(HomeNews.as_view()), name='home'),
    path('', HomeNews.as_view(), name='home'),

    # path('category/<int:category_id>/', get_category, name='category'),
    path('category/<str:slug>/', NewsByCategory.as_view(), name='category'),

    # path('news/<int:news_id>/', view_news, name='view_news'),
    path('news/<int:pk>/', ViewNews.as_view(), name='detail_news'),

    # path('news/add-news/', add_news, name='add_news'),
    path('news/add-news/', CreateNews.as_view(), name='add_news'),

    path('news/<int:pk>/add-comment/', CreateComment.as_view(), name='add_comment'),

    path('news/<int:pk>/add-reply-comment/', CreateReplyComment.as_view(), name='add_reply_comment'),

    path('like/<int:pk>/', LikeView, name='like_news'),

    path('remove-like/<int:pk>/', RemoveLikeView, name='remove_like_news'),

    path('comment-like/<int:pk>/', CommentLikeView, name='like_comments'),

    path('reply-comment-like/<int:pk>/', ReplyCommentLikeView, name='like_reply_comments'),

    # path('view/<int:pk>/', ViewView, name='view_news'),

]
