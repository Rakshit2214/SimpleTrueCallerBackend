from django.conf import settings
from cryptography.fernet import Fernet
from django.http import JsonResponse
from rest_framework.views import APIView


class EncryptData:
    def __init__(self, key):
        self.key = key
        self.cipher_suite = Fernet(key)

    def encrypt_data(self, data):
        return self.cipher_suite.encrypt(data.encode()).decode()

    def decrypt_data(self, encrypted_data):
        return self.cipher_suite.decrypt(encrypted_data.encode()).decode()


class SecureCredentials(APIView):

    encryptData = EncryptData(settings.ENCRYPTION_KEY)

    @staticmethod
    def get_encrypted(request):
        encrypt_username = SecureCredentials.encryptData.encrypt_data(request.data.get('username'))
        encrypt_password = SecureCredentials.encryptData.encrypt_data(request.data.get('password'))
        return JsonResponse({'username': encrypt_username, 'password': encrypt_password}, safe=True)

    @staticmethod
    def get_decrypted(request):
        decrypt_username = SecureCredentials.encryptData.decrypt_data(request.data.get('username'))
        decrypt_password = SecureCredentials.encryptData.decrypt_data(request.data.get('password'))
        return JsonResponse({'username': decrypt_username, 'password': decrypt_password}, safe=True)
