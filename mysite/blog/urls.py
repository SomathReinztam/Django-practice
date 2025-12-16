from django.urls import path
from .views import (
    AddPostView,
    AllPostAuthorsView,
    AuthorPostsView
)

urlpatterns = [
    path("posts/add/", AddPostView.as_view(), name="add-post"),
    path("posts/authors/", AllPostAuthorsView.as_view(), name="post-authors"),
    path("posts/by-author/", AuthorPostsView.as_view(), name="posts-by-author"),
]
