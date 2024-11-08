from django.test import TestCase
from django.contrib.auth.models import User
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
