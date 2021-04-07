from rest_framework import serializers
from .models import Profile, Chat, Config, Timer, List, Reward


class ProfileSerializer(serializers.ModelSerializer):

    class Meta:
        model = Profile
        fields = '__all__'


class ChatSerializer(serializers.ModelSerializer):

    class Meta:
        model = Chat
        fields = '__all__'


class ConfigSerializer(serializers.ModelSerializer):

    class Meta:
        model = Config
        fields = '__all__'


class TimerSerializer(serializers.ModelSerializer):

    class Meta:
        model = Timer
        fields = '__all__'


class ListSerializer(serializers.ModelSerializer):

    class Meta:
        model = List
        fields = '__all__'


class RewardSerializer(serializers.ModelSerializer):

    class Meta:
        model = Reward
        fields = '__all__'


