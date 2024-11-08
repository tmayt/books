from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi
from django.shortcuts import get_object_or_404
from django.db import IntegrityError
from .serializers import BookSerializer, CommentSerializer
from .models import Book, Bookmark, Comment

class BookListView(APIView):
    @swagger_auto_schema(
        operation_description="Get a list of all books in the system.",
        responses={
            200: openapi.Response(
                description="A list of books",
                schema=BookSerializer(many=True)
            ),
            400: openapi.Response(
                description="Bad request"
            ),
        },
    )
    def get(self, request):
        books = Book.objects.all()
        context = {'request': request}
        serializer = BookSerializer(books, many=True, context=context)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
class BookDetailView(APIView):
    @swagger_auto_schema(
        operation_description="Retrieve a book by its ID",
        responses={
            200: BookSerializer,
            404: openapi.Response(description="Book not found")
        },
    )
    def get(self, request, pk, *args, **kwargs):
        try:
            book = Book.objects.get(pk=pk)
            context = {'request': request, 'detailed': True}
            serializer = BookSerializer(book, context=context)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except Book.DoesNotExist:
            return Response({"error": "Book not found"}, status=status.HTTP_404_NOT_FOUND)
        

class BookmarkToggleView(APIView):
    @swagger_auto_schema(
        operation_description="Toggle bookmark on a book by ID. Use POST to add and DELETE to remove.",
        responses={
            201: openapi.Response(description="Book bookmarked successfully"),
            204: openapi.Response(description="Bookmark removed successfully"),
            400: openapi.Response(description="Bookmark already exists"),
            404: openapi.Response(description="Book not found"),
        }
    )
    def post(self, request, pk):
        if not Comment.objects.filter(user=request.user, book=book).exists():
            book = get_object_or_404(Book, id=pk)
            bookmark, created = Bookmark.objects.get_or_create(user=request.user, book=book)
            if created:
                return Response({"message": "Book bookmarked successfully"}, status=status.HTTP_201_CREATED)
            return Response({"message": "Bookmark already exists"}, status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response({"message": "You have Comment on this book"}, status=status.HTTP_400_BAD_REQUEST)

    @swagger_auto_schema(
        operation_description="Remove a bookmark from a book by ID.",
    )
    def delete(self, request, pk):
        bookmark = Bookmark.objects.filter(user=request.user, book__id=pk).first()
        if bookmark:
            bookmark.delete()
            return Response({"message": "Bookmark removed successfully"}, status=status.HTTP_204_NO_CONTENT)
        return Response({"message": "Bookmark not found"}, status=status.HTTP_404_NOT_FOUND)
    
class SubmitCommentView(APIView):
    @swagger_auto_schema(
        operation_description="Submit a comment with optional rating and/or text. Both cannot be empty. Each user can comment only once per book.",
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            properties={
                'text': openapi.Schema(type=openapi.TYPE_STRING, description='Comment text', nullable=True),
                'rating': openapi.Schema(type=openapi.TYPE_INTEGER, description='Rating (1-5)', nullable=True),
            },
            required=['pk'],
            example={"text": "Great book!", "rating": 5}
        ),
        responses={
            201: openapi.Response(description="Comment submitted successfully"),
            200: openapi.Response(description="Comment modified successfully"),
            400: openapi.Response(description="Either text or rating must be provided, and each user can comment on a book only once. Rating must be a number between 1 and 5, or left blank"),
            404: openapi.Response(description="Book not found"),
        }
    )
    def post(self, request, pk):
        book = get_object_or_404(Book, id=pk)

        text = request.data.get('text')
        rating = request.data.get('rating')

        if (text is None and rating is None):
            return Response(
                {"error": "Either text or rating must be provided"},
                status=status.HTTP_400_BAD_REQUEST
            )
        if (int(rating) in range(1, 6)):
            return Response(
                {"error": "Rating must be a number between 1 and 5, or left blank"},
                status=status.HTTP_400_BAD_REQUEST
            )

        try:
            bookmark = Bookmark.objects.filter(user=request.user, book=book).first()
            if bookmark:
                bookmark.delete()                
            # Attempt to create the comment
            comment = Comment.objects.create(
                user=request.user,
                book=book,
                text=text if text else None,
                rating=rating if rating is not None else 0
            )
            created = True
        except IntegrityError:
            comment = Comment.objects.get(user=request.user, book=book)
            comment.text = text if text else None
            comment.rating = rating if rating is not None else 0
            comment.save()
            created = False
        
        serializer = CommentSerializer(comment)
        return Response(serializer.data, status=status.HTTP_201_CREATED if created else status.HTTP_200_OK)
    
