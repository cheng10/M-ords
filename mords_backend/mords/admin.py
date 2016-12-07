from django.contrib import admin

from mords_api.models import Word, Book, Learner, Note, Entry

admin.site.register(Word)
admin.site.register(Book)
admin.site.register(Learner)
admin.site.register(Note)
admin.site.register(Entry)
