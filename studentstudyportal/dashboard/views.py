from cgitb import text
from doctest import Example
from email import message
from gc import is_finalized
import imp
from multiprocessing import context
from turtle import title
from django.shortcuts import redirect, render
from django.views import generic
from .forms import  Homeworkform, Noteform,DashbordForm, Todoform, UserRegistrationform
from .models import Homework, Notes, Todo_model
from django.contrib import messages
from youtubesearchpython import VideosSearch
import requests
import wikipedia
from django.contrib.auth.decorators import login_required


# Create your views here.
def home(request):
    return render(request,'dashboard/home.html')

    
@login_required
def notes(request):
    if request.method == 'POST':
        form = Noteform(request.POST)
        if form.is_valid():
            notes = Notes(user=request.user,title=request.POST['title'],description = request.POST['description'])
            notes.save()
        messages.success(request,f'Notes added from {request.user.username} successfully')
    else:
        form = Noteform()
    form =Noteform()
    notes = Notes.objects.filter(user=request.user)
    context = {'notes':notes,'form':form}
    return render(request,'dashboard/notes.html',context)

@login_required
def delete(request,pk=None):
    id=pk
    destroy = Notes.objects.get(id=id)
    destroy.delete()
    return redirect('notes')


class NotesdetailView(generic.DetailView):
    model = Notes

@login_required
def homework(request):
    if request.method == "POST":
        form = Homeworkform(request.POST)
        if form.is_valid():
            try:
                finished = request.POST['iS_finished']
                if finished == 'on':
                    finished = True
            except:
                finished =False
        homeworks = Homework(
            user = request.user,
            subject = request.POST['subject'],
            title = request.POST['title'],
            description = request.POST['description'],
            due = request.POST['due'],
            iS_finished = finished
        )
        homeworks.save()
        form = Homeworkform()
        messages.success(request,f"homework is uploaded successfuly")
    else:
        form = Homeworkform()
    
    home = Homework.objects.filter(user=request.user)
    if len(home) == 0:
        homework_done = True
    else:
        homework_done=False
    context = {'form':form,'home':home,'homework_done':homework_done}
    return render(request,"dashboard/homework.html",context)

@login_required
def update_homework(request,pk=None):
    home = Homework.objects.get(id=pk)
    if home.iS_finished == True:
        home.iS_finished = False
    else:
        home.iS_finished = True
    home.save()
    return redirect('homework')

@login_required
def delete_homework(request,pk=None):
    Homework.objects.get(id=pk).delete()
    return redirect('homework')


def youtube(request):
    if request.method == "POST":
        form = DashbordForm(request.POST)
        search = request.POST['search']
        video = VideosSearch(search,limit=10)
        result_list = []
        for i in video.result()['result']:
            result_dict = {
                'input' : search,
                'title': i['title'],
                'duration': i['duration'],
                'thumbnail': i['thumbnails'][0]['url'],
                'channel': i['channel']['name'],
                'link': i['link'],
                'views': i['viewCount']['short'],
                'published': i['publishedTime'],
            }
            desc = ''
            if i['descriptionSnippet']:
                for j in i['descriptionSnippet']:
                    desc += j['text']
            result_dict['descriptionSnippet'] = desc
            result_list.append(result_dict)
            context = {
                'form':form,
                'results': result_list
            }
        return render(request,'dashboard/youtube.html',context)
    else:
        form = DashbordForm()
    context = {'form':form}
    return render(request,'dashboard/youtube.html',context)
        


                            
@login_required
def Todo(request):
    if request.method == "POST":
        form = Todoform(request.POST)
        if form.is_valid():
            try:
                finished = request.POST['iS_finished']
                if finished == 'on':
                    finished = True
            except:
                finished =False
        todos = Todo_model(
            user = request.user,
            title = request.POST['title'],
            iS_finished = finished)
        todos.save()
        messages.success(request,f"todo added from {request.user.username}")
    else:
        form = Todoform()
    form = Todoform()
    todo = Todo_model.objects.filter(user=request.user)
    if len(todo) == 0:
        todo_done = True
    else:
        todo_done=False
    context = {'form':form,'todos':todo,'todo_done':todo_done}
    return render(request,"dashboard/todo.html",context)

@login_required
def update_todo(request,pk=None):
    home = Todo_model.objects.get(id=pk)
    if home.iS_finished == True:
        home.iS_finished = False
    else:
        home.iS_finished = True
    home.save()
    return redirect('todo')

@login_required
def delete_todo(request,pk=None):
    Todo_model.objects.get(id=pk).delete()
    return redirect('todo')


def books(request):
    if request.method == "POST":
        form = DashbordForm(request.POST)
        search = request.POST['search']
        url = "https://www.googleapis.com/books/v1/volumes?q="+search
        r = requests.get(url)
        answer = r.json()
        result_list = []
        for i in range(10):
            result_dict = {
                'title': answer['items'][i]['volumeInfo']['title'],
                'subtitle': answer['items'][i]['volumeInfo'].get('subtitle'),
                'description': answer['items'][i]['volumeInfo'].get('decription'),
                'count': answer['items'][i]['volumeInfo'].get('pageCount'),
                'categories': answer['items'][i]['volumeInfo'].get('categories'),
                'ratings': answer['items'][i]['volumeInfo'].get('pageRating'),
                'thumbnail': answer['items'][i]['volumeInfo'].get('imageLinks').get('thumbnail'),
                'preview': answer['items'][i]['volumeInfo'].get('previewLink'),
            }
            result_list.append(result_dict)
            context = {
                'form':form,
                'results': result_list
            }
        return render(request,'dashboard/books.html',context)
    else:
        form = DashbordForm()
    context = {'form':form}
    return render(request,'dashboard/books.html',context)


def dictionary(request):
    if request.method == "POST":
        form = DashbordForm(request.POST)
        search = request.POST['search']
        url = "https://api.dictionaryapi.dev/api/v2/entries/en_US/"+search
        r = requests.get(url)
        answer = r.json()
        try:
            phonetics = answer[0]['phonetics'][0]['search']
            audio  = answer[0]['phonetics'][0]['audio']
            definition = answer[0]['meanings'][0]['definitions'][0]['definition']
            example = answer[0]['meanings'][0]['definitions'][0]['example']
            synonyms = answer[0]['meanings'][0]['definitions'][0]['synonyms']
            context = {
                'form':form,
                'input': search,
                'phonetics': phonetics,
                'audio': audio,
                'definition':definition,
                'example': example,
                'synonyms': synonyms
            }
        except:
            context = {'form':form,
            'input': ''}
        return render(request,"dashboard/dictionary.html",context)
    else:
        form = DashbordForm()
        context = {'form':form}
    form = DashbordForm()
    return render(request,"dashboard/dictionary.html",context)

def wiki(request):
    if request.method == "POST":
        text  = request.POST['search']
        form = DashbordForm(request.POST)
        search = wikipedia.page(text)
        context  = {
            'form':form,
            'title': search.title,
            'link': search.url,
            'details': search.summary
        }
        return render(request,"dashboard/wiki.html",context)
    else:
        form = DashbordForm()
        context = {
            'form':form
        }
    
    return render(request,"dashboard/wiki.html",context)

def register(request):
    if request.method == 'POST':
        form = UserRegistrationform(request.POST)
        if form.is_valid():
            form.save()
            username  =  form.cleaned_data.get('username')
            messages.success(request,f'Account created for {request.user.username} successfully')
            return redirect('login')
    else:
        form = UserRegistrationform()
    form = UserRegistrationform()
    context = {
        'form':form
    }
    return render(request,"dashboard/register.html",context)
@login_required
def profile(request):
    homeworks = Homework.objects.filter(iS_finished=False,user = request.user)
    todos = Todo_model.objects.filter(iS_finished=False,user = request.user)
    if len(homeworks) == 0:
        homework_done = True
    else:
        homework_done=False
    if len(todos) == 0:
        todo_done = True
    else:
        todo_done=False
    context = {'homeworks':homeworks,
    'todos': todos,
    'homework_done':homework_done,
    'todo_done': todo_done}
    return render(request,'dashboard/profile.html',context)




