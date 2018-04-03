from django.urls import path, re_path

from .api_views import (
    AllPostsAPI,
    PostAPI,
)

app_name = 'posts_api'
urlpatterns = [
    path(r'all/', AllPostsAPI.as_view(), name='all_posts'),
    re_path(r'^(?P<post_id>[0-9]+)/$', PostAPI.as_view(), name='post'),
]
