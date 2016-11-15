import datetime
from django.test import TestCase
from django.utils import timezone
from mords_api.models import Note


class NoteMethodTests(TestCase):
    def test_was_published_recently_with_future_note(self):
        """
        was_published_recently() should return False for notes whose
        pub_date is in the future.
        """
        time = timezone.now() + datetime.timedelta(days=30)
        future_note = Note(pub_date=time)
        self.assertIs(future_note.was_published_recently(), False)

    def test_was_published_recently_with_old_question(self):
        """
        was_published_recently() should return False for notes whose
        pub_date is older than 1 day.
        """
        time = timezone.now() - datetime.timedelta(days=30)
        old_note = Note(pub_date=time)
        self.assertIs(old_note.was_published_recently(), False)

    def test_was_published_recently_with_recent_question(self):
        """
        was_published_recently() should return True for notes whose
        pub_date is within the last day.
        """
        time = timezone.now() - datetime.timedelta(hours=1)
        recent_note = Note(pub_date=time)
        self.assertIs(recent_note.was_published_recently(), True)
