from django.contrib.auth import authenticate
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView
from rest_framework.response import Response
from .exception import IncorrectData,IncorrectAuthCredentials
from .models import User, OTP
from .serializers import UserSerializers, LoginSerializer, ChangePasswordSerializer, VerifyOtpSerializer
from rest_framework.authtoken.models import Token

class User_API(APIView):
    def get(self,request,*args,**kwargs):
        queryset=User.objects.all()
        serializer=UserSerializers(queryset, many=True)
        return Response(serializer.data)

    def post(self, request, *args, **kwargs):
        print(request.data)
        serializer=UserSerializers(data=request.data)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            return Response(serializer.data,status=status.HTTP_200_OK)
        else:
            return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)


user_api=User_API.as_view()



class User_crud(APIView):
    serializer_class = UserSerializers
    def get_object(self,id):
        try:
            return User.objects.get(id=id)
        except User.DoesNotExist:
            return Response(status=404)

    def get(self,request,id):
        exmp = self.get_object(id)
        serializer=self.serializer_class(exmp)
        return Response(serializer.data)

    def put(self,request,id):
        print(request.data)
        exmp=self.get_object(id)
        serializer=self.serializer_class(exmp,data=request.data)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            return Response(serializer.data)
        else:
            return Response(serializer.errors)


    def delete(self,request,id):
        exmp=self.get_object(id)
        exmp.delete()
        return Response(status=204)

user_crud =User_crud.as_view()

class VerifyOtp(APIView):
    def post(self, request, *args, **kwargs):
        print(request.data)
        serializer = VerifyOtpSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            try:
                user =User.objects.get(email=request.data['email'])
            except:
                return Response({'Error':'email id doesnot exist'}, status=status.HTTP_400_BAD_REQUEST)
            try:
                otp = OTP.objects.get(user_id=user.id)
                if otp.otp ==request.data['otp']:
                    user.is_active=True
                    user.save()
                    return Response(serializer.data, status=status.HTTP_200_OK)

            except:
                return Response({'Error': 'email id doesnot exist'}, status=status.HTTP_400_BAD_REQUEST)


        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
verifyOtp=VerifyOtp.as_view()


class Test(APIView):

    def post(self, request, *args, **kwargs):
        serializer = LoginSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            username = request.data['username']
            password = request.data['password']
            user = authenticate(request,username=username, password=password)

            if user:
                token, created = Token.objects.get_or_create(user=user)
                return Response({'Token':token.key},status=status.HTTP_200_OK)
            else:
                 raise IncorrectAuthCredentials(detail="Incorrect authentication credentials", code=401)
        else:
            raise IncorrectData(detail=serializer.errors, code=400)


loginuser = Test.as_view()


class ChangePwd(APIView):


    def put(self,request):

        serializer=ChangePasswordSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            user = User.objects.get(email=request.data['email'])
            user.set_password(request.data['new_password'])
            user.save()
            return Response({"Status":True}, status=status.HTTP_200_OK)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)



resetpwd=ChangePwd.as_view()
