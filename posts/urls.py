from django.urls import path, re_path

from .views import (
    AllPostsView,
    PostView,
)

app_name = 'posts'
urlpatterns = [
    path(r'all/', AllPostsView.as_view(), name='all_posts'),
    re_path(r'^(?P<post_id>[0-9]+)/$', PostView.as_view(), name='post'),
]
