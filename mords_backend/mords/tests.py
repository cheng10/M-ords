import datetime
from django.test import TestCase
from django.utils import timezone
from mords_api.models import Note, Word, Learner, Book
from django.urls import reverse
from django.contrib.auth.models import User


def create_user(username, pwd):
    """
    Creates a user with the given 'username' and 'pwd'.
    :param username:
    :param pwd:
    :return: new user instance
    """
    return User.objects.create_user(
        username=username,
        password=pwd
    )


def create_word(word_text):
    """
    Creates a note with the given `word_text`.
    :param word_text:
    :return: new word instance
    """
    return Word.objects.create(text=word_text)


def create_book(book_name, word_list):
    """
    Create a vocabulary book with given 'book_name'
    and 'word_list'.
    :param book_name:
    :param word_list:
    :return: new book instance
    """
    book = Book.objects.create(name=book_name)
    book.save()
    book.words = word_list
    return book


def create_learner(user, book, words_per_day=0):
    """
    Creates a learner with the given 'user', 'book'
    and 'words_perDay'.
    :param user:
    :param book:
    :param words_per_day:
    :return: new learner instance
    """
    return Learner.objects.create(
        user=user,
        book=book,
        words_perDay=words_per_day
    )


def create_note(word, author, note_text, days):
    """
    Creates a note with the given `note_text` and published the
    given number of `days` offset to now (negative for notes published
    in the past, positive for notes that have yet to be published).
    :param word:
    :param author
    :param note_text:
    :param days:
    :return: new note instance
    """
    time = timezone.now() + datetime.timedelta(days=days)
    return Note.objects.create(
        text=note_text,
        pub_date=time,
        word=word,
        author=author
    )


class NoteIndexDetailTests(TestCase):
    def setUp(self):
        user = create_user("testUser", "testPass")
        word1 = create_word("apple")
        word2 = create_word("banana")
        test_book = create_book("testBook", [word1, word2])
        self.test_word = word1
        self.test_learner = create_learner(user, test_book, 3)

    def test_detail_view_with_a_future_question(self):
        """
        The detail view of a word should not display future notes.
        :return:
        """
        future_note = create_note(
            word=self.test_word,
            author=self.test_learner,
            note_text='Future note.',
            days=5
        )
        url = reverse('mords:detail', args=(self.test_word.id,))
        response = self.client.get(url)
        self.assertNotContains(response, future_note.text)


class NoteMethodTests(TestCase):
    def test_was_published_recently_with_future_note(self):
        """
        was_published_recently() should return False for notes whose
        pub_date is in the future.
        """
        time = timezone.now() + datetime.timedelta(days=30)
        future_note = Note(pub_date=time)
        self.assertIs(future_note.was_published_recently(), False)

    def test_was_published_recently_with_old_note(self):
        """
        was_published_recently() should return False for notes whose
        pub_date is older than 1 day.
        """
        time = timezone.now() - datetime.timedelta(days=30)
        old_note = Note(pub_date=time)
        self.assertIs(old_note.was_published_recently(), False)

    def test_was_published_recently_with_recent_note(self):
        """
        was_published_recently() should return True for notes whose
        pub_date is within the last day.
        """
        time = timezone.now() - datetime.timedelta(hours=1)
        recent_note = Note(pub_date=time)
        self.assertIs(recent_note.was_published_recently(), True)
