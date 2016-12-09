from django.db import IntegrityError
from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse, HttpResponseRedirect
from django.utils import timezone
from django.urls import reverse
from django.contrib.auth.decorators import login_required
from django.views import generic
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from mords_api.models import Note, Word, Learner
from forms import UserForm, LearnerForm


class IndexView(generic.ListView):
    template_name = 'mords/index.html'
    context_object_name = 'latest_note_list'

    def get_queryset(self):
        """
        Return the last five published notes (not including those set to be
        published in the future).

        """
        return Note.objects.order_by('-pub_date')
        # return Note.objects.order_by('-pub_date')[:5]
        # return Note.objects.filter(pub_date__lte=timezone.now()).order_by('-pub_date')[:5]


def signup(request):
    registered = False
    if request.method == 'POST':
        user_form = UserForm(data=request.POST)
        learner_form = LearnerForm(data=request.POST)
        if user_form.is_valid() and learner_form.is_valid():
            user = user_form.save()
            user.set_password(user.password)
            user.save()
            learner = learner_form.save(commit=False)
            learner.user = user
            if 'picture' in request.FILES:
                learner.picture = request.FILES['picture']
            learner.save()
            registered = True
        else:
            print(user_form.errors, learner_form.errors)
    else:
        user_form = UserForm()
        learner_form = LearnerForm()

    context = {
        'user_form': user_form,
        'learner_form': learner_form,
        'registered': registered
    }
    return render(request,
                  'mords/signup.html',
                  context
                  )


def user_login(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(username=username, password=password)
        if user:
            if user.is_active:
                login(request, user)
                return HttpResponseRedirect(reverse('mords:index'))
            else:
                return HttpResponse("Your account is disabled.")
        else:
            print("Invalid login details: {0}, {1}".format(username, password))
            return HttpResponse("Invalid login details supplied.")

    else:
        return render(request, 'mords/login.html', {})


@login_required
def user_logout(request):
    logout(request)
    return HttpResponseRedirect(reverse('mords:index'))


def detail(request, word_text):
    """
    Excludes any notes that aren't published yet.
    :param request:
    :param word_text:
    :return:
    """
    word = get_object_or_404(Word, text=word_text)
    notes = word.note_set.all()
    # notes = word.note_set.all().filter(pub_date__lte=timezone.now())
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
