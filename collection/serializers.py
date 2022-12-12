from collections import OrderedDict

from rest_framework import serializers

from .models import Collection, Movie


class MovieSerializer(serializers.ModelSerializer):
    class Meta:
        model = Movie
        fields = '__all__'
        extra_kwargs = {
            'uuid': {
                'validators': []
            }
        }


class CollectionListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Collection
        fields = ['title', 'uuid', 'description']


class CreateCollectionSerializer(serializers.ModelSerializer):
    movies = MovieSerializer(many=True)

    class Meta:
        model = Collection
        fields = ['uuid', 'title', 'description', 'movies']
        depth = 1

    def create(self, validated_data):
        # Create Collection and then create all related movies separately
        # and add those to the collection
        movies_data = validated_data.pop('movies')
        collection = Collection.objects.create(**validated_data)

        for movie_data in movies_data:
            try:
                movie = Movie.objects.get(uuid=movie_data.get('uuid'))
            except Movie.DoesNotExist:
                movie = Movie.objects.create(**movie_data)
            collection.movies.add(movie)

        return collection

    def to_representation(self, instance):
        # Update the response and pass only collection_uuid
        response = super().to_representation(instance)
        updated_response = OrderedDict()
        updated_response['collection_uuid'] = response['uuid']

        return updated_response


class CollectionSerializer(serializers.ModelSerializer):
    movies = MovieSerializer(many=True)

    class Meta:
        model = Collection
        fields = ['title', 'description', 'movies']
        depth = 1

    def update(self, instance, validated_data):
        # Update Collection and then create all related movies separately
        # and add those to the collection
        movies_data = validated_data.pop('movies')

        instance.title = validated_data.get('title', instance.title)
        instance.description = validated_data.get('description', instance.description)
        instance.save()

        for movie_data in movies_data:
            try:
                movie = Movie.objects.get(uuid=movie_data.get('uuid'))
            except Movie.DoesNotExist:
                movie = Movie.objects.create(**movie_data)
            instance.movies.add(movie)

        return instance
