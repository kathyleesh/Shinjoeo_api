from .models import NewWord
from rest_framework import serializers

class NewWordSerializer(serializers.ModelSerializer):
    class Meta:
        model=NewWord
        fields= '__all__'
    