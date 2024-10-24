from rest_framework import serializers

from appbase.models.user import User

class CreateUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        exclude = ["id", "avatar_url", "last_login", "status"]