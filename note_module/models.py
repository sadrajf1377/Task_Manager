from django.db import models
from user_module.models import User_Model

# Create your models here.
class User_Note(models.Model):
    imp_choices=(('high','high'),('moderate','moderate'),('low','low'))
    note_importance=models.CharField(choices=imp_choices,db_index=True,null=False,blank=False,max_length=20,verbose_name='how important is this note')
    author=models.ForeignKey(User_Model,on_delete=models.CASCADE,null=False,blank=False,related_name='notes',db_index=True,verbose_name='who wrote this note')
    date_created=models.DateField(verbose_name='when was this note created',auto_now_add=True)
    title=models.CharField(max_length=200,verbose_name='title of note',null=False,blank=False)
    content=models.TextField(verbose_name='main text of this note',db_index=True)
    attached_file=models.FileField(null=True,blank=True,verbose_name='the attached file of this note (optional)')
    class Meta:
        verbose_name='user_note'
        verbose_name_plural='users_notes'
        db_table='notes'




