from django.shortcuts import render, redirect
from django.contrib import messages
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from .models import Room, Topic, Message
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import UserCreationForm
from django.db.models import Q
from .forms import RoomForm

# rooms=[
#     {'id': 1, 'name': 'Lets learn python'},
#     {'id': 2, 'name': 'Design with me'},
#     {'id': 3, 'name': 'Fronend developers'},
# ]

def loginPage(request):
    page = 'login'
    if request.user.is_authenticated:
        return redirect('home')

    if request.method == 'POST':
        username= request.POST.get('username').lower()
        password = request.POST.get('password')
        try: 
            user= User.objects.get(username=username)
        except:
            messages.error(request, 'User does not exists')

        user = authenticate(request, username=user, password=password)
        if user is not None:
            login(request, user)#the user will be oficcilay loged in
            return redirect('home')
        else:
            messages.error(request, 'Username or Password does not exist')

    context={'page':page}
    return render(request, 'base/loging_register.html', context) #we use render to show something, to render something

def logoutUser(request):
    logout(request)
    return redirect('home') #we use redirect to change the page

def registerUser(request):
    form = UserCreationForm()
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.username = user.username.lower()
            user.save()
            login(request, user)
            return redirect('home')
        else:
            messages.error(request, 'An error ocurred during registration')

    context={'form':form}
    return render(request, 'base/loging_register.html', context)

def home(request):
    q=request.GET.get('q') if request.GET.get('q') != None else ''
    rooms= Room.objects.filter(
        Q(topic__name__icontains=q) | #Q allows us to use & (and) | (or) in our queries.
        Q(name__icontains=q) |
        Q(description__icontains=q) |
        Q(host__username__icontains=q)
        )#We use double underscore to refer the object due to it is a foreign key.
    #and we use icontains so that it retrieves every instance that contains q on it. like regular expressions
    room_count=rooms.count()
    topics = Topic.objects.all()
    room_messages = Message.objects.filter(Q(room__topic__name__icontains=q))

    context={'rooms':rooms, 'topics':topics, 'room_count': room_count, 'room_messages':room_messages}
    return render(request, 'base/home.html', context)#cuando lo pasamos aqui ya está disponible en la template, es como las properties en react.

def room(request, pk):
    room = Room.objects.get(id=pk)
    # comments = Message.objects.filter(room=pk)
    comments = room.message_set.all() #This is another way to do it, by passing the name of the model+_set, it will retrieve all of the messages related to this room thanks to the foreign key
    participants= room.participants.all()
    if request.method == 'POST':
        message= Message.objects.create(
            user=request.user,
            room=room,
            body=request.POST.get('body')
        )
        room.participants.add(request.user)
        return redirect('room', pk=room.id)
    
    context = {'room':room, 'comments':comments, 'participants':participants}
    return render(request, 'base/room.html', context)

def userProfile(request, pk):
    user = User.objects.get(id = pk)
    rooms = user.room_set.all()
    room_messages = user.message_set.all()
    topics = Topic.objects.all()
    context = {'user': user, 'rooms':rooms, 'room_messages': room_messages, 'topics':topics}
    return render(request, 'base/profile.html', context)

@login_required(login_url='/login')#to restrict this pages only to loggedin users
def createRoom(request):
    form = RoomForm()
    if request.method=='POST':
        #print(request.POST) in console
        form=RoomForm(request.POST)
        if form.is_valid():
            room=form.save(commit=False)#This gives us an instance of the formof our Room model
            room.host = request.user
            room.save()
            return redirect('home')#Utilizamos el nombre de nuestra url en lugar del path como tal.

    context = {'form':form}
    return render(request, 'base/room_form.html', context)

@login_required(login_url='/login')
def updateRoom(request, pk):
    room=Room.objects.get(id=pk)
    form = RoomForm(instance=room)#this attribute is usefull for us because it wont create a new register, it will give you that instance

    if request.user != room.host:
        return HttpResponse('You are not allowed here!!')

    if request.method=='POST':
        form=RoomForm(request.POST, instance=room)
        if form.is_valid():
            form.save()
            return redirect('home')

    context={'form':form}
    return render(request, 'base/room_form.html', context)

@login_required(login_url='/login')
def deleteRoom(request, pk):
    room = Room.objects.get(id=pk)

    if request.user != room.host:
        return HttpResponse('You are not allowed here!!')

    if request.method=='POST':
        room.delete()
        return redirect('home')
    return render(request, 'base/delete.html', {'obj': room})

@login_required(login_url='/login')
def deleteMessage(request, pk):
    message = Message.objects.get(id=pk)

    if request.user != message.user:
        return HttpResponse('You are not allowed here!!')

    if request.method=='POST':
        comments = message.room.message_set.filter(user__exact=message.user)
        if comments.count() == 1:
            message.room.participants.remove(request.user)

        message.delete()
        return redirect('home')
    return render(request, 'base/delete.html', {'obj': message})
