from rest_framework import serializers
from apps.crm.models.admin import AdminGroup, AdminUser

# Define the serializer for AdminGroup
class AdminGroupSerializer(serializers.ModelSerializer):
    class Meta:
        model = AdminGroup
        fields = '__all__'

# Define the serializer for AdminUser
class AdminUserSerializer(serializers.ModelSerializer):
    groups = AdminGroupSerializer(many=True, read_only=True)

    class Meta:
        model = AdminUser
        fields = ('id', 'username', 'email', 'first_name', 'last_name', 'groups', 'is_staff', 'is_active')
