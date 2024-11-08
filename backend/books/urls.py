from django.urls import path
from .views import BookListView, BookDetailView, BookmarkToggleView, SubmitCommentView

urlpatterns = [
    path('list/', BookListView.as_view(), name='book-list'),
    path('<int:pk>/', BookDetailView.as_view(), name='book-detail'),
    path('bookmark/<int:pk>/', BookmarkToggleView.as_view(), name='bookmark-toggle'),
    path('comment/<int:pk>/', SubmitCommentView.as_view(), name='submit-comment'),
]