from django.shortcuts import render, redirect, HttpResponse
from apps.login_app.models import User
from .models import Message, Comment
from django.contrib import messages


def home(request):
    if 'user_id' not in request.session:
        messages.error(request, "You must log in to view that page.")
        return redirect('/')
    this_user = User.objects.filter(id = request.session['user_id'])[0]
    context = {
        'this_user' : this_user,
        'user_messages' : Message.objects.filter(user_id = this_user.id),
        'all_posts' : Message.objects.all(),
    }
    return render(request, 'home.html', context)

def post_message(request):
    if request.method != 'POST' or 'user_id' not in request.session:
        return redirect('/')
    current_user = User.objects.filter(id = request.session['user_id'])[0]
    new_message = Message.objects.create(
        message = request.POST['message'],
        user_id = current_user,
    )
    return redirect('/wall')

def message_delete(request):
    if request.method != 'POST' or 'user_id' not in request.session:
        return redirect('/')
    this_message = Message.objects.filter(id = request.POST['message_id'])
    this_message.delete()
    return redirect('/wall')

def comment_create(request):
    if request.method == 'POST':
        current_user = User.objects.filter(id = request.session['user_id'])[0]
        new_comment = Comment.objects.create(
            comment = request.POST['message_comment'],
            user_id = current_user,
            message_id = Message.objects.filter(id = request.POST['message_id'])[0],
        )
    return redirect('/wall')

def comment_delete(request):
    if request.method != 'POST' or 'user_id' not in request.session:
        return redirect('/')
    this_comment = Comment.objects.filter(id = request.POST['comment_id'])
    this_comment.delete()
    return redirect('/wall')

def selected_message(request, message_id):
    selected_post = Message.objects.get(id = message_id)
    context = {
        'id' : selected_post.id,
        'message' : selected_post.message,
    }
    return render(request, 'post.html', context)