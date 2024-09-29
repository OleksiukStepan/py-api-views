from rest_framework import serializers

from cinema.models import (
    Movie,
    Actor,
    Genre,
    CinemaHall
)


class MovieSerializer(serializers.Serializer):
    id = serializers.IntegerField(read_only=True)
    title = serializers.CharField(max_length=255)
    description = serializers.CharField()
    duration = serializers.IntegerField()
    actors = serializers.PrimaryKeyRelatedField(
        queryset=Actor.objects.all(),
        many=True,
    )
    genres = serializers.PrimaryKeyRelatedField(
        queryset=Genre.objects.all(),
        many=True,
    )

    def create(self, validated_data: dict) -> Movie:
        actors = validated_data.pop("actors", [])
        genres = validated_data.pop("genres", [])
        movie = Movie.objects.create(**validated_data)
        movie.actors.set(actors)
        movie.genres.set(genres)
        return movie

    def update(self, instance: Movie, validated_data: dict) -> Movie:
        instance.title = validated_data.get("title", instance.title)
        instance.description = validated_data.get(
            "description", instance.description
        )
        instance.duration = validated_data.get("duration", instance.duration)
        actors = validated_data.get("actors", None)
        genres = validated_data.get("genres", None)

        if actors:
            instance.actors.set(actors)

        if genres:
            instance.genres.set(genres)

        instance.save()

        return instance


class ActorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Actor
        fields = ["first_name", "last_name"]


class GenreSerializer(serializers.ModelSerializer):
    class Meta:
        model = Genre
        fields = ["name"]


class CinemaHallSerializer(serializers.ModelSerializer):
    class Meta:
        model = CinemaHall
        fields = ["name", "rows", "seats_in_row"]
