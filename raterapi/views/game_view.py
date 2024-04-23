from django.http import HttpResponseServerError
from rest_framework import serializers, status
from rest_framework.response import Response
from rest_framework.viewsets import ViewSet
from django.contrib.auth.models import User
from raterapi.models import Game, Category, Review


class GameView(ViewSet):
    """Game view set"""

    def create(self, request):
        """Handle POST operations

        Returns:
            Response -- JSON serialized instance
        """
        user = request.auth.user

        categories = []
        for category_id in request.data["categories"]:
            category = Category.objects.get(pk=category_id)
            categories.append(category)

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
            game.categories.set(categories)
            serializer = GameSerializer(game)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        except Exception as ex:
            return Response(
                {"Stupid mortal, malformed object dummy.": ex.args[0]},
                status=status.HTTP_400_BAD_REQUEST,
            )

    def retrieve(self, request, pk=None):
        """Handle GET requests for single item

        Returns:
            Response -- JSON serialized instance
        """
        try:
            # game = Game.objects.get(pk=pk)
            # serializer = GameSerializer(game)
            # return Response(serializer.data)
            game = Game.objects.get(pk=pk)
            game_serializer = GameSerializer(game)
            reviews = Review.objects.filter(game_id=pk)
            review_serializer = GameReviewSerializer(reviews, many=True)
            game_data = game_serializer.data
            game_data["reviews"] = review_serializer.data
            return Response(game_data)

        except Exception as ex:
            return Response({"reason": ex.args[0]}, status=status.HTTP_400_BAD_REQUEST)

    def update(self, request, pk=None):
        """Handle PUT requests

        Returns:
            Response -- Empty body with 204 status code
        """
        try:
            user = request.auth.user

            categories = []
            for category_id in request.data["categories"]:
                category = Category.objects.get(pk=category_id)
                categories.append(category)

            game = Game.objects.get(pk=pk)
            game.title = request.data["title"]
            game.description = request.data["description"]
            game.designer = request.data["designer"]
            game.year_released = request.data["yearReleased"]
            game.number_of_players = request.data["numberOfPlayers"]
            game.estimated_time_to_play = request.data["estimatedTimeToPlay"]
            game.age_recommendation = request.data["ageRecommendation"]
            game.user = user
            game.image_url = request.data["imageUrl"]
            game.save()
            game.categories.set(categories)
        except Game.DoesNotExist:
            return Response(None, status=status.HTTP_404_NOT_FOUND)

        except Exception as ex:
            return HttpResponseServerError(ex)

        return Response(None, status=status.HTTP_204_NO_CONTENT)

    def destroy(self, request, pk=None):
        """Handle DELETE requests for a single item

        Returns:
            Response -- 200, 404, or 500 status code
        """
        try:
            game = Game.objects.get(pk=pk)
            game.delete()
            return Response(None, status=status.HTTP_204_NO_CONTENT)

        except Game.DoesNotExist as ex:
            return Response({"message": ex.args[0]}, status=status.HTTP_404_NOT_FOUND)

        except Exception as ex:
            return Response(
                {"message": ex.args[0]}, status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )

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

    firstName = serializers.CharField(source="first_name")
    lastName = serializers.CharField(source="last_name")

    class Meta:
        model = User
        fields = (
            "id",
            "firstName",
            "lastName",
            "username",
        )


class GameCategorySerializer(serializers.ModelSerializer):
    """JSON Serializer"""

    class Meta:
        model = Category
        fields = (
            "id",
            "label",
        )


class GameReviewSerializer(serializers.ModelSerializer):
    """JSON Serializer"""

    user = UserGameSerializer(many=False)

    class Meta:
        model = Review
        fields = (
            "id",
            "user",
            "game",
            "text",
        )


class GameSerializer(serializers.ModelSerializer):
    """JSON Serializer"""

    user = UserGameSerializer(many=False)
    categories = GameCategorySerializer(many=True)
    reviews = GameReviewSerializer(many=True)

    yearReleased = serializers.DateField(source="year_released")
    numberOfPlayers = serializers.IntegerField(source="number_of_players")
    estimatedTimeToPlay = serializers.CharField(source="estimated_time_to_play")
    ageRecommendation = serializers.IntegerField(source="age_recommendation")
    imageUrl = serializers.CharField(source="image_url")

    class Meta:
        model = Game
        fields = (
            "id",
            "title",
            "description",
            "designer",
            "yearReleased",
            "numberOfPlayers",
            "estimatedTimeToPlay",
            "ageRecommendation",
            "user",
            "imageUrl",
            "categories",
            "reviews",
        )
