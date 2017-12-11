from django.db import models

# Create your models here.

class User(models.Model):
    '''用户表'''
    username=models.CharField(max_length=32)
    password=models.CharField(max_length=32)

    def __str__(self):
        return self.username
class Room(models.Model):
    '''会议室表'''
    name=models.CharField(verbose_name="会议室名",max_length=32)


    def __str__(self):
        return self.name
class RoomDetail(models.Model):
    '''会议室详细信息'''
    time_choice=(
        (1,"上午八点"),(2, "上午九点"),(3, "上午十点"),(4, "上午十一点"),
        (5,"上午十二点"),(6, "下午一点"),(7, "下午两点"),(8, "下午三点"),
        (9, "下午四点"),(10,"下午五点"),(11, "下午六点"),(12,"下午七点"),
    )
    time=models.IntegerField(verbose_name="选择时间段",choices=time_choice)
    room=models.ForeignKey(verbose_name="选择会议室",to="Room")
    reservation=models.ForeignKey(verbose_name="预约人",to="User")
    create_time=models.DateField(verbose_name="预约时间")

