from django.http import JsonResponse

from rest_framework.views import APIView
from rest_framework import generics, permissions, status
from rest_framework_simplejwt.tokens import RefreshToken

from .authentication import Authentication
from .serializers import RegisteredAppUserSerializer, ContactStoreBOSerializer
from .models import ContactStoreBO, RegisteredAppUser

from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response

from django.contrib.auth import login, logout
from django.contrib import messages


class LoginView(APIView):
    permission_classes = [permissions.AllowAny]

    def post(self, request):
        username, password = self.get_details(request)
        user = Authentication.user_authentication(username, password)
        if user is not None:
            login(request, user)
            refresh = RefreshToken.for_user(user).access_token
            return JsonResponse(data={'message': "User Validated Successfully", 'token': f"{refresh}"}, status=200, safe=True)
        return JsonResponse(data={'error': 'Invalid credentials'}, safe=True, status=400)

    @staticmethod
    def get_details(request):
        return request.data.get('username'), request.data.get('password')


class LogoutView(APIView):
    def post(self, request):
        logout(request)
        messages.success(request, 'You have been logged out successfully.')
        return JsonResponse(data={'message': "User Logged Out Successfully"}, status=200, safe=True)


class RegisterView(generics.CreateAPIView):
    permission_classes = [permissions.AllowAny]
    queryset = RegisteredAppUser.objects.all()
    serializer_class = RegisteredAppUserSerializer


class ContactListView(generics.ListCreateAPIView):
    queryset = ContactStoreBO.objects.all()
    serializer_class = ContactStoreBOSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return self.request.user.contacts.all()

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)


@api_view(['POST'])
@permission_classes([permissions.IsAuthenticated])
def mark_contact_spam(request):
    threshold = 10
    increment = 0.01
    contact_number = request.data.get('contact_number')
    try:
        contactQuerySet = ContactStoreBO.objects.filter(ContactNumber=contact_number)

        if not contactQuerySet.exists():
            return Response(status=status.HTTP_404_NOT_FOUND)

        for contactDetail in contactQuerySet:
            contactDetail.ContactSpamValue += increment
            if contactDetail.ContactSpamValue >= threshold:
                contactDetail.ContactIsSpam = True
            contactDetail.save()
        return Response(status=status.HTTP_204_NO_CONTENT)
    except ContactStoreBO.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)


def is_user_in_contact_list(user, requester_contact_number):
    for contactStoreBO in user.contacts:
        if contactStoreBO.ContactNumber == requester_contact_number:
            return True
        return False


@api_view(['GET'])
@permission_classes([permissions.AllowAny])
def search_by_name(request):
    name = request.data.get('name')
    contacts = (ContactStoreBO.objects.filter(ContactName__icontains=name, ContactIsSpam=False)
                .order_by('ContactName'))
    contactStoreBoSerializer = ContactStoreBOSerializer(contacts, many=True)
    return JsonResponse({'Search_result': contactStoreBoSerializer.data}, status=200)


@api_view(['GET'])
@permission_classes([permissions.AllowAny])
def search_by_phone(request):
    contact_number_search = request.data.get('phone_number')
    try:
        user = RegisteredAppUser.objects.get(registeredUserNumber=contact_number_search)
        userSerializer = RegisteredAppUserSerializer(user)
        return Response(userSerializer.data, status=status.HTTP_200_OK)

    except RegisteredAppUser.DoesNotExist:
        contacts = ContactStoreBO.objects.filter(phone_number=phone_number)
        if contacts.exists():
            contact_data = ContactStoreBOSerializer(contacts, many=True).data
            return Response(contact_data, status=status.HTTP_200_OK)
        else:
            return Response({'detail': 'No matches found.'}, status=status.HTTP_404_NOT_FOUND)
