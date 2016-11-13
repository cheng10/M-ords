from django.shortcuts import render
from django.http import HttpResponse
from mords_api.models import Note


def index(request):
    return HttpResponse("Hello, world. Welcome to Mords!")


def detail(request, word_text):
    return HttpResponse("You're looking at word %s." % word_text)


def note(request, word_text):
    response = "You're looking at the note of word %s."
    return HttpResponse(response % word_text)


def know(request, word_text):
    return HttpResponse("You're saying you know word %s." % word_text)


def latest_notes(request):
    latest_note_list = Note.objects.order_by('-pub_date')[:5]
    output = ', '.join([n.text for n in latest_note_list])
    return HttpResponse(output)
