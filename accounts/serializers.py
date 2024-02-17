from rest_framework import serializers
from .models import *


class RegisterSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['name','email','mobile_no','password','role']
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        try:
            user = User(
                            email=validated_data["email"],
                            name=validated_data["name"],
                            mobile_no=validated_data["mobile_no"],
                            role=validated_data["role"]
                        )
        except Exception as e:
            raise serializers.ValidationError({"msg":f'{e} is Required Field'})
            
                
        user.set_password(validated_data["password"])
        user.save()
        return user
    
    def to_internal_value(self, data):
        try:
            return super().to_internal_value(data)
        except serializers.ValidationError as error:
            msg =[]
            for field, messages in error.detail.items():
                if "required" in messages[0].lower():
                    msg.append({'msg': f'{field} is Required'.capitalize().replace('_'," ")})
                else:
                    msg.append({"msg":f"{field} is Invalid"})
            raise serializers.ValidationError(msg[0])

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ["name","mobile_no","email","gst_no","pan_no","pan_card","gst_certificate","role"]
        
    def to_internal_value(self, data):
        try:
            return super().to_internal_value(data)
        except serializers.ValidationError as error:
            msg =[]
            for field, messages in error.detail.items():
                if "required" in messages[0].lower():
                    msg.append({'msg': f'{field} is Required'.capitalize().replace('_'," ")})
                else:
                    msg.append({"msg":f"{field} is Invalid"})
            raise serializers.ValidationError(msg[0])