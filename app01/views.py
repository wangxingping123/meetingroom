import json
from django.shortcuts import render,HttpResponse,redirect
from django.http import JsonResponse
from app01 import models


def login(request):
    if request.is_ajax():
        username = request.POST.get("username")
        password = request.POST.get("password")
        data = {"flag": False}
        user = models.User.objects.filter(username=username, password=password).first()
        if user:
            request.session["user"]={"username":user.username,"user_id":user.id}
            data["flag"] = True

        return HttpResponse(json.dumps(data))

    return render(request, "login.html")



def index(request):

    user_id=request.session["user"].get("user_id")
    if not user_id:
        return redirect("/login/")

    if request.method =="POST":
        '''保存用户的预定信息'''
        data={"flag":True,}
        reserve_list=json.loads(request.body.decode("utf8")) #取出预定信息

        try:
            objlist=[]
            for info in reserve_list:
                time=info.get("time_slot")
                room_id=info.get("room_id")
                reserve_time=info.get("reserve_time")
                obj=models.RoomDetail(time=time,room_id=room_id,create_time=reserve_time,
                reservation_id=user_id)
                objlist.append(obj)
            models.RoomDetail.objects.bulk_create(objlist)
            data["reserve_time"]=reserve_time
        except:
            data["flag"]=False
        return HttpResponse(json.dumps(data))

    #一天中所有的时间段信息
    time_slot=models.RoomDetail.time_choice
    import datetime
    nowtime=datetime.datetime.now().date()

    return render(request,"index.html",{"time_slot":time_slot,"nowtime":nowtime})


def roominfo(request):



    #获取用户要查询的时间
    date=request.GET.get("date")
    room_dic = {}
    roomlist = models.Room.objects.all()
    for room in roomlist:
        room_dic[room.id] = {"name": room.name, "info": {time[0]: None for time in models.RoomDetail.time_choice}}
    room_detail_list = models.RoomDetail.objects.filter(create_time=date)
    for obj in room_detail_list:
        # 将每一个会议室的预定信息保存到字典中
        room_dic[obj.room_id]["info"][obj.time] = {"name":obj.reservation.username,"id":obj.id}
  
    return JsonResponse(room_dic)

def cancel(request,id):
    #取消预约
    data={"flag":True}
    user_id = request.session["user"].get("user_id")
    try:
        models.RoomDetail.objects.filter(id=id,user_id=user_id).delete()
    except:
        data["flag"]=False
    return JsonResponse(data)