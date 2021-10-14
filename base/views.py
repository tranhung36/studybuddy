from django.contrib.auth.models import User
from django.contrib import messages
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import authenticate, login, logout
from django.db.models import Q
from .models import (
    Message,
    Room,
    Topic,
    Whiteboard
)
from .forms import RoomForm, UserForm
import uuid


def create_uuid():
    return uuid.uuid4()


def login_page(request):
    page = 'login'
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        try:
            user = User.objects.get(username=username)
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                messages.success(request, 'Login successfully!')
                return redirect('home')
            else:
                messages.error(request, 'Invalid password')
        except:
            messages.error(request, 'User does not exists')

    context = {'page': page}
    return render(request, 'base/login_register.html', context)


def register_page(request):
    form = UserCreationForm()
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            login(request, form)
            return redirect('home')
        else:
            messages.error(request, 'An error occurred during registration ')
    return render(request, 'base/login_register.html', {'form': form})


def logout_page(request):
    logout(request)
    messages.warning(request, 'Logout successfully!')
    return redirect('login')


def home(request):
    q = request.GET.get('q') if request.GET.get('q') != None else ''
    rooms = Room.objects.filter(
        Q(topic__name__icontains=q) |
        Q(name__icontains=q) |
        Q(description__icontains=q)
    )
    topics = Topic.objects.all()
    room_activity = Message.objects.filter(
        Q(room__topic__name__icontains=q) |
        Q(room__name__icontains=q) |
        Q(room__description__icontains=q)
    )
    context = {'rooms': rooms, 'topics': topics,
               'room_activity': room_activity}
    return render(request, 'base/home.html', context)


def user_profile(request, pk):
    user = User.objects.get(id=pk)
    rooms = user.room_set.all()
    topics = Topic.objects.all()
    room_activity = user.message_set.all()
    context = {'user': user, 'rooms': rooms,
               'topics': topics, 'room_activity': room_activity}
    return render(request, 'base/profile.html', context)


def room(request, pk):
    room = Room.objects.get(id=pk)
    room_messages = room.message_set.all()
    participants = room.participants.all()
    if request.method == 'POST':
        message = Message.objects.create(
            user=request.user,
            room=room,
            body=request.POST.get('body')
        )
        room.participants.add(request.user)
        return redirect('room', pk=room.id)
    context = {'room': room, 'room_messages': room_messages,
               'participants': participants}
    return render(request, 'base/room.html', context)


@login_required(login_url='login')
def create_room(request):
    form = RoomForm()
    topics = Topic.objects.all()
    if request.method == 'POST':
        topic_name = request.POST.get('topic')
        topic = Topic.objects.get(name=topic_name)
        Room.objects.create(
            host=request.user,
            topic=topic,
            name=request.POST.get('name'),
            description=request.POST.get('description')
        )
        return redirect('home')
    context = {'form': form, 'topics': topics}
    return render(request, 'base/room_form.html', context)


@login_required(login_url='login')
def update_room(request, pk):
    room = Room.objects.get(id=pk)
    topics = Topic.objects.all()
    form = RoomForm(instance=room)
    if request.method == 'POST':
        topic_name = request.POST.get('topic')
        topic = Topic.objects.get(name=topic_name)
        room.name = request.POST.get('name')
        room.topic = topic
        room.description = request.POST.get('description')
        room.save()
        return redirect('room', pk=room.id)
    context = {'form': form, 'topics': topics}
    return render(request, 'base/room_form.html', context)


@login_required(login_url='login')
def delete_room(request, pk):
    room = Room.objects.get(id=pk)
    if request.method == 'POST':
        room.delete()
        return redirect('home')
    context = {'obj': room}
    return render(request, 'base/delete.html', context)


@login_required(login_url='login')
def delete_message(request, pk):
    message = Message.objects.get(id=pk)
    if request.method == 'POST':
        message.delete()
        return redirect('home')
    context = {'obj': message}
    return render(request, 'base/delete.html', context)


@login_required(login_url='login')
def update_profile(request):
    return render(request, 'base/update_profile.html')


def white_board(request, pk):
    room = Room.objects.get(id=pk)
    wb_id = Whiteboard.objects.create(wid=create_uuid())
    if request.method == "POST":
        room.wb_id = wb_id
        room.save()
        return redirect('room', pk=room.id)
    context = {'room': room}
    return render(request, 'scripts.html', context)


def update_profile(request):
    user = request.user
    form = UserForm(instance=user)
    if request.method == 'POST':
        form = UserForm(request.POST, instance=user)
        if form.is_valid():
            form.save()
            return redirect('user-profile', pk=user.id)
    context = {'form': form}
    return render(request, 'base/update_profile.html', context)
