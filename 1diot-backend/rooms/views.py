from django.shortcuts import render

# Create your views here.
from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework import status
from django.core.exceptions import ObjectDoesNotExist
from django.apps import apps

from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from .models import Room
from .serializers import *
import random

VOTE_RIGHT_POINTS = 100
ESCAPE_POINTS = 200

@api_view(['GET', 'POST'])
def rooms_list(request):
    if request.method == 'GET':
        data = []
        nextPage = 1
        previousPage = 1
        rooms = Room.objects.all()
        page = request.GET.get('page', 1)
        paginator = Paginator(rooms, 10)
        try:
            data = paginator.page(page)
        except PageNotAnInteger:
            data = paginator.page(1)
        except EmptyPage:
            data = paginator.page(paginator.num_pages)

        serializer = RoomSerializer(data,context={'request': request} ,many=True)
        if data.has_next():
            nextPage = data.next_page_number()
        if data.has_previous():
            previousPage = data.previous_page_number()

        return Response(serializer.data )

    elif request.method == 'POST':
        serializer = RoomSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            try:
                room = Room.objects.get(room_code=request.data["room_code"])
                Questions = apps.get_model('questions', 'Question')
                temp_question_array = []
                print( len(Questions.objects.all()))
                for i in range (0, len(Questions.objects.all())):
                    temp_question_array.append(i + 1)
                #really make it random
                random.shuffle(temp_question_array)
                random.shuffle(temp_question_array)
                random.shuffle(temp_question_array)
                print(temp_question_array)
                room.question_index_array += temp_question_array
                #add this user to the points array, start at zero
                room.user_points.append(0)
                room.host = room.user_list[0]
                room.save()
                return Response(serializer.data, status=status.HTTP_201_CREATED)
            except ObjectDoesNotExist:
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET', 'PUT', 'POST'])
def rooms_detail(request, room):

    try:
        room = Room.objects.get(room_code=room)
    except ObjectDoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    if request.method == 'GET':
        serializer = RoomSerializer(room,context={'request': request})
        return Response(serializer.data)

    elif request.method == 'PUT':
        serializer = RoomSerializer(room, data=request.data,context={'request': request})
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    elif request.method == 'POST':
        room.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

@api_view(['POST'])
def remove_room(request, room):
    try:
        room = Room.objects.get(room_code=room)
    except ObjectDoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    room.delete()
    return Response(status=status.HTTP_204_NO_CONTENT)


@api_view(['POST'])
def add_user(request, room):
    try:
        room = Room.objects.get(room_code=room)
    except ObjectDoesNotExist:
        return Response({"message" : "room does not exist"}, status=status.HTTP_404_NOT_FOUND)
    if request.data["user_name"] in room.user_list:
        return Response({"message" : "username already exists"}, status=status.HTTP_400_BAD_REQUEST)

    
    room.user_list.append(request.data["user_name"])
    room.user_count = len(room.user_list)
    room.user_points.append(0)
    room.save()
    return Response(status=status.HTTP_200_OK)
    
@api_view(['POST'])
def remove_user(request, room):
    try:
        room = Room.objects.get(room_code=room)
    except ObjectDoesNotExist:
        return Response({"message" : "room does not exist"}, status=status.HTTP_404_NOT_FOUND)

    if request.data["user_name"] in room.user_list:
        remove_index = room.user_list.index(request.data["user_name"])
        room.user_list.pop(remove_index)
        room.user_points.pop(remove_index)
        number_of_players = len(room.user_list)
        if (number_of_players == 0):
            room.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        else:
            room.user_count = number_of_players
            room.save()
        return Response(status=status.HTTP_200_OK)
    else: 
        return Response(status=status.HTTP_404_NOT_FOUND)

@api_view(['GET'])
def get_state(request, room):
    try:
        room = Room.objects.get(room_code=room)
    except ObjectDoesNotExist:
        return Response({"message" : "room does not exist"}, status=status.HTTP_404_NOT_FOUND)

    return Response({"state" : room.state}, status=status.HTTP_200_OK)

@api_view(['POST'])
def set_state(request, room):
    try:
        room = Room.objects.get(room_code=room)
    except ObjectDoesNotExist:
        return Response({"message" : "room does not exist"}, status=status.HTTP_404_NOT_FOUND)

    state = request.data["state"]
    #A = answering
    #V = voting
    #R = results
    #W = waiting
    #D = destroying
    if (state == "A" or state == "V" or state == "W" or state == "D" or state == "R"):
        room.state = state
        print(state)
        room.save()
        return Response(status=status.HTTP_200_OK)
    return Response(status=status.HTTP_400_BAD_REQUEST)


@api_view(['POST'])
def submit_answer(request, room):
    try:
        room = Room.objects.get(room_code=room)
    except ObjectDoesNotExist:
        return Response({"message" : "room does not exist"}, status=status.HTTP_404_NOT_FOUND)
    
    if request.data["user_name"] not in room.user_list:
        return Response({"Message" : "you are not a player in this game"}, status=status.HTTP_404_NOT_FOUND)
    
    print(request.data["user_name"] + ',' + request.data["answer"])
    room.answers.append(request.data["user_name"] + ',' + request.data["answer"])

    if (len(room.answers) == room.user_count):
        room.state = "V"
    room.save()
    return Response(status=status.HTTP_200_OK)

@api_view(['GET'])
def get_answers(request, room):
    try:
        room = Room.objects.get(room_code=room)
    except ObjectDoesNotExist:
        return Response({"message" : "room does not exist"}, status=status.HTTP_404_NOT_FOUND)
    
    answer_list = []
    for answer in room.answers:
        info = answer.split(',',2)
        user_answer_object = {"user_name" : info[0], "answer" : info[1]}
        answer_list.append(user_answer_object)

    return Response(answer_list, status=status.HTTP_200_OK)

@api_view(['POST'])
def set_wrong_user(request, room):
    
    try:
        room = Room.objects.get(room_code=room)
    except ObjectDoesNotExist:
        return Response({"message" : "room does not exist"}, status=status.HTTP_404_NOT_FOUND)
    user_count = room.user_count
    user_wrong_index = random.randint(0, user_count - 1)
    user_wrong_index = random.randint(0, user_count - 1)
    user_wrong_index = random.randint(0, user_count - 1)
    user_wrong_index = random.randint(0, user_count - 1)
    user_wrong_index = random.randint(0, user_count - 1)
    user_wrong_index = random.randint(0, user_count - 1)
    user_wrong = room.user_list[user_wrong_index]
    room.user_wrong = user_wrong
    room.save()
    return Response ({"user_name": user_wrong},status=status.HTTP_200_OK)


def set_wrong_user_helper(room):
    
    user_count = room.user_count
    user_wrong_index = random.randint(0, user_count - 1)
    user_wrong = room.user_list[user_wrong_index]
    room.user_wrong = user_wrong
    room.save()


@api_view(['GET'])
def get_wrong_user(request, room):
    try:
        room = Room.objects.get(room_code=room)
    except ObjectDoesNotExist:
        return Response({"message" : "room does not exist"}, status=status.HTTP_404_NOT_FOUND)

    return Response ({"user_name": room.user_wrong},status=status.HTTP_200_OK)

@api_view(['POST'])
def set_new_question(request, room):
    try:
        room = Room.objects.get(room_code=room)
    except ObjectDoesNotExist:
        return Response({"message" : "room does not exist"}, status=status.HTTP_404_NOT_FOUND)
    
    if (len(room.question_index_array) == 1):
        room.state = "V"
        room.question_index_array.pop(0)
    else:
        room_object = room
        if (room.question_id != 0):
            room.question_index_array.pop(0)
        room.question_id = room.question_index_array[0]
    room.save()
    return Response ({"question": room.question_id},status=status.HTTP_200_OK)

@api_view(['POST'])
def clear_room(request, room):
    
    try:
        room_obj = Room.objects.get(room_code=room)
    except ObjectDoesNotExist:
        return Response({"message" : "room does not exist"}, status=status.HTTP_404_NOT_FOUND)

    room_obj.vote_count = 0
    room_obj.vote_wrong = 0
    room_obj.state = "W"
    room_obj.voted_array.clear()
    #for i in range(0, len(room.user_points)):
        #room.user_points[i] = 0
    room_obj.answers.clear()
    room_obj.caught = False
    room_obj.winner_determined = False
    room_obj.save()
    set_wrong_user_helper(room_obj)
    return Response ({"user_name": room_obj.user_wrong}, status=status.HTTP_200_OK)

@api_view(['POST'])
def set_time(request, room):
    try:
        room = Room.objects.get(room_code=room)
    except ObjectDoesNotExist:
        return Response({"message" : "room does not exist"}, status=status.HTTP_404_NOT_FOUND)
    room.time = request.data["time"]
    room.save()
    return Response (status=status.HTTP_200_OK)

@api_view(['POST'])
def vote(request, room):
    try:
        room = Room.objects.get(room_code=room)
    except ObjectDoesNotExist:
        return Response({"message" : "room does not exist"}, status=status.HTTP_404_NOT_FOUND)

    voter = request.data["user_name"]
    user_selected = request.data["user_selected"]

    if voter not in room.user_list:
        return Response({"message" : "you are not in this game"}, status=status.HTTP_400_BAD_REQUEST)

    if user_selected not in room.user_list:
        return Response({"message" : "this user does not exist"}, status=status.HTTP_400_BAD_REQUEST)

    if voter == room.user_wrong:
        return Response({"message" : "you may not vote in this game"}, status=status.HTTP_200_OK)

    if voter == user_selected:
        return Response({"message" : "you cannot vote for yourself"}, status=status.HTTP_200_OK)

    #Check if user is in the room
    for idx,answer in enumerate(room.voted_array):
        info = answer.split(',',2)
        if info[0] == voter:
            room.voted_array.pop(idx)
            break

    if request.data["locked"]:
        room.vote_count += 1

    room.voted_array.append(voter + ',' + user_selected)

    if (len(room.user_list) - 1 == room.vote_count):
        room.state = "R"
    room.save()
    return Response (status=status.HTTP_200_OK)

@api_view(['POST'])
def determine_winner(request, room):
    try:
        room = Room.objects.get(room_code=room)
    except ObjectDoesNotExist:
        return Response({"message" : "room does not exist"}, status=status.HTTP_404_NOT_FOUND)

    if room.winner_determined == True:
        if room.caught:
            return Response ({"result" : "caught"}, status=status.HTTP_200_OK)
        else:
            return Response ({"result" : "escaped"}, status=status.HTTP_200_OK)

    room.vote_wrong = 0
    for i in range (0, len(room.voted_array)):
        info = room.voted_array[i].split(',',2)
        if info[1] == room.user_wrong:
            user_index = room.user_list.index(info[0]) 
            room.user_points[user_index] += VOTE_RIGHT_POINTS
            room.vote_wrong += 1
    
    room.winner_determined = True
    #room.save()
    if (room.vote_wrong/len(room.user_list) >= 0.5):
        room.caught = True
        room.save()
        return Response ({"result" : "caught"}, status=status.HTTP_200_OK)
    else:
        #might break everything
        room.caught = False
        wrong_user_index = room.user_list.index(room.user_wrong)
        room.user_points[wrong_user_index] += ESCAPE_POINTS
        room.save()
        return Response ({"result" : "escaped"}, status=status.HTTP_200_OK)

@api_view(['GET'])
def vote_results(request, room):
    try:
        room = Room.objects.get(room_code=room)
    except ObjectDoesNotExist:
        return Response({"message" : "room does not exist"}, status=status.HTTP_404_NOT_FOUND)
    
    
    result_list = []
    for vote in room.voted_array:
        info = vote.split(',',2)
        user_answer_object = {"user_name" : info[0], "user_selected" : info[1]}
        result_list.append(user_answer_object)

    return Response(result_list, status=status.HTTP_200_OK)

@api_view(['GET'])
def is_winner_determined(request, room):
    try:
        room = Room.objects.get(room_code=room)
    except ObjectDoesNotExist:
        return Response({"message" : "room does not exist"}, status=status.HTTP_404_NOT_FOUND)

    return Response({"winner_determined" : room.winner_determined}, status=status.HTTP_200_OK)

    
@api_view(['POST'])
def user_votes(request, room):
    try:
        room = Room.objects.get(room_code=room)
    except ObjectDoesNotExist:
        return Response({"message" : "room does not exist"}, status=status.HTTP_404_NOT_FOUND) 


    user = request.data["user_name"]

    if user not in room.user_list:
        return Response({"message" : "user not in this game"}, status=status.HTTP_400_BAD_REQUEST)

    
    votes_for_user = 0
    for vote in room.voted_array:
        info = vote.split(',',2)
        if info[1] == user:
            votes_for_user += 1

    return Response({"votes" : votes_for_user}, status=status.HTTP_200_OK)