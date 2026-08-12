from django.shortcuts import render,get_object_or_404

# Create your views here.
from rest_framework.views import APIView
from tripmater.serializer import userserilizer
from rest_framework.response import Response
from rest_framework import authentication,permissions
from tripmater.models import Trip,TripMember
from tripmater.serializer import TripSerializer,User,TripMember,TripMemberSerilizer
from rest_framework import serializers
from tripmater.permission import owneronly

class SignupView(APIView):
    def post(self,request):
        form_data=request.data
        serializer_instance=userserilizer(data=form_data)
        if serializer_instance.is_valid():
            serializer_instance.save()

            return Response(data=serializer_instance.data)
        else:
            return Response(data=serializer_instance.errors)

class TripListCreateView(APIView):
    authentication_classes=[authentication.BasicAuthentication]#username,password
    permission_classes=[permissions.IsAuthenticated]#verify user

    def get(self,request):
        qs=Trip.objects.filter(created_by=request.user)
        serializer_instance=TripSerializer(qs,many=True)
        return Response(data=serializer_instance.data)

    def post(self,request):
        form_data=request.data
        serializer_instance=TripSerializer(data=form_data)
        if serializer_instance.is_valid():
            trip=serializer_instance.save(created_by=request.user)
            # TripMember.objects.create(trip=trip,member=request.user,role="OWNER")
            return Response(data=serializer_instance.data)
        else:
            return Response()

class TripRetriveUpdateDeleteView(APIView):

    authentication_classes=[authentication.BasicAuthentication]
    permission_classes=[owneronly]

    def get(self,request,pk):
        trip_object=get_object_or_404(Trip,id=pk)
        self.check_object_permissions(request,trip_object)

        serializer_instance=TripSerializer(trip_object)
        return Response(data=serializer_instance.data)
       
    

    def put(self,request,pk):
        
        trip_object=get_object_or_404(Trip,id=pk)
        self.check_object_permissions(request,trip_object)
        form_data=request.data

        serializer_instance=TripSerializer(data=form_data,instance=trip_object)
        if serializer_instance.is_valid():
            serializer_instance.save()
            return Response(data=serializer_instance.data)
        else:
            return Response(data=serializer_instance.errors)

    def delete(self,request,pk):
        trip_object=get_object_or_404(Trip,id=pk)
        self.check_object_permissions(request,trip_object)
        trip_object.delete()
        return Response(data={"message":"deleted"})    


class AddMemberview(APIView):
    def post(self,request,pk):
        trip_id=pk
        form_data=request.data
        trip_object=get_object_or_404(Trip,id=trip_id)
        member_object=get_object_or_404(User,id=form_data.get("member"))
        if trip_object.created_by!=request.user:
            raise serializers.ValidationError("you donot have the permission")
        if TripMember.objects.filter(trip=trip_object,member=member_object).exists():
            raise serializers.ValidationError("already a member")
        
        serializer_instance=TripMemberSerilizer(data=form_data)
        if serializer_instance.is_valid():
            serializer_instance.save(trip=trip_object)
            return Response(data=serializer_instance.data)
        else:
            return Response(data=serializer_instance.errors)


        # trip_id=pk
        # user_id=request.data.get("member")

        # trip_object= get_object_or_404(Trip,id=trip_id)
        # user_object= get_object_or_404(User,id=user_id)

        # TripMember.objects.create(trip=trip_object,member=user_object)

        # return Response(data={"message":"member added..."})
          
    
           


            
    

    

   

        