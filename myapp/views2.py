from django.shortcuts import render

# Create your views here.

from rest_framework import status
from rest_framework.response import Response
from rest_framework.generics import (
CreateAPIView,
RetrieveAPIView,
)
from rest_framework.permissions import IsAuthenticated

from .models import CustomUser
from utilities import messages
from .serializers import LoginSerializer
from utilities.utils import ResponseInfo
from utilities.firebase import (
login_firebase_user,
logout_firebase_user,
FirebaseAuthentication,
)


class LoginAPIView(CreateAPIView):
    """
    Class for creating api for login user.
    """
    permission_classes = ()
    authentication_classes = ()
    serializer_class = LoginSerializer

    def __init__(self, **kwargs):
        """
        Constructor function for formatting the web response to return.
        """
        self.response_format = ResponseInfo().response
        super(LoginAPIView, self).__init__(**kwargs)

    def post(self, request, *args, **kwargs):
        """
        POST Method for login users.
        """
        try:
            CustomUser.objects.get(email=request.data["email"])
            serializer = self.get_serializer(data=request.data)

            if serializer.is_valid(raise_exception=True):
                user = login_firebase_user(serializer.validated_data.pop("email"), serializer.validated_data.pop('password'))
            if not user.get("error"):
                self.response_format["data"] = user
                self.response_format["message"] = [messages.SUCCESS]
            else:
                self.response_format["status_code"] = status.HTTP_400_BAD_REQUEST
                self.response_format["error"] = "login_error"
                self.response_format["message"] = [messages.INVALID_CREDENTIALS]
        except CustomUser.DoesNotExist:
            self.response_format["data"] = None
            self.response_format["error"] = "user"
            self.response_format["status_code"] = status.HTTP_404_NOT_FOUND
            self.response_format["message"] = [messages.UNAUTHORIZED_ACCOUNT]
            return Response(self.response_format)


class LogoutAPIView(CreateAPIView):
    """
    Class for creating api for logout user.
    """
    permission_classes = (IsAuthenticated,)
    authentication_classes = (FirebaseAuthentication,)
    serializer_class = LoginSerializer

    def __init__(self, **kwargs):
        """
        Constructor function for formatting the web response to return.
        """
        self.response_format = ResponseInfo().response
        super(LogoutAPIView, self).__init__(**kwargs)

    def post(self, request, *args, **kwargs):
        """
        POST Method for logout users.
        """
        uid = request.user.uid
        logout_firebase_user(uid)

        self.response_format["data"] = None
        self.response_format["error"] = None
        self.response_format["status_code"] = status.HTTP_200_OK
        self.response_format["message"] = [messages.LOGOUT_SUCCESS]
        return Response(self.response_format)


class GetDataAPIView(RetrieveAPIView):
    """
    Class for creating api for getting authenticated data.
    """
    permission_classes = (IsAuthenticated,)
    authentication_classes = (FirebaseAuthentication,)
    serializer_class = LoginSerializer

    def __init__(self, **kwargs):
        """
        Constructor function for formatting the web response to return.
        """
        self.response_format = ResponseInfo().response
        super(GetDataAPIView, self).__init__(**kwargs)

    def get(self, request, *args, **kwargs):
        """
        GET Method for getting authenticated data.
        """
        self.response_format["data"] = request.user.email
        return Response(self.response_format)