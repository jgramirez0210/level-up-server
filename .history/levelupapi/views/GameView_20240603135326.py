from django.http import HttpResponseServerError
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import serializers, status
from levelupapi.models import Game, Gamer, Game_Type


class GameView(ViewSet):
    """Level up game types view"""

    def retrieve(self, request, pk):
        """Handle GET requests for single game type

        Returns:
            Response -- JSON serialized game type
        """
        game = Game.objects.get(pk=pk)
        serializer = GameSerializer(game)
        return Response(serializer.data)

    def list(self, request):
        """Handle GET requests to get all game types

        Returns:
            Response -- JSON serialized list of game types
        """
        games = Game.objects.all()
        game_type = request.query_params.get("type", None)
        if game_type is not None:
            games = games.filter(game_type__id=game_type)
        serializer = GameSerializer(games, many=True)
        return Response(serializer.data)
        
    def create(self, request):
        gamer = Gamer.objects.get(uid=request.data["userId"])
        game_type = Game_Type.objects.get(pk=request.data["game_type"])   

        game = Game.objects.create(
            title=request.data["title"],
            maker=request.data["maker"],
            number_of_players=request.data["number_of_players"],
            skill_level=request.data["skill_level"],
            game_type=game_type,
            gamer=gamer,
        )
        serializer = GameSerializer(game)
        return Response(serializer.data)
     
    def update(self, request, pk):
        game = Game.objects.get(pk=pk)
        game.title = request.data["title"]
        game.maker = request.data["maker"]
        game.number_of_players = request.data.get("number_of_players")
        game.skill_level = request.data.get("skill_level")

        game_type = GameType.objects.get(pk=request.data.get("game_type"))
        game.game_type = game_type
        game.save()

        return Response(None, status=status.HTTP_204_NO_CONTENT)
    
    def destroy(self, request, pk):
        game = Game.objects.get(pk=pk)
        game.delete()
        return Response(None, status=status.HTTP_204_NO_CONTENT)

class GameSerializer(serializers.ModelSerializer):
    """JSON serializer for game types
    """
    number_of_players = serializers.CharField()
    skill_level = serializers.CharField()

    class Meta:
        model = Game
        fields = ('id', 'game_type', 'title', 'maker', 'number_of_players', 'skill_level')
