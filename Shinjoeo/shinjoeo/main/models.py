from tkinter import CASCADE
from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class NewWord(models.Model):
    id = models.BigAutoField(primary_key=True)
    word = models.CharField(unique=True,max_length=20)
    explain = models.TextField(blank=False)
    like_user_ids = models.ManyToManyField(User,related_name='likeword', blank=True)
    create_time = models.DateTimeField(auto_now_add=True) 
    create_user_id = models.ForeignKey(User, to_field= 'username',related_name = "newword", on_delete=models.CASCADE,db_column="create_user_id")
    likeCnt = models.IntegerField(default=0)
   
    def __str__(self):
        return str(self.word)