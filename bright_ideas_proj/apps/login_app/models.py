from django.db import models
import re
import bcrypt


class UserManager(models.Manager):
    def register_validator(self, postData):
        EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')
        errors = {}

        if len(postData['first_name']) < 2:
            errors['first_name'] = "First name should be at least 2 characters long."

        if len(postData['last_name']) < 2:
            errors['last_name'] = "Last name should be at least 2 characters long."
    
        if len(postData['email']) == 0:
            errors['email'] = "Email is required."

        if len(postData['password']) < 8:
            errors['password'] = "Password should be at least 8 characters long."

        if postData['password'] != postData['confirm_password']:
            errors['match'] = "Passwords should match."
        return errors

    def login_validator(self, postData):
        errors = {}
        existing_users = User.objects.filter(email = postData['email'])
        print(existing_users)
        if len(postData['email']) == 0:
            errors['email'] = "Email required."
        elif len(existing_users) == 0:
            errors['does_not_exist'] = "Please enter a valid email and password."

        if len(postData['password']) < 8:
            errors['password'] = "Password required."

        elif not bcrypt.checkpw(postData['password'].encode(), existing_users[0].password.encode()):
            errors['mismatch'] = "Please enter a valid email and password."
        return errors



class User(models.Model):
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
    email = models.CharField(max_length=255, unique=True)
    password = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    objects = UserManager()
