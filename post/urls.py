from django.urls import path
from post.views import(
    create_post_view,
    edit_post_view,
    delPost,
)

app_name = 'post'

urlpatterns = [
    path('create', create_post_view, name='create'),
    path('<pk>/edit', edit_post_view, name='edit'),
    path('<pk>/delete', delPost, name='delete'),
]
