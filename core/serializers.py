from rest_framework import serializers
from core.models import User, Semester, Card


class UserSimpleGuestSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'username', 'realname')


class UserSimpleSerializer(UserSimpleGuestSerializer):
    pass


class UserExtendedSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'username', 'realname', 'email', 'is_superuser', 'is_staff', 'is_active', 'date_joined',
                  'groups', 'user_permissions', 'phone_number',)
        depth = 1


class SemesterSerializer(serializers.ModelSerializer):
    class Meta:
        model = Semester
        fields = ('id', 'year', 'semester')


class CardSerializer(serializers.ModelSerializer):
    user = UserSimpleSerializer()

    class Meta:
        model = Card
        fields = ('id', 'user', 'card_number', 'card_uid', 'disabled', 'comment')


class CardCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Card
        fields = ('user', 'card_number', 'card_uid', 'comment')
        extra_kwargs = {'comment': {'default': None}}
