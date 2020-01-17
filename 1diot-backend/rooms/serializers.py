from rest_framework import serializers
from .models import Room
from .models import Answer


class AnswerSerialzier(serializers.ModelSerializer):
    class Meta:
      model = Answer
      fields = ('user_name', 'answer')

class RoomSerializer(serializers.ModelSerializer): 
    #answer = AnswerSerialzier(many=True)

    class Meta:
        model = Room
        fields = ('pk', 
                'user_list',
                'host', 
                'room_code', 
                'state', 
                'question_id', 
                'vote_wrong', 
                'user_count', 
                'user_wrong', 
                'time', 
                'answers', 
                'question_index_array', 
                'user_points',
                'voted_array',
                'vote_count',
                'caught',
                'winner_determined')
