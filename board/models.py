from datetime import datetime
from django.db import models
from member.models import Member

# on_delete : CASCADE, DO_NOTHING

class Board(models.Model):
    id= models.AutoField(primary_key=True)
    title = models.CharField(max_length=20)
    member = models.ForeignKey(Member, on_delete=models.CASCADE, related_name='board')
    views = models.IntegerField(default=0)
    regdate = models.DateTimeField(default=datetime.now)
    contents = models.TextField(null=False, blank=False)

    class Meta :
        db_table = 'board'
        ordering = ['-regdate']

    def __str__(self):
        return self.title