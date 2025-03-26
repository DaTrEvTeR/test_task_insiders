import json
import pandas as pd
from django.db import models
from django.core.cache import cache
from django_filters.rest_framework import DjangoFilterBackend
from django.http import JsonResponse, HttpResponse
from django.contrib.auth.mixins import LoginRequiredMixin
from rest_framework import viewsets, permissions, filters
from rest_framework.decorators import action
from rest_framework.response import Response
from .models import Location, Review, Like
from .serializers import LocationSerializer, ReviewSerializer, LikeSerializer

CACHE_TIMEOUT = 900


class LocationViewSet(LoginRequiredMixin, viewsets.ModelViewSet):
    queryset = Location.objects.annotate(
        likes_count=models.Count("likes", filter=models.Q(likes__is_like=True)),
        dislikes_count=models.Count("likes", filter=models.Q(likes__is_like=False)),
    ).order_by("-likes_count", "dislikes_count")
    serializer_class = LocationSerializer
    filter_backends = [DjangoFilterBackend, filters.SearchFilter]
    filterset_fields = ["reviews__comment", "likes__is_like"]
    search_fields = ["name", "address"]

    def list(self, request, *args, **kwargs):
        if request.query_params:
            return super().list(request, *args, **kwargs)

        cache_key = "locations_list"
        cached_data = cache.get(cache_key)

        if cached_data:
            return Response(json.loads(cached_data))
        response = super().list(request, *args, **kwargs)
        cache.set(cache_key, json.dumps(response.data), CACHE_TIMEOUT)
        return response

    def retrieve(self, request, *args, **kwargs):
        cache_key = f"location_{kwargs['pk']}"
        cached_data = cache.get(cache_key)

        if cached_data:
            return Response(json.loads(cached_data))

        response = super().retrieve(request, *args, **kwargs)
        cache.set(cache_key, json.dumps(response.data), CACHE_TIMEOUT)
        return response

    def perform_create(self, serializer):
        serializer.save()
        cache.delete("locations_list")

    def perform_update(self, serializer):
        location = serializer.save()
        cache.delete("locations_list")
        cache.delete(f"location_{location.pk}")

    def perform_destroy(self, instance):
        cache.delete("locations_list")
        cache.delete(f"location_{instance.pk}")
        instance.delete()

    @action(detail=False, methods=["get"])
    def export(self, request):
        """Експорт локацій у JSON або CSV"""
        format_type = request.GET.get("format", "csv")

        locations = Location.objects.values("id", "name", "address")

        if format_type == "json":
            return JsonResponse(list(locations), safe=False, json_dumps_params={"indent": 2})

        df = pd.DataFrame.from_records(locations)
        csv_data = df.to_csv(index=False, encoding="utf-8-sig")

        response = HttpResponse(csv_data, content_type="text/csv")
        response["Content-Disposition"] = 'attachment; filename="locations.csv"'
        return response


class ReviewViewSet(LoginRequiredMixin, viewsets.ModelViewSet):
    queryset = Review.objects.all()
    serializer_class = ReviewSerializer

    def get_queryset(self):
        location_id = self.kwargs["location_pk"]
        cache_key = f"location_{location_id}_reviews"
        cached_data = cache.get(cache_key)

        if cached_data:
            return Review.objects.filter(location_id=location_id)

        queryset = Review.objects.filter(location_id=location_id)
        cache.set(cache_key, list(queryset.values()), CACHE_TIMEOUT)
        return queryset

    def perform_create(self, serializer):
        review = serializer.save(user=self.request.user, location_id=self.kwargs["location_pk"])
        cache.delete(f"location_{review.location.pk}")
        cache.delete(f"location_{review.location.pk}_reviews")
        cache.delete("locations_list")

    def perform_destroy(self, instance):
        cache.delete(f"location_{instance.location.pk}")
        cache.delete(f"location_{instance.location.pk}_reviews")
        cache.delete("locations_list")
        instance.delete()


class LikeViewSet(LoginRequiredMixin, viewsets.ModelViewSet):
    queryset = Like.objects.all()
    serializer_class = LikeSerializer

    def get_queryset(self):
        location_id = self.kwargs["location_pk"]
        cache_key = f"location_{location_id}_likes"
        cached_data = cache.get(cache_key)

        if cached_data:
            return Like.objects.filter(location_id=location_id)

        queryset = Like.objects.filter(location_id=location_id)
        cache.set(cache_key, list(queryset.values()), CACHE_TIMEOUT)
        return queryset

    def perform_create(self, serializer):
        like = serializer.save(user=self.request.user, location_id=self.kwargs["location_pk"])
        cache.delete(f"location_{like.location.pk}")
        cache.delete(f"location_{like.location.pk}_likes")
        cache.delete("locations_list")

    def perform_destroy(self, instance):
        cache.delete(f"location_{instance.location.pk}")
        cache.delete(f"location_{instance.location.pk}_likes")
        cache.delete("locations_list")
        instance.delete()
