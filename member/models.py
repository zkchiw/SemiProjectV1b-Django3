from datetime import datetime
from django.db import models

class Member(models.Model):
    id=models.AutoField(primary_key=True)
    userid=models.CharField(max_length=18, unique=True)
    passwd=models.CharField(max_length=18)
    name=models.CharField(max_length=5)
    email=models.CharField(max_length=100)
    regdate=models.DateTimeField(default=datetime.now)

    class Meta :
        db_table = 'member' # 테이블 생성시 이름 지정
        ordering = ['-regdate'] # 정렬기준 설정

    def __str__(self):
        return self.userid  # 객체 출력시 출력형태 정의

