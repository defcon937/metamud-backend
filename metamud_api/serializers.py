from rest_framework import serializers
from .models import Sword

class SwordSerializer(serializers.ModelSerializer):
    class Meta:
        model = Sword
        fields = ["sword_name", "timestamp", "updated", "user"]
