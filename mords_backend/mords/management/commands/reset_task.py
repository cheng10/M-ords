from django.core.management.base import BaseCommand, CommandError
from mords_api.models import Learner


class Command(BaseCommand):
    help = 'reset learner learning status everyday'

    def handle(self, *args, **options):
        learners = Learner.objects.all()
        self.stdout.write(str(len(learners))+' learners to process.')
        for learner in learners:
            learner.words_finished = 0
            learner.save()

        self.stdout.write(self.style.SUCCESS('Successfully reset learners task.'))
