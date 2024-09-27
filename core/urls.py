from django.contrib import admin
from django.conf.urls.static import static
from django.conf import settings
from django.urls import path, include
from app.views import Login, SignUp, Logout, home, DeletePost, CreatePost, create_review,post_like,profile, ChoosePhoto, add_item, delete_item,comment,notification
from django.contrib.auth.views import PasswordChangeView, PasswordChangeDoneView


urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('social_django.urls', namespace='social')),
    path('', home, name='home'),
    path('login/', Login.as_view(), name='login'),
    path('singup/', SignUp.as_view(), name='signup'),
    path('logout/', Logout.as_view(), name='logout'),
    path('choose_photo/<int:pk>', ChoosePhoto.as_view(), name='choose_photo'),
    path('accounts/password_change/', PasswordChangeView.as_view(template_name='registration/change_password.html'), name='password_change'),
    path('accounts/password_change/done/', PasswordChangeDoneView.as_view(template_name='registration/change_password_done.html'), name='password_change_done'),
    path('create/', CreatePost.as_view(), name='create'),
    path('delete/<int:id>', DeletePost.as_view(), name='delete'),
    path('create_review/', create_review, name='create_review'),
    path('like/<int:pk>/', post_like, name='post_like'),
    path('profile/', profile, name='profile'),
    path('add-item/', add_item, name='add-item'),
    path('delete-item/<str:context>/', delete_item, name='delete-item'),
    path('review/<int:id>/', comment, name='review'),
    path('notification', notification, name='notification'),

    
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
