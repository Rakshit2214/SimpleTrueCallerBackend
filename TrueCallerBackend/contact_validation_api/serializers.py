from rest_framework import serializers
from django.contrib.auth import get_user_model
from .models import ContactStoreBO, AuthDetailStore, RegisteredAppUser
from .encryption import SecureCredentials

User = get_user_model()


class AuthDetailStoreSerializer(serializers.ModelSerializer):
    class Meta:
        model = AuthDetailStore
        fields = ('username', 'password')

    def create(self, validated_data):
        validated_data = SecureCredentials.get_decrypted(validated_data)

       #Hashing should happen at frontend
       # validated_data['username'] = sha256(validated_data['username'].encode('utf-8')).hexdigest()
       # validated_data['password'] = sha256(validated_data['password'].encode('utf-8')).hexdigest()

        return super().create(validated_data)


class RegisteredAppUserSerializer(serializers.ModelSerializer):
    username = AuthDetailStoreSerializer()

    class Meta:
        model = RegisteredAppUser
        fields = ('id', 'name', 'username', 'registeredUserNumber', 'userEmailId')

    def create(self, validated_data):
        auth_data = validated_data.pop('username')
        auth_detail = AuthDetailStore.objects.create(**auth_data)
        registered_user = RegisteredAppUser.objects.create(username=auth_detail, **validated_data)
        ContactStoreBO.objects.create(
            registeredContactOwner=registered_user,
            ContactName=registered_user.name,
            ContactNumber=registered_user.registeredUserNumber,
            ContactEmailId=registered_user.userEmailId,
            ContactSpamValue=0.0,
            ContactIsSpam=False,
        )
        return registered_user

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        contact_spam_value = (ContactStoreBO.objects.get(ContactNumber=representation['registeredUserNumber'])).ContactSpamValue
        contact_is_spam = (ContactStoreBO.objects.get(ContactNumber=representation['registeredUserNumber'])).ContactIsSpam

        update_data = {
            'spamValue': contact_spam_value,
            'isSpam': contact_is_spam,
        }
        representation.update(update_data)

        return representation


class ContactStoreBOSerializer(serializers.ModelSerializer):
    class Meta:
        model = ContactStoreBO
        fields = ('id', 'registeredContactOwner', 'ContactName', 'ContactEmailId'
                  , 'ContactNumber', 'ContactSpamValue', 'ContactIsSpam')

    def create(self, validated_data):
        return super().create(validated_data)
