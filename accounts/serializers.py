from rest_framework import serializers
from accounts.models import User, Role
from rest_framework.validators import UniqueValidator
from django.contrib.auth.password_validation import validate_password


class RegistrationSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(
        required=True,
        validators=[UniqueValidator(queryset=User.objects.all())]
    )

    password = serializers.CharField(write_only=True, required=True, validators=[validate_password])
    password2 = serializers.CharField(write_only=True, required=True)
    roles = serializers.PrimaryKeyRelatedField(queryset=Role.objects.all(), many=True)

    class Meta:
        model = User
        fields = ('username', 'password', 'password2','roles', 'email','address', 'first_name', 'last_name')
        extra_kwargs = {
            'username': {'required': True},
            'password': {'required': True},
            'password2': {'required': True},
            'email': {'required': True},
            'roles': {'required': True}
        }

    def validate(self, attrs):
        if attrs['password'] != attrs['password2']:
            raise serializers.ValidationError({"password": "Password fields didn't match."})
        return attrs

    def create(self, validated_data):
        import ipdb
        ipdb.set_trace()
        roles = validated_data.pop('roles', [])
        user = User.objects.create(
            username=validated_data['username'],
            email=validated_data['email'],
            first_name=validated_data['first_name'],
            last_name=validated_data['last_name']
        )
        for role in roles:
            user.roles.add(role)

        user.set_password(validated_data['password'])
        user.save()

        return user


class UserSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = ('username', 'first_name', 'last_name','role' ,'address','email', 'is_staff',
                  'is_active', 'date_joined')
