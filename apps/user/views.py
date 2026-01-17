from .models import CustomUser, VendorProfile
from rest_framework.exceptions import ValidationError
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.validators import ValidationError

from .serializers import (
    SignUpSerializer,
    SignInSerializer,
    SignOutSerializer,
    VendorProfileSerializer,

    UpdateVendorProfileSerializer,
    UserInfoSerializer,
)


# Create your views here.
class SignUpAPIView(APIView):
    permission_classes = []

    def post(self, request):

        serializer = SignUpSerializer(data=request.data)

        if serializer.is_valid():

            serializer.save()

            return Response({
                "status" : "success",
                "message" : "User registered successfully.",
                "data" : serializer.data
            })
        raise ValidationError(serializer.errors)

class SignInAPIView(APIView):

    permission_classes = []

    def post(self, request):
        
        serializer = SignInSerializer(data=request.data)
        
        if serializer.is_valid():
            return Response({
                "status" : "success",
                "message" : "User signed in successfully.",
                "data" : serializer.data
            })
        raise ValidationError(serializer.errors)


class SignOutAPIView(APIView):
    permission_classes = [IsAuthenticated]
    authentication_classes = [JWTAuthentication]

    def post(self, request):
        serializer = SignOutSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()

            return Response({
                "status" : "success",
                "message" : "Sign Out Successfull"
            })
        
        raise ValidationError(serializer.errors)

    permission_classes = [IsAuthenticated]
    authentication_classes = [JWTAuthentication]

    def post(self, request):
        serializer = ChangePasswordSerializer(data=request.data, context={'request': request})
        if serializer.is_valid():
            serializer.save()
            return Response({
                "status" : "success",
                "message" : "Password changed successfully.",
                "data" : serializer.data
            })
        raise ValidationError(serializer.errors)


   




class UpdateProfileAPIView(APIView):
    permission_classes = [IsAuthenticated]
    authentication_classes = [JWTAuthentication]

    def put(self, request):
        user = request.user

        try:
            userProfile = VendorProfile.objects.select_related('vendor').get(vendor=user)

        except VendorProfile.DoesNotExist:
            return Response({
                "status" : "error",
                "message" : "User profile not found."
            })

        serializer = UpdateVendorProfileSerializer(userProfile, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response({
                "status" : "success",
                "message" : "Profile updated successfully.",
                "data" : serializer.data
            })
        raise ValidationError(serializer.errors)


class MyProfileAPIView(APIView):
    permission_classes = [IsAuthenticated]
    authentication_classes = [JWTAuthentication]

    def get(self, request):
        vendor = request.user

        user_info = CustomUser.objects.prefetch_related('vendor_profile').get(id=vendor.id)
        serializer = UserInfoSerializer(user_info)
        

        return Response({
            "status" : "success",
            "message" : "Profile retrieved successfully.",
            "data" : serializer.data
        })


class CreateVendorProfile(APIView):
    permission_classes = [IsAuthenticated]
    authentication_classes = [JWTAuthentication]

    def post(self, request):
        user = request.user

        business_name = request.data.get('business_name')
        address = request.data.get('address')

        if VendorProfile.objects.filter(vendor = user).exists():
            return Response({
                "status" : "error",
                "message" : "You are already a vendor"
            })

        VendorProfile.objects.create(
            vendor = user,
            business_name = business_name,
            address = address
        )

        user.role = 'vendor'
        user.save()

        return Response({
            "status" : "success",
            "message" : "Vendor Profile create successfull"
        })



class SwitchRoleAPIView(APIView):
    permission_classes = [IsAuthenticated]
    authentication_classes = [JWTAuthentication]

    def post(self, request):

        user = request.user
        role = request.data.get('role')
        
        user.role = role
        user.save()
        return Response({
            "status" : "success",
            "message" : "Role switched successfully.",
        })
        