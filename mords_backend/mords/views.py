from django.db import IntegrityError
from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse, HttpResponseRedirect
from django.utils import timezone
from django.urls import reverse
from django.contrib.auth.decorators import login_required
from django.views import generic
from django.contrib.auth.models import User
from mords_api.models import Note, Word, Learner


class IndexView(generic.ListView):
    template_name = 'mords/index.html'
    context_object_name = 'latest_note_list'

    def get_queryset(self):
        """
        Return the last five published notes (not including those set to be
        published in the future).

        """
        # return Note.objects.order_by('-pub_date')[:5]
        return Note.objects.filter(pub_date__lte=timezone.now()).order_by('-pub_date')[:5]


# def index(request):
#     latest_note_list = Note.objects.order_by('-pub_date')[:5]
#     # tempalte = loader.get_template('mords/index.html')
#     context = {
#         'latest_note_list': latest_note_list,
#     }
#     # return HttpResponse(tempalte.render(context, request))
#     return render(request, 'mords/index.html', context)


def signup(request):
    try:
        username = request.POST['username']
        pwd = request.POST['password']
    except KeyError:
        error_message = 'You did not enter username or password.'
        return HttpResponseRedirect(reverse('mords:signup', args=(error_message,)))

    else:
        try:
            user = User.objects.create(
                username=username,
                password=pwd
            )
        except IntegrityError:
            error_message = 'User already exist.'
            return HttpResponseRedirect(reverse('mords:signup', args=(error_message,)))

        return HttpResponseRedirect(reverse('mords:login',))


def detail(request, word_text):
    """
    Excludes any notes that aren't published yet.
    :param request:
    :param word_text:
    :return:
    """
    word = get_object_or_404(Word, text=word_text)
    notes = word.note_set.all().filter(pub_date__lte=timezone.now())
    context = {
        'word': word,
        'notes': notes
    }
    return render(request, 'mords/detail.html', context)


@login_required
def comment(request, word_text):
    word = get_object_or_404(Word, text=word_text)

    try:
        text = request.POST['note']
    # except request.POST['note'] is None:
    except KeyError:
        return render(request, 'mords/detail.html',
                      {
                          'word': word,
                          'error_message': 'You did not enter a note.',
                      })
    else:
        try:
            author = Learner.objects.get(user=request.user)
        except Learner.DoesNotExist:
            return render(request, 'mords/detail.html',
                      {
                          'word': word,
                          'error_message': 'Learner does not exist.',
                      })
        pub_date = timezone.now()
        Note.objects.create(
            word=word,
            pub_date=pub_date,
            author=author,
            text=text
        )
        return HttpResponseRedirect(reverse('mords:results', args=(word.text,)))


def results(request, word_text):
    word = get_object_or_404(Word, text=word_text)
    return render(request, 'mords/results.html', {'word': word})


def note(request, word_text):
    response = "You're looking at the note of word %s."
    return HttpResponse(response % word_text)


def know(request, word_text):
    return HttpResponse("You're saying you know word %s." % word_text)


def latest_notes(request):
    latest_note_list = Note.objects.order_by('-pub_date')[:5]
    output = ', '.join([n.text for n in latest_note_list])
    return HttpResponse(output)
