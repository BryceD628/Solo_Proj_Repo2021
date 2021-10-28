from django.db import models
from apps.login_app.models import User

class Post_Manager(models.Manager):
    def post_validator(self, post_data):
        errors = {}
        if len(post_data['message']) < 5:
            errors['message'] = "Post must be longer than 5 characters."
        if len(post_data['comment']) < 5:
            errors['comment'] = "Comment must be longer than 5 characters."
        return errors


class Message(models.Model):
    message = models.TextField()
    created_at = models.DateTimeField(auto_now_add= True)
    updated_at = models.DateTimeField(auto_now= True)
    user_id = models.ForeignKey(User, related_name='user_messages', on_delete=models.CASCADE)
    objects = Post_Manager()


class Comment(models.Model):
    comment = models.TextField()
    created_at = models.DateTimeField(auto_now_add= True)
    updated_at = models.DateTimeField(auto_now= True)
    message_id = models.ForeignKey(Message, related_name='message_comments', on_delete=models.CASCADE)
    user_id = models.ForeignKey(User, related_name='user_comments', on_delete=models.CASCADE)
    objects = Post_Manager()