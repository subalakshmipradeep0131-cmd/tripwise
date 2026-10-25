from rest_framework import serializers
from django.contrib.auth.models import User
from tripmater.models import Trip,TripMember,Expense
from django.db.models import Sum

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
    total=serializers.SerializerMethodField(read_only=True)
    member_total=serializers.SerializerMethodField(read_only=True)

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

    def get_total(self,obj):
        total=Expense.objects.filter(trip=obj).values("amount").aggregate(total=Sum("amount")).get("total")
        return total

    def get_member_total(self,obj):
        trip_member_object=TripMember.objects.filter(trip=obj)
        result=[]

        for t_m_o in trip_member_object:
            member=t_m_o.member
            total=Expense.objects.filter(trip=obj,paid_by=member).values("amount").aggregate(total=Sum("amount")).get("total")
            result.append({"member":member.username,"total":total})
        return result    


class ExpenseSerializer(serializers.ModelSerializer):

    class Meta:

        model= Expense
        fields= "__all__"
        read_only_fields = ["id","created_at","updated_at","paid_by","trip"]
          





   
              
     
        