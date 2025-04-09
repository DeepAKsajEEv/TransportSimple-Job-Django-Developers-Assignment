from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login, logout, authenticate
from django.http import JsonResponse ,HttpResponseForbidden
from django.core.paginator import Paginator
from .models import Question, Answer
from .forms import QuestionForm, AnswerForm, SignupForm

def home(request):
    questions = Question.objects.all().order_by('-created_at')
    paginator = Paginator(questions, 5)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    answered_questions = []
    if request.user.is_authenticated:
        answered_questions = Answer.objects.filter(author=request.user).values_list('question_id', flat=True)
    return render(request, 'core/home.html', {
        'questions': page_obj,
        'answered_questions': answered_questions
    })

@login_required
def question_detail(request, question_id):
    question = get_object_or_404(Question, id=question_id)
    answers = question.answers.all().order_by('-created_at')
    paginator = Paginator(answers, 3)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    if request.method == 'POST':
        form = AnswerForm(request.POST)
        if form.is_valid():
            answer = form.save(commit=False)
            answer.author = request.user
            answer.question = question
            answer.save()
            return redirect('question_detail', question_id=question.id)
    else:
        form = AnswerForm()
    return render(request, 'core/question_detail.html', {'question': question, 'form': form, 'answers': page_obj})

@login_required
def like_answer(request, answer_id):
    if request.method == 'POST':
        answer = get_object_or_404(Answer, id=answer_id)
        liked = False
        if request.user in answer.likes.all():
            answer.likes.remove(request.user)
        else:
            answer.likes.add(request.user)
            liked = True
        return JsonResponse({'likes_count': answer.likes.count(), 'liked': liked})
    return JsonResponse({'error': 'Invalid request'}, status=400)

def signup_view(request):
    if request.method == 'POST':
        form = SignupForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('home')
    else:
        form = SignupForm()
    return render(request, 'core/signup.html', {'form': form})

def login_view(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user:
            login(request, user)
            return redirect('home')
    return render(request, 'core/login.html')

def logout_view(request):
    logout(request)
    return redirect('login')

@login_required
def post_question(request):
    if request.method == 'POST':
        form = QuestionForm(request.POST)
        if form.is_valid():
            question = form.save(commit=False)
            question.author = request.user
            question.save()
            return redirect('home')
    else:
        form = QuestionForm()
    return render(request, 'core/post_question.html', {'form': form})

@login_required
def delete_question(request, question_id):
    question = get_object_or_404(Question, id=question_id)
    if request.user == question.author:
        question.delete()
        return JsonResponse({'success': True})
    return HttpResponseForbidden()


@login_required
def delete_answer(request, answer_id):
    answer = get_object_or_404(Answer, id=answer_id)
    if request.user == answer.author:
        answer.delete()
        return JsonResponse({'success': True})
    return HttpResponseForbidden()
