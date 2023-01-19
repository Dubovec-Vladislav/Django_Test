from django.contrib.auth import login
# from django.http import HttpResponse
from django.shortcuts import redirect, get_object_or_404
from django.urls import reverse_lazy
from django.views.generic import ListView, DetailView, CreateView
from django.db.models import Sum, F
from django.contrib.auth.mixins import LoginRequiredMixin

from .models import News, Category, Comment, ReplyComment
from .forms import NewsForm, RegisterUserForm, LoginUserForm, CommentForm, ReplyCommentForm
from .utils import MyMixin

from django.contrib.auth.views import LoginView, LogoutView


# from django.core.mail import send_mail


class HomeNews(MyMixin, ListView):
    model = News
    template_name = 'news/home_news_list.html'
    context_object_name = 'news'
    paginate_by = 2

    # extra_context = {'title': 'Главная'}

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Главная страница'
        context['sum_views_list'] = Category.objects.annotate(sum_views=Sum("news__views"))
        return context

    def get_queryset(self):
        return News.objects.filter(is_published=True).select_related('category')


class NewsByCategory(MyMixin, ListView):
    model = News
    template_name = 'news/home_news_list.html'
    context_object_name = 'news'
    allow_empty = False
    paginate_by = 2

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = Category.objects.get(slug=self.kwargs['slug'])
        # context['sum_views_list'] = Category.objects.annotate(sum_views=Sum("news__views"))
        return context

    def get_queryset(self):
        return News.objects.filter(category__slug=self.kwargs['slug'], is_published=True)


class ViewNews(DetailView):
    model = News
    template_name = "news/news_detail.html"
    context_object_name = "news_item"

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)

        # self.object.views = F('views') + 1
        # self.object.save()
        # self.object.refresh_from_db()

        news_likes = get_object_or_404(News, id=self.kwargs['pk'])
        total_likes = news_likes.total_likes()
        context["total_likes"] = total_likes

        return context


def LikeView(request, pk):
    if request.user.is_authenticated:
        news = get_object_or_404(News, id=request.POST.get('news_id'))
        news.likes.add(request.user)
        # return HttpResponseRedirect(reverse('view_news', args=[str(pk)]))
        return redirect('detail_news', pk)
    else:
        return redirect('login')


def RemoveLikeView(request, pk):
    if request.user.is_authenticated:
        news = get_object_or_404(News, id=request.POST.get('news_id'))
        news.likes.remove(request.user)
        # return HttpResponseRedirect(reverse('view_news', args=[str(pk)]))
        return redirect('detail_news', pk)
    else:
        return redirect('login')


def CommentLikeView(request, pk):
    if request.user.is_authenticated:
        comment = get_object_or_404(Comment, id=request.POST.get('comment_id'))
        comment.likes.add(request.user)
        return redirect('detail_news', pk)
    else:
        return redirect('login')


def ReplyCommentLikeView(request, pk):
    if request.user.is_authenticated:
        comment = get_object_or_404(ReplyComment, id=request.POST.get('reply_comment.id'))
        comment.likes.add(request.user)
        return redirect('detail_news', pk)
    else:
        return redirect('login')


class CreateNews(LoginRequiredMixin, CreateView):
    form_class = NewsForm
    template_name = "news/add_news.html"
    success_url = reverse_lazy("home")


class CreateComment(CreateView):
    model = Comment
    form_class = CommentForm
    template_name = "news/add_comment.html"
    # fields = '__all__'
    success_url = reverse_lazy('home')

    def form_valid(self, form):
        form.instance.news_id = self.kwargs['pk']
        return super().form_valid(form)


class CreateReplyComment(CreateView):
    model = ReplyComment
    form_class = ReplyCommentForm
    template_name = "news/add_reply_comment.html"
    # fields = '__all__'
    success_url = reverse_lazy('home')

    def form_valid(self, form):
        form.instance.parent_comment_id = self.kwargs['pk']
        return super().form_valid(form)


class RegisterUser(MyMixin, CreateView):
    form_class = RegisterUserForm
    template_name = "news/register.html"
    success_url = reverse_lazy('login')

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        c_def = self.get_user_context(title="Регистрация")
        return dict(list(context.items()) + list(c_def.items()))

    def form_valid(self, form):
        user = form.save()
        login(self.request, user)
        return redirect('home')


class Login(LoginView):
    form_class = LoginUserForm
    template_name = "news/login.html"


class Logout(LogoutView):
    pass

# def index(request):
#     news = News.objects.all()
#     context = {
#         "news": news,
#         "title": "Список Новостей",
#     }
#     return render(request, template_name="news/index.html", context=context)


# def test(request):
#     if request.method == 'POST':
#         form = ContactForm(request.POST)
#         if form.is_valid():
#             mail = send_mail(form.cleaned_data['subject'], form.cleaned_data['content'], 'vladpryadko69@gmail.com',
#                              ['elka5776@gmail.com'], fail_silently=False)
#             if mail:
#                 messages.success(request, 'Письмо отправлено!')
#                 return redirect('test')
#             else:
#                 messages.error(request, 'Ошибка отправки')
#         else:
#             messages.error(request, 'Ошибка регистрации')
#     else:
#         form = ContactForm()
#     return render(request, 'news/test.html', {"form": form})

# def register(request):
#     if request.method == 'POST':
#         form = RegisterUserForm(request.POST)
#         if form.is_valid():
#             user = form.save()
#             login(request, user)
#             messages.success(request, "Успешная регистрация")
#             return redirect('home')
#         else:
#             messages.error(request, "Ошибка регестрации")
#     else:
#         form = UserRegisterForm()
#     return render(request, 'news/register.html', {"form": form})

# def user_login(request):
#     if request.method == 'POST':
#         form = UserLoginForm(data=request.POST)
#         if form.is_valid():
#             user = form.get_user()
#             login(request, user)
#             return redirect('home')
#     else:
#         form = UserLoginForm()
#     return render(request, 'news/login.html', {"form": form})

# def user_logout(request):
#     logout(request)
#     return redirect('home')


# def get_category(request, category_id):
#     news = News.objects.filter(category_id=category_id)
#     category = Category.objects.get(pk=category_id)
#     return render(request, "news/category.html", {"news": news, "category": category})


# def view_news(request, news_id):
#     # news_item = News.objects.get(pk=news_id)
#     news_item = get_object_or_404(News, pk=news_id)
#     return render(request, "news/view_news.html", {"news_item": news_item})


# def add_news(request):
#     if request.method == "POST":
#         form = NewsForm(request.POST)
#         if form.is_valid():
#             print(form.cleaned_data)
#             # news = News.objects.create(**form.cleaned_data)
#             news = form.save()
#             return redirect(news)
#     else:
#         form = NewsForm()
#     return render(request, "news/add_news.html", {"form": form})
