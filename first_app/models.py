from django.db import models
import re

class UserManager(models.Manager):

    def basic_validator(self, post_data):
        errors = {}

        name_regex = re.compile(r"^[a-zA-Z]+$")
        email_regex = re.compile(r"^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$")

        if not name_regex.match(post_data["fname"]):
            errors["fname"] = "First name should consist of alphabetical characters only"
        if not name_regex.match(post_data["lname"]):
            errors["lname"] = "Last name should consist of alphabetical characters only"
        if not email_regex.match(post_data["email"]):
            errors["email"] = "Email is invalid"

        if post_data["fname"] == "" or len(post_data["fname"]) < 2 or len(post_data["fname"]) > 50:
            errors["fname"] = "First name should have 2 characters to 50 characters long"
        if post_data["lname"] == "" or len(post_data["lname"]) < 2 or len(post_data["lname"]) > 50:
            errors["lname"] = "Last name should have 2 characters to 50 characters long"
        if post_data["email"] == "" or len(post_data["email"]) < 2 or len(post_data["email"]) > 50:
            errors["email"] = "Email should have 2 characters to 50 characters long"
        if post_data["pw"] == "" or len(post_data["pw"]) < 8 or len(post_data["pw"]) > 50:
            errors["pw"] = "Password should be at least 8 characters"
        if post_data["pw"] != post_data["confirm_pw"]:
            errors["confirm_pw"] = "Password and confirm password should match."


        try:
            self.get(email=post_data["email"])
            errors["email"] = "Email already in use."
        except:
            pass
        return errors

    def update_validator(self, post_data, user_id):
        errors = {}

        name_regex = re.compile(r"^[a-zA-Z]+$")
        email_regex = re.compile(r"^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$")

        if not name_regex.match(post_data["fname"]):
            errors["fname"] = "First name should consist of alphabetical characters only"
        if not name_regex.match(post_data["lname"]):
            errors["lname"] = "Last name should consist of alphabetical characters only"
        if not email_regex.match(post_data["email"]):
            errors["email"] = "Email is invalid"

        if post_data["fname"] == "" or len(post_data["fname"]) < 2 or len(post_data["fname"]) > 50:
            errors["fname"] = "First name should have 2 characters to 50 characters long"
        if post_data["lname"] == "" or len(post_data["lname"]) < 2 or len(post_data["lname"]) > 50:
            errors["lname"] = "Last name should have 2 characters to 50 characters long"
        if post_data["email"] == "" or len(post_data["email"]) < 2 or len(post_data["email"]) > 50:
            errors["email"] = "Email should have 2 characters to 50 characters long"
        
        this_user_email = User.objects.get(id = user_id).email
        if post_data['email'] != this_user_email:
            this_email = User.objects.filter(email = post_data['email'])
            if len(this_email) > 0:
                errors['email'] = 'Email already exists.'

        return errors

    def pw_validator(self, post_data):
        errors = {}

        if post_data["pw"] == "" or len(post_data["pw"]) < 8 or len(post_data["pw"]) > 50:
            errors["pw"] = "Password should be at least 8 characters"
        if post_data["pw"] != post_data["confirm_pw"]:
            errors["confirm_pw"] = "Password and confirm password should match."

        return errors

    def profile_validator(self, post_data, request):
        errors = {}

        this_user_email = User.objects.get(id = request.session['user_id']).email
        if post_data['email'] != this_user_email:
            this_email = User.objects.filter(email = post_data['email'])
            if len(this_email) > 0:
                errors['email'] = 'Email already exists.'
        if post_data["fname"] == "" or len(post_data["fname"]) < 2 or len(post_data["fname"]) > 50:
            errors["fname"] = "First name should have 2 characters to 50 characters long"
        if post_data["lname"] == "" or len(post_data["lname"]) < 2 or len(post_data["lname"]) > 50:
            errors["lname"] = "Last name should have 2 characters to 50 characters long"
        
        return errors

    def description_validator(self, post_data):
        errors = {}

        if len(post_data['description']) < 10:
            errors['description'] = 'Description should have at least 10 characters.'
        
        return errors



class User(models.Model):
    first_name = models.CharField(max_length = 50)
    last_name = models.CharField(max_length = 50)
    email = models.CharField(max_length = 384, unique = True)
    level_admin = models.IntegerField(default=1)
    description = models.TextField(null = True)
    password = models.CharField(max_length = 60)
    created_at = models.DateTimeField(auto_now_add = True)
    updated_at = models.DateTimeField(auto_now = True)

    objects = UserManager()

class Message(models.Model):
    message = models.TextField()
    user = models.ForeignKey(User, related_name = 'sent_messages', on_delete = models.CASCADE)
    receiver = models.ForeignKey(User, related_name = 'wall_messages', on_delete = models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    

class Comment(models.Model):
    comment = models.TextField()
    message = models.ForeignKey(Message, related_name = 'comments', on_delete = models.CASCADE)
    user = models.ForeignKey(User, related_name = 'comments', on_delete = models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

