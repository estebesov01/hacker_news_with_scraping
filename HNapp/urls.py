from django.contrib import admin
from django.urls import path, include
from .views import *

app_name = 'HNapp'

urlpatterns = [
    path('', post_list_view, name='home'),
    path('new', new_post_list_view, name='new_home'),
    path('user/<username>', user_info_view, name='user_info'),
    path('posts/<username>', user_submissions, name='user_posts'),
    path('submit', submit_post_view, name='submit'),
    path('edit/<int:id>', edit_post_view, name='edit'),
    path('signin', sign_in, name='signin'),
    path('signup', sign_up, name='signup'),
    path('signout', sign_out, name='signout'),
    path('vote/<int:post_id>', up_vote_view, name='vote'),
    path('downvote/<int:post_id>', down_vote_view, name='dvote'),
    path('post/<int:id>', comment_list_view, name='post'),
    path('post/<int:id1>/comment/<int:id2>', comment_reply_view, name='reply'),
    path('parse', parse_site, name='parse_site'),
    path('delete/<int:id>/', post_delete_view, name='post_delete'),

]
