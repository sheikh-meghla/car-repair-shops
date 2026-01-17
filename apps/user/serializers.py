from rest_framework import  serializers
from django.core.exceptions import ValidationError
from django.contrib.auth.password_validation import validate_password
from rest_framework_simplejwt.tokens import RefreshToken
from apps.user.models import CustomUser, VendorProfile

class SignUpSerializer(serializers.ModelSerializer):
    email = serializers.EmailField()
    password = serializers.CharField(write_only=True)
    business_name = serializers.CharField(write_only=True, required=False)
    address = serializers.CharField(write_only=True, required=False)

    def validate(self, attrs):
        email = attrs.get('email')

        if CustomUser.objects.filter(email=email).exists():

            raise serializers.ValidationError({'email': 'User with this email already exists.'})
        
        return attrs

    class Meta:
        model = CustomUser
        fields = ['email', 'password', 'role', 'business_name', 'address']

    def create(self, validated_data):
        email = validated_data.pop('email')
        password = validated_data.pop('password')
        role = validated_data.pop('role')
        
        business_name = validated_data.pop('business_name', None)
        address = validated_data.pop('address', None)
        
        user = CustomUser.objects.create_user(email=email, password=password, role=role, **validated_data)

        if role == 'vendor':
            if business_name and address:
                VendorProfile.objects.create(
                    vendor=user,
                    business_name = business_name,
                    address = address
                )

        return user
    
    def to_representation(self, instance):
        return {
            'id': instance.id,
            'email': instance.email,
            'role': instance.role,
        }


class SignInSerializer(serializers.Serializer):

    email = serializers.EmailField()
    password = serializers.CharField(write_only=True)
    refresh_token = serializers.CharField(read_only=True)
    access_token = serializers.CharField(read_only=True)

    def validate(self, attrs):
        password = attrs.get('password')
        user = CustomUser.objects.filter(email=attrs['email']).first()
        if not user:
           raise serializers.ValidationError({'email': 'User with this email does not exist.'})
        if not user.check_password(password):
            raise serializers.ValidationError({'password': 'Invalid password.'})
        self.user = user
        return attrs

    def to_representation(self, instance):
        user = self.user
        refresh = RefreshToken.for_user(user)
        return {
            'id': user.id,
            'email': user.email,
            'role': user.role,
            'refresh_token': str(refresh),
            'access_token': str(refresh.access_token)
        }

class SignOutSerializer(serializers.Serializer):
    refresh_token = serializers.CharField(write_only=True)

    def validate(self, attrs):
        self.refresh_token = attrs.get('refresh_token')
        return attrs
    
    def save(self, **kwargs):
        try:
            token = RefreshToken(self.refresh_token)
            token.blacklist()
        except Exception as e:
            return ValidationError({'error': str(e)})



class CustomUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ['id','email','role']

class VendorProfileSerializer(serializers.ModelSerializer):
    vendor = CustomUserSerializer()
    class Meta:
        model = VendorProfile
        fields = ['vendor','business_name', 'address', 'is_active']



class UpdateVendorProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = VendorProfile
        fields = '__all__'
        read_only_fields = ['vendor']


class UserInfoSerializer(serializers.ModelSerializer):
    vendor_profile = VendorProfileSerializer()
    class Meta:
        model = CustomUser
        fields = ['id','email','role','vendor_profile']


