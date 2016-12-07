from django.core.management.base import BaseCommand, CommandError
from mords_api.models import Book


class Command(BaseCommand):
    help = 'crawl dictionary data from urban dictionary'

    def handle(self, *args, **options):
        book =

        # raise CommandError('Poll "%s" does not exist' % poll_id)



        self.stdout.write(self.style.SUCCESS('Successfully updated vocabulary book: urban_dic_new'))