from rest_framework import serializers
from .models import CustomUser, UserProfile, Company
from rest_framework_simplejwt.tokens import RefreshToken, TokenError


class UserProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserProfile
        fields = [
            'managerFirstName', 
            'managerMiddleName', 
            'managerLastName', 
            'managerCountry', 
            'managerRegion', 
            'managerZone', 
            'managerWoreda', 
            'managerKebele', 
            'managerPhoneNumber', 
            'userRole',
            'managerRenewedIDFront',
            'managerRenewedIDBack',
            'profilePic'
        ]


class UserCompanySerializer(serializers.ModelSerializer):
    class Meta:
        model = Company
        fields = [
            'companyName',
            'companyCountry',
            'companyRegion',
            'companyZone',
            'companyWoreda',
            'companyKebele',
            'companyHN',
            'companyTIN',
            'companyLicense',
            'companyLogo'
        ]    


class RegistrationSerializer(serializers.ModelSerializer):
    password = serializers.CharField(
        max_length=68, min_length=6, write_only=True)
    user_profile = UserProfileSerializer(many=False, required=True)
    user_company = UserCompanySerializer(many=False, required=True)

    class Meta:
        model = CustomUser
        fields = ['email', 'password', 'user_profile', 'user_company']
        

    def create(self, validated_data):
        print(validated_data)
        try:
            userData = validated_data.pop('user_profile', {})
            companyData = validated_data.pop('user_company', {})

            user = CustomUser.objects.create_user(**validated_data)
            UserProfile.objects.create(user=user, **userData)
            Company.objects.create(manager=user, **companyData)
        except serializers.ValidationError as e:
            print(e.detail)

        return user
    

class LogoutSerializer(serializers.Serializer):
    refresh = serializers.CharField()

    default_error_message = {
        'bad_token': ('Token is expired or invalid')
    }

    def validate(self, attrs):
        self.token = attrs['refresh']
        return attrs

    def save(self, **kwargs):

        try:
            RefreshToken(self.token).blacklist()

        except TokenError:
            return self.default_error_message

class CheckEmailSerializer(serializers.Serializer):
    email = serializers.EmailField()

class AuthorizeSerializer(serializers.Serializer):
    pass    