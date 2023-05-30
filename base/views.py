from django.shortcuts import render
from agora_token_builder import RtcTokenBuilder
import random
from django.http import JsonResponse
import time
import json
from .models import RoomMember
# Create your views here.
from django.views.decorators.csrf import csrf_exempt

def getToken(request):
    appId = '5e3ab380cc55486ba0e261633e223433'
    appCertificate = 'a927625c40404e1db9b63634a7416e14'
    channelName = request.GET.get('channel')
    uid = random.randint(1,230)
    expirationTimeSeconds = 3600 * 24
    currentTimeStamp = time.time()
    privilegeExpiredTs = currentTimeStamp + expirationTimeSeconds 
    role = 1
    token = RtcTokenBuilder.buildTokenWithUid(appId, appCertificate, channelName, uid, role, privilegeExpiredTs)
    return JsonResponse({'token':token,'uid':uid}, safe= False)


def lobby(request):
    return render(request,'base/lobby.html')

def room(request):
    return render(request,'base/room.html')

@csrf_exempt
def createMember(request):
    data = json.loads(request.body)
    member, created = RoomMember.objects.get_or_create(
        name = data['name'],
        uid = data['uid'],
        room_name = data['room_name']

    )
    return JsonResponse({'name':data['name']},safe=False)


def getMember(request):
    uid = request.GET.get('UID')
    room_name = request.GET.get('room_name')

    member = RoomMember.objects.get(
        uid=uid,
        room_name=room_name
    )

    name = member.name
    return JsonResponse({'name':member.name},safe=False)

@csrf_exempt
def deleteMember(request):
    data = json.loads(request.body)

    member = RoomMember.objects.get(
        name = data['name'],
        uid=data['uid'],
        room_name=data['room_name']
    )

    member.delete()
    return JsonResponse('Member deleted',safe=False)