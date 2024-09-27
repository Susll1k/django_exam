from django.forms import BaseModelForm
from django.shortcuts import render, redirect   
from django.contrib.auth.models import User
from django.contrib.auth.views import LoginView, LogoutView
from django.urls import reverse_lazy
from django.views.generic import CreateView, ListView, DetailView, UpdateView
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from django.contrib.auth.mixins import UserPassesTestMixin, LoginRequiredMixin
from django.contrib.auth.decorators import login_required
from .forms import SignUpForm, LoginForm, CreatePostForm,PhotoForm
from django.core.mail import send_mail
from django.conf import settings
from .models import CustomUser, Post, Review,Like
from django.views.generic.edit import CreateView, DeleteView
from django.contrib.contenttypes.models import ContentType
from django.http import HttpRequest, HttpResponse, JsonResponse
from django.shortcuts import get_object_or_404
from django.contrib.contenttypes.models import ContentType

from rest_framework import status
from rest_framework.response import Response
from rest_framework.decorators import api_view
from .serializers import LikeSerializer


def post_like(request, pk):
    post = get_object_or_404(Post, pk=pk)
    content_type = ContentType.objects.get_for_model(Post)
    
    like = Like.objects.get_or_create(
        content_type=content_type,
        object_id=post.id,
    )
    
    if request.method == 'POST':
        if like[0].like:
            like[0].delete()
        else:
            like[0].like=True
            like[0].save()
    
    return redirect('home')


class SignUp(CreateView):
    model = CustomUser
    form_class = SignUpForm
    success_url = reverse_lazy('login')
    template_name = 'registration/signup.html'
    def form_valid(self, form):
        user = form.save()
        
        send_mail(
            "Добро пожаловать в Olau! Ваш аккаунт успешно создан",
            f"""Здравствуйте, {user.username}!

Добро пожаловать в Olau! Мы рады сообщить, что ваш аккаунт был успешно создан. Теперь вы можете начать пользоваться всеми возможностями нашего сервиса.

Если у вас возникнут вопросы или понадобится помощь, наша команда всегда готова помочь.

Спасибо, что выбрали Olau!

С уважением,
Команда Olau""",
            settings.EMAIL_HOST_USER,
            [user.email],
            fail_silently=False
        )
        return super().form_valid(form)


class Login(LoginView):
    template_name = 'registration/login.html'
    form_class=LoginForm
    next_page = reverse_lazy('home')
    


class Logout(LogoutView):
    next_page = reverse_lazy('login')

class ChoosePhoto(UpdateView):
    model=CustomUser
    template_name = 'avatar.html'
    success_url = reverse_lazy('profile')
    form_class = PhotoForm


    def form_valid(self, form: BaseModelForm) -> HttpResponse:
        user=self.request.user.username
        posts=Post.objects.filter(author=user)
        for post in posts:
            post.picture=str(self.request.user.picture)
            post.save()
        return super().form_valid(form)


@login_required(login_url="login")
def comment(request, id):
    post=Post.objects.get(id=id)
    if request.method == 'POST':
        text = request.POST.get('text', None)
        post_id = post.id
        user_id= request.user
        Review.objects.create(text=text, author=user_id, post = post)
        return render(request, 'comment.html', {'post': post})

    return render(request, 'comment.html', {'post': post})

def notification(request):
    username=request.user.username
    user=CustomUser.objects.get(username=username)

    notification = list(user.likes_author.all()) + list(user.reviews_author.all())
    
    # Сортируем уведомления по полю 'created_at'
    notification = sorted(notification, key=lambda x: x.created_at, reverse=True)

    return render(request, 'notification.html', {'notification': notification})

@login_required(login_url="login")
def home(request):
    posts=Post.objects.all()
    user=request.user
    liked_posts = Like.objects.filter(author=user).values_list('post_id', flat=True)

    return render(request, 'index.html', {'posts': posts, 'liked_posts': liked_posts})

@login_required(login_url="login")
def profile(request):
    user=request.user
    posts=Post.objects.filter(author=user)
    content_type = ContentType.objects.get_for_model(Post)
    liked_posts = Like.objects.filter(author=user).values_list('post_id', flat=True)
    
    if request.method == 'POST':
        user = CustomUser.objects.get(id=request.user.id)
        if request.FILES.get('picture'):
            user.picture = 'profile_pics/'+str(request.FILES.get('picture'))
        if request.POST.get('username_input'):
            user.username = request.POST.get('username_input')
        user.save()
        form = PhotoForm(request.POST, request.FILES,instance=user)
        if form.is_valid():
            form.save()
    else:
        form = PhotoForm()


    return render(request, 'profile.html',{'posts':posts, 'user':user,'form':form, 'liked_posts': liked_posts})


class CreatePost(CreateView):
    model = Post
    success_url = reverse_lazy('home')
    template_name = 'create.html'
    form_class = CreatePostForm
    def form_valid(self, form: BaseModelForm) -> HttpResponse:
        form.instance.author=self.request.user
        return super().form_valid(form)


class DeletePost(DeleteView):
    model = Post
    success_url = reverse_lazy('home')
    template_name = 'delete.html'


def create_review(request):
    reviews=Review.objects.all()

    if request.method == 'POST':
        text = request.POST.get('text', None)
        post_id = request.POST.get('post_id', None)
        Review.objects.create(text=text, content_type=ContentType.objects.get_for_model(Post),
                              object_id = int(post_id))
        return render(request, 'coment.html', {'reviews': reviews})

    return render(request, 'coment.html', context= {'reviews':reviews})

@api_view(['POST'])
def add_item(request):
    serializer = LikeSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['DELETE'])
def delete_item(request, context):
    ncontext=context.split(",")
    try:
        item = Like.objects.filter(author_id=int(ncontext[1]),post_id=int(ncontext[0]))
    except Like.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)
    
    item.delete()
    return Response(status=status.HTTP_204_NO_CONTENT)