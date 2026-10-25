from rest_framework.permissions import BasePermission
from django.shortcuts import get_object_or_404
from tripmater.models import Trip,TripMember

class owneronly(BasePermission):
    def has_object_permission(self, request, view, obj):
        return request.user== obj.created_by

class Memberonly(BasePermission):
    def has_permission(self, request, view):
        trip_id=view.kwargs.get("pk")
        trip_object=get_object_or_404(Trip,id=trip_id)
        return TripMember.objects.filter(member=request.user,trip=trip_object).exists()

    