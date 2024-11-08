from django.test import TestCase
from django.contrib.auth.models import User
from rest_framework.test import APITestCase, APIClient
from rest_framework import status
from .models import Book, Bookmark, Comment
from django.db.utils import IntegrityError

class BookModelTest(TestCase):
    def setUp(self):
        self.book = Book.objects.create(
            title="Test Book",
            author="Author Name",
            description="A test book description.",
            published_date="2023-01-01",
        )

    def test_create_book(self):
        """Test creating a new Book instance."""
        book = Book.objects.create(
            title="Another Book",
            author="Another Author",
            description="Another description.",
            published_date="2023-02-01",
        )
        self.assertEqual(Book.objects.count(), 2)

    def test_read_book(self):
        """Test reading an existing Book instance."""
        book = Book.objects.get(id=self.book.id)
        self.assertEqual(book.title, "Test Book")

    def test_update_book(self):
        """Test updating an existing Book instance."""
        self.book.title = "Updated Test Book"
        self.book.save()
        updated_book = Book.objects.get(id=self.book.id)
        self.assertEqual(updated_book.title, "Updated Test Book")

    def test_delete_book(self):
        """Test deleting a Book instance."""
        book_id = self.book.id
        self.book.delete()
        with self.assertRaises(Book.DoesNotExist):
            Book.objects.get(id=book_id)


class BookmarkModelTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username="user1", password="password123")
        self.book = Book.objects.create(
            title="Bookmark Test Book",
            author="Author Name",
            published_date="2023-01-01",
        )

    def test_create_bookmark(self):
        """Test creating a Bookmark instance."""
        bookmark = Bookmark.objects.create(user=self.user, book=self.book)
        self.assertEqual(Bookmark.objects.count(), 1)
        self.assertEqual(bookmark.user, self.user)

    def test_read_bookmark(self):
        """Test reading a Bookmark instance."""
        bookmark = Bookmark.objects.create(user=self.user, book=self.book)
        fetched_bookmark = Bookmark.objects.get(id=bookmark.id)
        self.assertEqual(fetched_bookmark.book, self.book)

    def test_update_bookmark(self):
        """Test updating a Bookmark instance."""
        bookmark = Bookmark.objects.create(user=self.user, book=self.book)
        new_book = Book.objects.create(
            title="Another Book",
            author="Another Author",
            published_date="2023-02-01",
        )
        bookmark.book = new_book
        bookmark.save()
        updated_bookmark = Bookmark.objects.get(id=bookmark.id)
        self.assertEqual(updated_bookmark.book, new_book)

    def test_delete_bookmark(self):
        """Test deleting a Bookmark instance."""
        bookmark = Bookmark.objects.create(user=self.user, book=self.book)
        bookmark_id = bookmark.id
        bookmark.delete()
        with self.assertRaises(Bookmark.DoesNotExist):
            Bookmark.objects.get(id=bookmark_id)

    def test_unique_constraint(self):
        """Test that a user cannot bookmark the same book twice."""
        Bookmark.objects.create(user=self.user, book=self.book)
        with self.assertRaises(IntegrityError):
            # Attempting to create a duplicate bookmark for the same user and book
            Bookmark.objects.create(user=self.user, book=self.book)


class CommentModelTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username="user2", password="password123")
        self.book = Book.objects.create(
            title="Comment Test Book",
            author="Author Name",
            published_date="2023-01-01",
        )

    def test_create_comment(self):
        """Test creating a Comment instance."""
        comment = Comment.objects.create(
            user=self.user,
            book=self.book,
            text="Great book!",
            rating=5
        )
        self.assertEqual(Comment.objects.count(), 1)
        self.assertEqual(comment.text, "Great book!")

    def test_read_comment(self):
        """Test reading a Comment instance."""
        comment = Comment.objects.create(user=self.user, book=self.book, text="Interesting!", rating=4)
        fetched_comment = Comment.objects.get(id=comment.id)
        self.assertEqual(fetched_comment.text, "Interesting!")

    def test_update_comment(self):
        """Test updating a Comment instance."""
        comment = Comment.objects.create(user=self.user, book=self.book, text="Good read.", rating=3)
        comment.text = "Amazing read!"
        comment.rating = 5
        comment.save()
        updated_comment = Comment.objects.get(id=comment.id)
        self.assertEqual(updated_comment.text, "Amazing read!")
        self.assertEqual(updated_comment.rating, 5)

    def test_delete_comment(self):
        """Test deleting a Comment instance."""
        comment = Comment.objects.create(user=self.user, book=self.book, text="Not bad", rating=3)
        comment_id = comment.id
        comment.delete()
        with self.assertRaises(Comment.DoesNotExist):
            Comment.objects.get(id=comment_id)


class BookAPITestCase(APITestCase):
    def setUp(self):
        
        self.user = User.objects.create_user(username='testuser', password='testpass')
        self.client = APIClient()
        response = self.client.post('/auth/token/', {'username': 'testuser', 'password': 'testpass'})
        self.token = response.data['access']
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {self.token}')
        
        self.book = Book.objects.create(
            title="Test Book",
            author="Author Name",
            description="Test description",
            published_date="2024-01-01"
        )

    def test_get_list_book(self):
        """Test retrieving a list of book"""
        self.test_bookmark_book()

        url = f'/books/list/'
        response = self.client.get(url)
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data[0]['author'], self.book.author)
        self.assertEqual(response.data[0]['is_bookmarked'], True)

    def test_get_single_book(self):
        """Test retrieving a single book by its ID"""
        url = f'/books/{self.book.id}/'
        response = self.client.get(url)
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        
        self.assertEqual(response.data['title'], self.book.title)
        self.assertEqual(response.data['author'], self.book.author)

    def test_bookmark_book(self):
        """Test bookmarking a book"""
        url = f'/books/bookmark/{self.book.id}/'
        response = self.client.post(url)
        
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        
        bookmark_exists = Bookmark.objects.filter(user=self.user, book=self.book).exists()
        self.assertTrue(bookmark_exists)

    def test_remove_bookmark(self):
        """Test removing a bookmark from a book"""
        Bookmark.objects.create(user=self.user, book=self.book)
        
        url = f'/books/bookmark/{self.book.id}/'
        response = self.client.delete(url)
        
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        
        bookmark_exists = Bookmark.objects.filter(user=self.user, book=self.book).exists()
        self.assertFalse(bookmark_exists)

    def add_comment(self, comment_data, status_code=status.HTTP_201_CREATED):
        url = f'/books/comment/{self.book.id}/'
        response = self.client.post(url, data=comment_data)
        
        rating = response.data['rating'] if response.data['rating'] else ''
        text = response.data['text'] if response.data['text'] else ''

        self.assertEqual(response.status_code, status_code)        
        self.assertEqual(text, comment_data['text'])
        self.assertEqual(rating, comment_data['rating'])

        if status_code == status.HTTP_201_CREATED or status_code == status.HTTP_200_OK:
            bookmark_exists = Comment.objects.filter(user=self.user, book=self.book).exists()
            self.assertTrue(bookmark_exists)

    def test_add_comment(self):
        """Test adding a comment to a book"""
        self.add_comment({"text": "Great book!", "rating": 4})

    def test_modify_comment(self):
        """Ensure a user submit more than one comment just create at first time and after that just modify"""
        self.add_comment({"text": "My first comment", "rating": 5}, status.HTTP_201_CREATED)
        self.add_comment({"text": "Trying another comment", "rating": 3}, status.HTTP_200_OK)

    def test_add_just_rate(self):
        """Test adding a rate without text to a book"""
        self.add_comment({"text": '', "rating": 2})

    def test_add_just_text_comment(self):
        """Test adding a text without rate to a book"""
        self.add_comment({"text": 'Great book!', "rating": ''})

    def test_remove_bookmark_if_submit_comment(self):
        """add bookmark then submit comment for remove bookmark"""
        self.test_bookmark_book()
        self.test_add_comment()
        url = f'/books/list/'
        response = self.client.get(url)
        self.assertEqual(response.data[0]['is_bookmarked'], False)

    def test_cant_bookmark_when_have_comment(self):
        """users cant bookmark when have comment on the book"""
        self.test_add_comment()
        url = f'/books/bookmark/{self.book.id}/'
        response = self.client.post(url)
        
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data['message'], 'You have Comment on this book')
        