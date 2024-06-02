from django.http import HttpResponseServerError
from rest_framework.viewsets import viewsets
from rest_framework.response import Response
from rest_framework import serializers
from levelupapi.models import Gamer

class GamerView(ViewSet.ModelViewSet):
    """Level up gamers view"""
    
    def list(self, request):
        """Handle GET requests to get all gamers

        Returns:
            Response -- JSON serialized list of gamers
        """
        gamers = Gamer.objects.all()

        serializer = GamerSerializer(gamers, many=True)
        return Response(serializer.data)

class GamerSerializer(serializers.ModelSerializer):
    """JSON serializer for gamers
    """
    class Meta:
        model = Gamer
        fields = ('id', 'bio')