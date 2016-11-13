from django.contrib import admin

from mords_api.models import Word, Book, Learner, Note

admin.site.register(Word)
admin.site.register(Book)
admin.site.register(Learner)
admin.site.register(Note)
