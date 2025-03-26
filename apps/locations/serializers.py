from rest_framework import serializers
from .models import Location, Review, Like


class ReviewSerializer(serializers.ModelSerializer):
    user = serializers.ReadOnlyField(source="user.username")

    class Meta:
        model = Review
        fields = ["id", "user", "location", "comment", "created_at"]
        extra_kwargs = {"location": {"read_only": True}}

    def validate_comment(self, value):
        if len(value) < 5:
            raise serializers.ValidationError("Comment must be at least 5 characters long.")
        return value


class LikeSerializer(serializers.ModelSerializer):
    user = serializers.ReadOnlyField(source="user.username")

    class Meta:
        model = Like
        fields = ["id", "user", "location", "is_like"]
        extra_kwargs = {"location": {"read_only": True}}

    def validate(self, data):
        user = self.context["request"].user
        location = self.context["view"].kwargs["location_pk"]

        existing_like = Like.objects.filter(user=user, location_id=location).first()
        if existing_like:
            raise serializers.ValidationError("You have already rated this location.")
        return data


class LocationSerializer(serializers.ModelSerializer):
    reviews = ReviewSerializer(many=True, read_only=True)
    likes_count = serializers.SerializerMethodField()
    dislikes_count = serializers.SerializerMethodField()

    class Meta:
        model = Location
        fields = ["id", "name", "address", "reviews", "likes_count", "dislikes_count"]

    def get_likes_count(self, obj):
        return obj.likes.filter(is_like=True).count()

    def get_dislikes_count(self, obj):
        return obj.likes.filter(is_like=False).count()
