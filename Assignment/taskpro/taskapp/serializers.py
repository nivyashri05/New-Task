from rest_framework import serializers
from rest_framework.validators import UniqueValidator
from taskapp.models import User, OTP
from taskapp.utils import otpgen,Email


class UserSerializers(serializers.ModelSerializer):
    email = serializers.EmailField(max_length=255, required=True,
                                   validators=[UniqueValidator(queryset=User.objects.all())])
    class Meta:
        model=User
        fields='__all__'

    def create(self, validated_data):
        print(validated_data)
        email = validated_data.pop('email')
        password = validated_data.pop('password')
        username = validated_data.pop('username')
        phone = validated_data.pop('phone')
        user = User.objects.create(email=email,username=username,phone=phone)
        user.set_password(password)
        user.save()
        obj= OTP.objects.create(user_id=user.id,otp=otpgen())
        obj.save()
        Email('otp of your account',obj.otp,user.email)
        return user

    def update(self, instance, validated_data):
        print(validated_data)
        instance.email = validated_data.get('email',instance.email)
        instance.password = validated_data.get('password', instance.password)
        instance.username = validated_data.get('username', instance.username)
        instance.phone = validated_data.get('phone', instance.phone)
        instance.save()
        return instance


class VerifyOtpSerializer(serializers.Serializer):
    email = serializers.EmailField(max_length=255, required=True)
    otp   =serializers.IntegerField(required=True)

class LoginSerializer(serializers.Serializer):
    username = serializers.CharField(max_length=256, required=True)
    password = serializers.CharField(required=True, min_length=5)

    class Meta:
        model = User


class ChangePasswordSerializer(serializers.Serializer):
    email = serializers.EmailField(max_length=256, required=True)
    old_password = serializers.CharField(required=True)
    new_password = serializers.CharField(required=True)

    class Meta:
        model = User

