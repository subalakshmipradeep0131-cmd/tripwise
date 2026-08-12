from rest_framework import serializers
from django.contrib.auth.models import User
from tripmater.models import Trip,TripMember

class userserilizer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = ["username","email","password"]

    def create(self, validated_data):
        return User.objects.create_user(**validated_data) 

class TripMemberSerilizer(serializers.ModelSerializer):

    class Meta:
        model =  TripMember
        fields = "__all__"
        read_only_fields=["id","trip","role","joined_at"] 

class TripSerializer(serializers.ModelSerializer):

    created_by=serializers.StringRelatedField(read_only=True)
    member_count=serializers.SerializerMethodField(read_only=True)
    trip_member=serializers.SerializerMethodField(read_only=True)

    class Meta:

        model = Trip
        fields = "__all__"
        read_only_fields = ["id","created_by","created_at","updated_at"]

    def get_member_count(self,trip_obj):
        return TripMember.objects.filter(trip=trip_obj).count() 

    def get_trip_member(self,obj):
        members=TripMember.objects.filter(trip=obj)
        serializer_instance=TripMemberSerilizer(members,many=True)
        return serializer_instance.data


    from django.db.models.signals import post_save
    from django.dispatch import receiver

    @receiver(post_save,sender=Trip) 
    def add_trip_owner(sender,instance,created,**kwargs):
        if created :
             TripMember.objects.create(trip=instance,member=instance.created_by,role="OWNER")


   
              
     
        