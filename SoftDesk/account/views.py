from django.shortcuts import render
from rest_framework.views import APIView
from account.serializers import SignupSerializer
from rest_framework.response import Response


class SignupView(APIView):
    def post(self, request):
        serializer = SignupSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)
