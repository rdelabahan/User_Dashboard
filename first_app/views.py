from django.shortcuts import render, redirect
from django.contrib import messages
from .models import User, Message, Comment
import bcrypt

def index(request):
    return render(request, 'index.html')

def sign_in(request):
    return render(request, 'sign.html')

def register(request):
    return render(request, 'register.html')

def create_user(request):
    if request.method == "GET":
        return redirect('/')
    errors = User.objects.basic_validator(request.POST)
    if errors:
        for key, value in errors.items():
            messages.error(request, value)
        return redirect("/register")
    else:
        
        pw_hash = bcrypt.hashpw(request.POST["pw"].encode(), bcrypt.gensalt()).decode()
        this_user = User.objects.create(
            first_name = request.POST["fname"],
            last_name = request.POST["lname"],
            email = request.POST["email"],
            password = pw_hash,
        )
        if this_user.id == 1:
            this_user.level_admin = 9
            this_user.save()
        messages.success(request, 'You have successfully registered!')
        return redirect("/register")

def authenticate(request):
    if request.method == "GET":
        return redirect('/sign_in')
    try:
        user = User.objects.get(email = request.POST["l_email"])
    except:
        messages.error(request, "Incorrect email address or password.")
        return redirect('/sign_in')
    
    if bcrypt.checkpw(request.POST['l_pw'].encode(), user.password.encode()):
        request.session['user_id'] = user.id
        request.session['user_first_name'] = user.first_name
        request.session['user_last_name'] = user.last_name
        request.session['user_email'] = user.email
        request.session['user_level'] = user.level_admin
        if request.session['user_level'] == 9:
            return redirect('/dashboard/admin')
        else:
            return redirect('/dashboard')
        return redirect('/dashboard')
    else:
        messages.error(request, "Incorrect email address or password.")
        return redirect('/sign_in')

def display_dashboard_admin(request):
    context = {
        'users': User.objects.all(),
    }
    return render(request, 'admin_dashboard.html',context)

def display_dashboard(request):
    context = {
        'users': User.objects.all(),
    }
    return render(request, 'dashboard.html',context)

def logout(request):
    if 'user_id' in request.session:
        del request.session['user_id']
    if 'user_first_name' in request.session:
        del request.session['user_first_name']
    if 'user_last_name' in request.session:
        del request.session['user_last_name']
    if 'user_email' in request.session:
        del request.session['user_email']
    if 'user_level' in request.session:
        del request.session['user_level']
    return redirect('/')

def new(request):
    return render(request, 'new.html')

def add_new_user(request):
    if request.method == "GET":
        return redirect('/')
    errors = User.objects.basic_validator(request.POST)
    if errors:
        for key, value in errors.items():
            messages.error(request, value)
        return redirect("/users/new")
    else:
        pw_hash = bcrypt.hashpw(request.POST["pw"].encode(), bcrypt.gensalt()).decode()
        User.objects.create(
            first_name = request.POST["fname"],
            last_name = request.POST["lname"],
            email = request.POST["email"],
            password = pw_hash,
        )
        messages.success(request, 'You have successfully added a new user!')
        return redirect("/users/new")

def delete_user(request, user_id):

    logged_user = User.objects.get(id = request.session['user_id'])
    this_user = User.objects.get(id = user_id)
    if this_user.id == logged_user.id:
        if 'user_id' in request.session:
            del request.session['user_id']
        if 'user_first_name' in request.session:
            del request.session['user_first_name']
        if 'user_last_name' in request.session:
            del request.session['user_last_name']
        if 'user_email' in request.session:
            del request.session['user_email']
        if 'user_level' in request.session:
            del request.session['user_level']
        this_user.delete()
        return redirect('/')
    elif this_user.id == 1:
        messages.error(request, "You can't delete the main admin user.")
        return redirect('/dashboard/admin')
    else:
        this_user.delete()
        return redirect('/dashboard/admin')
    

def display_user(request, user_id):
    context = {
        'user': User.objects.get(id = user_id)
    }
    return render(request, 'edit.html', context)

def update_user(request, user_id):
    errors = User.objects.update_validator(request.POST, user_id)
    if errors:
        for k, v in errors.items():
            messages.error(request, v)
        return redirect(f'/users/edit/{user_id}')
    else:
        this_user = User.objects.get(id = user_id)
        if this_user.id == 1:
            messages.error(request, "You are the main admin. Main admin can't be a normal user.")
            return redirect(f'/users/edit/{user_id}')
        else:
            this_user.email = request.POST['email']
            this_user.first_name = request.POST['fname']
            this_user.last_name = request.POST['lname']
            this_user.level_admin = request.POST['level_admin']
            this_user.save()
            messages.success(request, 'User info successfully updated!')
            return redirect(f'/users/edit/{user_id}')

def change_password(request, user_id):
    errors = User.objects.pw_validator(request.POST)
    if errors:
        for k, v in errors.items():
            messages.error(request, v)
        return redirect(f'/users/edit/{user_id}')
    else:
        pw_hash = bcrypt.hashpw(request.POST["pw"].encode(), bcrypt.gensalt()).decode()
        this_user = User.objects.get(id = user_id)
        this_user.password = pw_hash
        this_user.save()
        messages.success(request, 'User password successfully changed!')
        return redirect(f'/users/edit/{user_id}')

def display_user_profile(request):
    context = {
        'user': User.objects.get(id = request.session['user_id']),
    }
    return render(request, 'edit_profile.html', context)

def normal_user_update(request):
    this_user = User.objects.get(id = request.session['user_id'])
    errors = User.objects.profile_validator(request.POST, request)
    if errors:
        for k, v in errors.items():
            messages.error(request, v)
        return redirect(f'/users/edit')
    else:
        this_user.email = request.POST['email']
        this_user.first_name = request.POST['fname']
        this_user.last_name = request.POST['lname']
        this_user.save()
        messages.success(request, 'User info successfully updated!')
        return redirect(f'/users/edit')

def change_pw(request):
    errors = User.objects.pw_validator(request.POST)
    if errors:
        for k, v in errors.items():
            messages.error(request, v)
        return redirect(f'/users/edit')
    else:
        pw_hash = bcrypt.hashpw(request.POST["pw"].encode(), bcrypt.gensalt()).decode()
        this_user = User.objects.get(id = request.session['user_id'])
        this_user.password = pw_hash
        this_user.save()
        messages.success(request, 'User password successfully changed!')
        return redirect(f'/users/edit')

def update_description(request):
    errors = User.objects.description_validator(request.POST)
    if errors:
        for k, v in errors.items():
            messages.error(request, v)
        return redirect(f'/users/edit')
    else:
        this_user = User.objects.get(id = request.session['user_id'])
        this_user.description = request.POST['description']
        this_user.save()
        messages.success(request, 'Description successfully updated!')
        return redirect(f'/users/edit')

def show_user_wall(request, user_id):
    context = {
        'user': User.objects.get(id = user_id),
    }
    return render(request,'user_wall.html', context)

def create_message(request, user_id):
    this_user = User.objects.get(id = request.session['user_id'])
    this_receiver = User.objects.get(id = user_id)
    Message.objects.create(
        message = request.POST['message'],
        user = this_user,
        receiver = this_receiver,
    )
    return redirect(f'/users/show/{user_id}')

def create_comment(request, message_id, user_id):
    this_user = User.objects.get(id = request.session['user_id'])
    this_message = Message.objects.get(id = message_id)
    Comment.objects.create(
        comment = request.POST['comment'],
        user = this_user,
        message = this_message,
    )
    return redirect(f'/users/show/{user_id}')