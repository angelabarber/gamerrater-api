from django.http import HttpResponseServerError
from rest_framework import serializers, status
from rest_framework.response import Response
from rest_framework.viewsets import ViewSet
from django.contrib.auth.models import User
from raterapi.models import Game


class GameView(ViewSet):
    """Game view set"""

    def create(self, request):
        """Handle POST operations

        Returns:
            Response -- JSON serialized instance
        """
        user = request.auth.user

        game = Game()
        game.title = request.data["title"]
        game.description = request.data["description"]
        game.designer = request.data["designer"]
        game.year_released = request.data["yearReleased"]
        game.number_of_players = request.data["numberOfPlayers"]
        game.estimated_time_to_play = request.data["estimatedTimeToPlay"]
        game.age_recommendation = request.data["ageRecommendation"]
        game.user = user
        game.image_url = request.data["imageUrl"]

        try:
            game.save()
            serializer = GameSerializer(game)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        except Exception as ex:
            return Response(
                {"Stupid mortal, malformed object dummy": ex.args[0]},
                status=status.HTTP_400_BAD_REQUEST,
            )

    # def retrieve(self, request, pk=None):
    #     """Handle GET requests for single item

    #     Returns:
    #         Response -- JSON serialized instance
    #     """
    #     try:
    #         void = Void.objects.get(pk=pk)
    #         serializer = VoidSerializer(void)
    #         return Response(serializer.data)
    #     except Exception as ex:
    #         return Response({"reason": ex.args[0]}, status=status.HTTP_400_BAD_REQUEST)

    # def update(self, request, pk=None):
    #     """Handle PUT requests

    #     Returns:
    #         Response -- Empty body with 204 status code
    #     """
    #     try:
    #         void = Void.objects.get(pk=pk)
    #         void.sample_name = request.data["name"]
    #         void.sample_description = request.data["description"]
    #         void.save()
    #     except Void.DoesNotExist:
    #         return Response(None, status=status.HTTP_404_NOT_FOUND)

    #     except Exception as ex:
    #         return HttpResponseServerError(ex)

    #     return Response(None, status=status.HTTP_204_NO_CONTENT)

    # def destroy(self, request, pk=None):
    #     """Handle DELETE requests for a single item

    #     Returns:
    #         Response -- 200, 404, or 500 status code
    #     """
    #     try:
    #         void = Void.objects.get(pk=pk)
    #         void.delete()
    #         return Response(None, status=status.HTTP_204_NO_CONTENT)

    #     except Void.DoesNotExist as ex:
    #         return Response({"message": ex.args[0]}, status=status.HTTP_404_NOT_FOUND)

    #     except Exception as ex:
    #         return Response(
    #             {"message": ex.args[0]}, status=status.HTTP_500_INTERNAL_SERVER_ERROR
    #         )

    def list(self, request):
        """Handle GET requests for all items

        Returns:
            Response -- JSON serialized array
        """
        try:
            games = Game.objects.all()
            serializer = GameSerializer(games, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except Exception as ex:
            return HttpResponseServerError(ex)


class UserGameSerializer(serializers.ModelSerializer):
    """JSON Serializer"""

    class Meta:
        model = User
        fields = (
            "id",
            "first_name",
            "last_name",
            "username",
        )


class GameSerializer(serializers.ModelSerializer):
    """JSON Serializer"""

    user = UserGameSerializer(many=False)

    class Meta:
        model = Game
        fields = (
            "id",
            "title",
            "description",
            "designer",
            "year_released",
            "number_of_players",
            "estimated_time_to_play",
            "age_recommendation",
            "user",
            "image_url",
        )
