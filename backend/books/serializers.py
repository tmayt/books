from rest_framework import serializers
from django.db.models import Avg, Count
from .models import Book, Comment, Bookmark

class CommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = ['id', 'user', 'book', 'text', 'rating', 'submitted_on']
        read_only_fields = ['id', 'user', 'book', 'submitted_on']

class CommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = ['user', 'text', 'rating', 'submitted_on']

class BookmarkSerializer(serializers.ModelSerializer):
    class Meta:
        model = Bookmark
        fields = ['user', 'added_on']

class BookSerializer(serializers.ModelSerializer):
    class Meta:
        model = Book
        fields = ['id', 'title', 'author', 'description', 'published_date', 'cover_image']

    def to_representation(self, instance):
        data = super().to_representation(instance)
    
        data['is_bookmarked'] = Bookmark.objects.filter(book=instance, user=self.context.get('request').user).exists()
        data['total_bookmarks'] = instance.bookmarked_by.count()

        # Check if the 'detailed' context flag is set to True
        if self.context.get('detailed', False):
            # Add additional fields for detailed view
            comments = instance.comments
            data['total_comments'] = comments.exclude(text=None).count()
            data['total_rating'] = comments.exclude(rating=0).count()
            data['rating_avg'] = comments.exclude(rating=0).aggregate(average_rating=Avg('rating'))['average_rating']
            rating_counts = comments.exclude(rating=0).values('rating').annotate(count=Count('rating')).order_by('rating')
            rating_dict = {str(i): 0 for i in range(1, 6)}
            for rating in rating_counts:
                rating_dict[str(rating['rating'])] = rating['count']
            data['rating_dict'] = rating_dict
            data['users_actions'] = comments.values('user__username', 'text', 'rating', 'submitted_on')
        return data
