from rest_framework.decorators import APIView
from .serializers import UserRegisterSerializer
from rest_framework.response import Response
from rest_framework import status

class RegisterView(APIView):

    def post(self, request):

        seriailizer = UserRegisterSerializer(data=request.data)

        if seriailizer.is_valid():
            seriailizer.save()
            
            return Response({
                "message":"User Registered Successfully"
            },status=status.HTTP_201_CREATED)
        
        return Response(seriailizer.errors , status=status.HTTP_400_BAD_REQUEST)



