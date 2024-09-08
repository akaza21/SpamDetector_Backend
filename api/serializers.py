from rest_framework import serializers
from .models import User, Contact, SpamReport

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'phone_number', 'email']
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        user = User.objects.create_user(**validated_data)
        return user

class ContactSerializer(serializers.ModelSerializer):
    class Meta:
        model = Contact
        fields = ['id', 'name', 'phone_number', 'email']

class SpamReportSerializer(serializers.ModelSerializer):
    class Meta:
        model = SpamReport
        fields = ['id', 'phone_number', 'timestamp']

class SearchResultSerializer(serializers.Serializer):
    name = serializers.CharField()
    phone_number = serializers.CharField()
    spam_likelihood = serializers.FloatField()
    email = serializers.EmailField(allow_null=True)

    def to_representation(self, instance):
        data = super().to_representation(instance)
        request = self.context.get('request')
        if not request or not request.user.is_authenticated:
            data.pop('email', None)
        return data