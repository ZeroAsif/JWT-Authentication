from rest_framework.response import Response
from rest_framework import status
from rest_framework.views import APIView
from account.serializers import  UserRegistrationSerializer,UserLoginSerializer,UserProfileSerializer,UserChangePassword,PasswordResetViewSerializer,UserPassworResetSerializer
from django.contrib.auth import authenticate
from account.renderers import UserRender
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.permissions import IsAuthenticated


def get_tokens_for_user(user):
    refresh = RefreshToken.for_user(user)

    return {
        'refresh': str(refresh),
        'access': str(refresh.access_token),
    }




class UserRegistrationView(APIView):
    renderer_classes = [UserRender]
    def post(self,request,format=None):
        serializer = UserRegistrationSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            user = serializer.save()
            token = get_tokens_for_user(user)
            return Response({ 'token':token,'msg':'Registration Success'},
            status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP__BAD_REQUEST )



class UserLoginView(APIView):
    renderer_classes = [UserRender]
    def post(self,request,format=None):
        serializer = UserLoginSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            email = serializer.data.get('email')
            password = serializer.data.get('password')
            user = authenticate (email=email, password=password)
            if user is not None:
                token = get_tokens_for_user(user)
                return Response({'token':token,'msg':'Login Success'},
                status=status.HTTP_200_OK)

            else:
                return Response({'errors':{'non_fields_errors':['Emial or Password os not valid']}},
                status=status.HTTP_404_USER_NOT_FOUND)
        return Response(serializer.errors,
            status=status.HTTP_400_BAD_REQUEST)
                
        
class UserProfileView(APIView):
    renderer_classes = [UserRender]
    Permission_classes = [IsAuthenticated]
    def get (self,request, format=None):
        serializer = UserProfileSerializer(request.user)
        return Response(serializer.data, status=status.HTTP_200_OK)
     


class UserChangePasswordView(APIView):
    renderer_classes = [UserRender]
    Permission_classes = [IsAuthenticated]
    def post (self,request, format=None):
        serializer = UserChangePassword(data=request.data, context={'user':request.user})
        if serializer.is_valid(raise_exception=True):
            return Response({'msg':'Password Change Successfully'},
            status=status.HTTP_201_CREATED)
        return Response(serializer.errors,
            status=status.HTTP_400_BAD_REQUEST)

class PasswordResetView(APIView):
    renderer_classes = [UserRender]
    def post(self, request, fomat=None):
        serializer= PasswordResetViewSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            return Response({'msg':'Password Reset link send. Please Check your Email'},
            status=status.HTTP_200_OK)
        return Response(serializer.errors,
        status=status.HTTP_400_BAD_REQUEST)


class UserPasswordResetView(APIView):
    renderer_classes = [UserRender]
    def post(self, request,uid,token, fomat=None):
        serializer = UserPassworResetSerializer(data=request.data,context={'uid':uid, 'token':token})
        if serializer.is_valid(raise_exception=True):
            return Response({'msg':'Password Reset Successfully'},
            status=status.HTTP_200_OK)
        return Response(serializer.errors,
        status=status.HTTP_400_BAD_REQUEST)   




 