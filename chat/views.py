from django.http import Http404
from django.shortcuts import render
from django.contrib.auth.decorators import login_required


from .models import ChatRoom, User


# Create your views here.
def index(request):
    return render(request,'chat/index.html')



def room(request,room_name):

    if(request.user.is_authenticated):
        user_name=request.user.username
        print(user_name)
        if(room_name=='david_jide'):
            try:
                room=ChatRoom.objects.get(room_name=room_name)
            except ChatRoom.DoesNotExist:
                chat_room=ChatRoom.objects.create(room_name=room_name)
                david=User.objects.get(username='david')
                jide=User.objects.get(username='jide')
                chat_room.users.add(david)
                chat_room.users.add(jide)
                chat_room.save()

            return render(request,'chat/room.html',{'room_name':room_name,'user_name':user_name})

    raise Http404