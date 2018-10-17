from django.urls import path
from . import views
from accounts import views as accounts_views
from django.contrib.auth import views as auth_views



app_name = 'boards'
urlpatterns = [
    path('', views.BoardListView.as_view(), name='home'),
    path('signup/', accounts_views.signup, name='signup'),
    path('login/', auth_views.LoginView.as_view(template_name='boards/login.html'), name='login'),
    path('reset/', auth_views.PasswordResetView.as_view(
        template_name='boards/password_reset.html',
        email_template_name='boards/password_reset_email.html',
        subject_template_name='boards/password_reset_subject.txt',

    ), name='password_reset'),
    path('reset/done/', auth_views.PasswordResetDoneView.as_view(
        template_name='boards/password_reset_done.html'

    ), name='password_reset_done'),
    path(r'^reset/(?P<uidb64>[0-9A-Za-z_\-]+)/(?P<token>[0-9A-Za-z]{1,13}-[0-9A-Za-z]{1,20})/$', auth_views.PasswordResetDoneView.as_view(
        template_name='boards/password_reset_confirm.html'

    ), name='password_reset_confirm'),
    path('reset/complete/', auth_views.PasswordResetCompleteView.as_view(
        template_name='boards/password_reset_complete.html'

    ), name='password_reset_complete'),
    path('setting/password/', auth_views.PasswordChangeView.as_view(
        template_name='boards/password_change.html'
    ),name='password_change'),
    path('setting/account/', views.UserUpdateView.as_view(),name='my_account'),
    path('setting/password/done/', auth_views.PasswordChangeDoneView.as_view(template_name='boards/password_change_done.html'), name='password_change_done'),
    path('logout/', auth_views.LogoutView.as_view(), name="logout"),
    path('<int:d>/', views.TopicListView.as_view(), name='topics'),
    path('<int:d>/topics/<int:topic_pk>/', views.PostListView.as_view(), name='topic_posts'),
    path('<int:id>/topics/<int:topic_pk>/post/<int:post_pk>/edit/', views.PostUpdateView.as_view() ,name='edit_post'),
    path('<int:d>/topics/<int:topic_pk>/reply/', views.post_reply, name='topic_posts_reply'),
    path('<int:id>/new/', views.new_topic, name='new_topic'),
]