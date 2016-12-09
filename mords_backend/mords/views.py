from datetime import timedelta
from django.db import IntegrityError
from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse, HttpResponseRedirect
from django.utils import timezone
from django.urls import reverse
from django.contrib.auth.decorators import login_required
from django.views import generic
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from mords_api.models import Note, Word, Learner, Entry
from forms import UserForm, LearnerForm, PasswordForm


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


class NewView(generic.ListView):
    template_name = 'mords/new.html'
    context_object_name = 'latest_entry_list'

    def get_queryset(self):
        return Entry.objects.filter(update_date__lte=timezone.now()+timedelta(days=1))


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
            if 'pic' in request.FILES:
                learner.pic = request.FILES['pic']
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


@login_required
def update_profile(request):
    if request.method == 'POST':
        learner_form = LearnerForm(data=request.POST)
        if learner_form.is_valid():
            learner = Learner.objects.get(user=request.user)
            learner.book = learner_form.cleaned_data['book']
            learner.words_perDay = learner_form.cleaned_data['words_perDay']
            if 'pic' in request.FILES:
                learner.pic = request.FILES['pic']
            learner.save()
        else:
            print(learner_form.errors)
    else:
        learner_form = LearnerForm()

    learner = Learner.objects.get(user=request.user)
    pass_form = PasswordForm()

    context = {
        'password_form': pass_form,
        'learner_form': learner_form,
        'learner': learner,
    }
    return render(request,
                  'mords/profile.html',
                  context
                  )


@login_required
def update_password(request):
    if request.method == 'POST':
        pass_form = PasswordForm(data=request.POST)
        if pass_form.is_valid():
            user = request.user
            user.set_password(pass_form.cleaned_data['password'])
            user.save()
            info = 'Password Updated'
        else:
            print(pass_form.errors)
            info = pass_form.errors
    else:
        info = ''
        pass_form = PasswordForm()

    learner = Learner.objects.get(user=request.user)
    learner_form = LearnerForm()

    context = {
        'password_form': pass_form,
        'learner_form': learner_form,
        'learner': learner,
        'info': info
    }
    return render(request,
                  'mords/profile.html',
                  context
                  )


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
