from django.urls import path
from . import views
urlpatterns = [
    path('', views.home),
    path('message/create', views.post_message),
    path('message/delete', views.message_delete),
    path('comment/create', views.comment_create),
    path('comment/delete', views.comment_delete),
]