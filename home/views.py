
from django.shortcuts import render, HttpResponse, redirect
from home.models import Contact
from django.contrib import messages
from blog.models import Post
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
import logging
from django.utils import timezone
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
import json

logger = logging.getLogger(__name__)

def home(request):
    
    response = render(request, 'home/home.html')
     # Log request details
    logger.info('Request processed', extra={
        'remote_host': request.META.get('REMOTE_ADDR', ''),
        'user': request.META.get('REMOTE_USER', ''),
        'auth_user': request.user.username if request.user.is_authenticated else '',
        'date': timezone.now().strftime('%Y-%m-%d %H:%M:%S %z'),  # Add the actual date formatting logic
        'request': f"{request.method} {request.path} {request.META.get('SERVER_PROTOCOL', '')}",
        'status_code': '',  # Add the actual status code
        'bytes_transferred': len(response.content) if response else 0,
    })
    
    
    logger.info('Response sent', extra={
        'remote_host': request.META.get('REMOTE_ADDR', ''),
        'user': request.META.get('REMOTE_USER', ''),
        'auth_user': request.user.username if request.user.is_authenticated else '',
        'date': timezone.now().strftime('%Y-%m-%d %H:%M:%S %z'), # Add the actual date formatting logic
        'request': f"{request.method} {request.path} {request.META.get('SERVER_PROTOCOL', '')}",
        'status_code': response.status_code if response else 0,
        'bytes_transferred': len(response.content) if response else 0,
    })
    return response


def contact(request):
    messages.success(request, 'Welcome To Contact')
    if request.method == 'POST':
        name = request.POST['name']
        email = request.POST['email']
        phone = request.POST['phone']
        content = request.POST['content']
        if len(name) < 3 or len(email) < 5 or len(phone) < 10 or len(content) < 6:
            messages.error(request, 'Please fill the form correctly')
        else:
            contact = Contact(name=name, email=email,
                              phone=phone, content=content)
            contact.save()
            messages.success(request, 'Thank you for submitting Your Form')
    return render(request, 'home/contact.html')


def about(request):
    messages.success(request, 'Welcome To About Page')
    return render(request, 'home/about.html')


def search(request):
    query = request.GET['query']
    if len(query) > 25:
        allPosts = Post.objects.none()
    else:
        allPostsTitle = Post.objects.filter(title__icontains=query)
        allPostsContent = Post.objects.filter(content__icontains=query)
        allPosts = allPostsTitle.union(allPostsContent)
    if allPosts.count() == 0:
        messages.warning(request, 'Search results not found')
    params = {'allPosts': allPosts, 'query': query}
    return render(request, 'home/search.html', params)

@csrf_exempt
def handleSignup(request):
    if request.method == 'POST':
        # Get the post parameters
        username = request.POST['username']
        fname = request.POST['fname']
        lname = request.POST['lname']
        lname = request.POST['lname']
        email = request.POST['email']
        pass1 = request.POST['pass1']
        pass2 = request.POST['pass2']
        # Check for error inputs
        if len(username) > 10:
            messages.error(
                request, 'Your username is too long')
            return redirect('home')
        if not username.isalnum():

            messages.error(
                request, 'Your username is invalid')
            return redirect('home')
        if pass1 != pass2:
            messages.error(
                request, 'Passwords donot match')
            return redirect('home')

        # Create The user
        myuser = User.objects.create_user(username, email, pass1)
        myuser.first_name = fname
        myuser.last_name = lname
        myuser.save()
        messages.success(request, 'Your account has been successfully created')
        return redirect('home')

    else:
        request.HttpResponse('404-Not Found!!')

@csrf_exempt
def handleLogin(request):
    if request.method == 'POST':
        # Get the post parameters
        loginusername = request.POST['loginusername']
        loginpass = request.POST['loginpass']

        user = authenticate(username=loginusername, password=loginpass)

        if user is not None:
            login(request, user)
            messages.success(request, 'Successfully logged in')
            return redirect('home')
        else:
            messages.error(request, 'Invalid username or password')
            return redirect('home')
    return HttpResponse('404- Not Found')


def handleLogout(request):
    logout(request)
    messages.success(request, 'Successfully logged out')
    return redirect('home')

def getUserIPAddress(request):
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    session = request.session
    try:
        session_hash = session['_auth_user_hash']
    except:
        session_hash = "NON LOGGED IN USER"
        
    if x_forwarded_for:
        ip = x_forwarded_for.split(',')[0]
    else:
        ip = request.META.get('REMOTE_ADDR')
        
    if request.user.is_authenticated:
        username = request.user.username
    else:
        username = "NON LOGGED IN USER"
    
    data = {
        "ip_address": ip,
        "session_hash": session_hash,
        "username": username
    }
    
    
    return JsonResponse(data)


@csrf_exempt
def storeClientLogs(request):
    if request.method == "POST":
        logs = json.loads(request.body.decode("utf-8"))

        # Try to read existing logs, initialize as an empty list if the file is empty or not found
        try:
            with open('Client_logger__demo_v1.json', 'r') as file:
                existing_logs = json.load(file)
        except (FileNotFoundError, json.JSONDecodeError):
            existing_logs = []

        # Combine existing logs with new logs
        combined_logs = existing_logs + logs

        # Write the combined logs back to the file
        with open('Client_logger__demo_v1.json', 'w') as file:
            file.write(json.dumps(combined_logs, indent=2))
            file.write('\n')

        return JsonResponse({"status": "Success"})
