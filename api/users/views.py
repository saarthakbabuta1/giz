from django.shortcuts import render
from django.conf import settings
from django.utils import timezone
from rest_framework.generics import CreateAPIView
from rest_framework import status
from rest_framework.exceptions import APIException,ValidationError
from rest_framework.generics import CreateAPIView,RetrieveUpdateAPIView
from rest_framework.parsers import JSONParser
from rest_framework.permissions import AllowAny,IsAuthenticated
from rest_framework.renderers import JSONRenderer
from rest_framework.response import Response
from rest_framework.views import APIView
from django.utils.text import gettext_lazy as _

from .serializers import UserSerializer,CustomTokenObtainPairSerializer
from .serializers import CheckUniqueSerializer,OTPSerializer
from .serializers import OTPLoginRegisterSerializer,PasswordResetSerializer
from .models import User,AuthTransaction
from .utils import get_client_ip,check_unique, login_user,validate_otp,send_otp,generate_otp
from .variables import EMAIL,MOBILE

from rest_framework_simplejwt.settings import api_settings
from drfaddons.utils import JsonResponse
from rest_framework_simplejwt.exceptions import InvalidToken
from rest_framework_simplejwt.exceptions import TokenError
from rest_framework_simplejwt.views import TokenRefreshView



# Create your views here.

class RegisterView(CreateAPIView):

    permission_classes = (AllowAny,)
    serializer_class = UserSerializer

    def perform_create(self, serializer):
        """Override perform_create to create user"""
        data = {
            "username": serializer.validated_data["username"],
            "email": serializer.validated_data["email"],
            "name": serializer.validated_data["name"],
            "password": serializer.validated_data["password"],
        }
        try:
            data["mobile"] = serializer.validated_data["mobile"]
        except KeyError:
            if not settings.USER_SETTINGS["MOBILE_OPTIONAL"]:
                raise ValidationError({"error": "Mobile is required."})
        return User.objects.create_user(**data)

class LoginView(APIView):

    permission_classes = (AllowAny,)
    serializer_class = CustomTokenObtainPairSerializer

    def post(self, request, *args, **kwargs):
        """
        Process a login request via username/password.
        """
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        # if data is valid then create a record in auth transaction model
        user = serializer.user
        
        token = serializer.validated_data.get("access")
        refresh_token = serializer.validated_data.get("refresh")

        AuthTransaction(
            created_by=user,
            token=str(token),
            refresh_token=str(refresh_token),
            ip_address=get_client_ip(self.request),
            session=user.get_session_auth_hash(),
            expires_at=timezone.now() + api_settings.ACCESS_TOKEN_LIFETIME,
        ).save()

        # For backward compatibility, returning custom response
        resp = {
            "refresh_token": str(refresh_token),
            "token": str(token),
            "session": user.get_session_auth_hash(),
        }
        return Response(resp, status=status.HTTP_200_OK)


class CheckUniqueView(APIView):

    renderer_classes = (JSONRenderer,)
    permission_classes = (AllowAny,)
    serializer_class = CheckUniqueSerializer

    def validated(self, serialized_data, *args, **kwargs):
        """Validates the response"""
        return (
            {
                "unique": check_unique(
                    serialized_data.validated_data["prop"],
                    serialized_data.validated_data["value"],
                )
            },
            status.HTTP_200_OK,
        )

    def post(self, request):
        """Overrides post method to validate serialized data"""
        serialized_data = self.serializer_class(data=request.data)
        if serialized_data.is_valid():
            return JsonResponse(self.validated(serialized_data=serialized_data))
        else:
            return JsonResponse(
                serialized_data.errors, status=status.HTTP_422_UNPROCESSABLE_ENTITY
            )

class RetrieveUpdateUserAccountView(RetrieveUpdateAPIView):

    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = (IsAuthenticated,)
    lookup_field = "created_by"

    def get_object(self):
        """Fetches user from request"""

        return self.request.user

    def update(self, request, *args, **kwargs):
        """Updates user's password"""
        print("New password; ",request.data["password"])
        print("User here: ",self.request.user)
        

        if "password" in request.data.keys():
            self.request.user.set_password('getmeonline1*')
            self.request.user.save()

        return super(RetrieveUpdateUserAccountView, self).update(
            request, *args, **kwargs
        )

class CustomTokenRefreshView(TokenRefreshView):

    def post(self, request, *args, **kwargs):
        """
        Process request to generate new access token using
        refresh token.
        """
        serializer = self.get_serializer(data=request.data)

        try:
            serializer.is_valid(raise_exception=True)
        except TokenError as e:
            raise InvalidToken(e.args[0])

        token = serializer.validated_data.get("access")

        auth_transaction = AuthTransaction.objects.get(
            refresh_token=request.data["refresh"]
        )
        auth_transaction.token = token
        auth_transaction.expires_at = (
            timezone.now() + api_settings.ACCESS_TOKEN_LIFETIME
        )
        auth_transaction.save(update_fields=["token", "expires_at"])

        return Response({"token": str(token)}, status=status.HTTP_200_OK)


class OTPView(APIView):

    permission_classes = (AllowAny,)
    serializer_class = OTPSerializer

    def post(self, request, *args, **kwargs):
        """Overrides post method to validate serialized data"""
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)

        destination = serializer.validated_data.get("destination")
        prop = serializer.validated_data.get("prop")
        user = serializer.validated_data.get("user")
        email = serializer.validated_data.get("email")
        is_login = serializer.validated_data.get("is_login")

        if "verify_otp" in request.data.keys():
            if validate_otp(destination, request.data.get("verify_otp")):
                if is_login:
                    return Response(
                        login_user(user, self.request), status=status.HTTP_202_ACCEPTED
                    )
                else:
                    return Response(
                        data={
                            "OTP": [
                                _("OTP Validated successfully!"),
                            ]
                        },
                        status=status.HTTP_202_ACCEPTED,
                    )
        else:
            otp_obj = generate_otp(prop, destination)
            
            sentotp = send_otp(destination, otp_obj, email)

            if sentotp["success"]:
                otp_obj.send_counter += 1
                otp_obj.save()

                return Response(sentotp, status=status.HTTP_201_CREATED)
            else:
                raise APIException(
                    detail=_("A Server Error occurred: " + sentotp["message"])
                )

class OTPLoginView(APIView):

    permission_classes = (AllowAny,)
    renderer_classes = (JSONRenderer,)
    parser_classes = (JSONParser,)
    serializer_class = OTPLoginRegisterSerializer

    def post(self, request, *args, **kwargs):
        """Overrides post method to validate serialized data"""
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)

        verify_otp = serializer.validated_data.get("verify_otp", None)
        name = serializer.validated_data.get("name")
        mobile = serializer.validated_data.get("mobile")
        email = serializer.validated_data.get("email")
        user = serializer.validated_data.get("user", None)

        if verify_otp:
            if validate_otp(email, verify_otp) and not user:
                user = User.objects.create_user(
                    name=name,
                    mobile=mobile,
                    email=email,
                    username=mobile,
                    password=User.objects.make_random_password(),
                )
                user.is_active = True
                user.save()
            return Response(
                login_user(user, self.request), status=status.HTTP_202_ACCEPTED
            )

        else:
            otp_obj_email = generate_otp(EMAIL, email)
            otp_obj_mobile = generate_otp(MOBILE, mobile)

            # Set same OTP for both Email & Mobile
            otp_obj_mobile.otp = otp_obj_email.otp
            otp_obj_mobile.save()

            # Send OTP to Email & Mobile
            sentotp_email = send_otp(email, otp_obj_email, email)
            sentotp_mobile = send_otp(mobile, otp_obj_mobile, email)

            message = {}
            print(sentotp_email)
            if sentotp_email["success"]:
                otp_obj_email.send_counter += 1
                otp_obj_email.save()
                message["email"] = {"otp": _("OTP has been sent successfully.")}
            else:
                message["email"] = {
                    "otp": _("OTP sending failed {}".format(sentotp_email["message"]))
                }

            if sentotp_mobile["success"]:
                otp_obj_mobile.send_counter += 1
                otp_obj_mobile.save()
                message["mobile"] = {"otp": _("OTP has been sent successfully.")}
            else:
                message["mobile"] = {
                    "otp": _("OTP sending failed {}".format(sentotp_mobile["message"]))
                }

            if sentotp_email["success"] or sentotp_mobile["success"]:
                curr_status = status.HTTP_201_CREATED
            else:
                raise APIException(
                    detail=_("A Server Error occurred: " + sentotp_mobile["message"])
                )

            return Response(data=message, status=curr_status)


class PasswordResetView(APIView):

    permission_classes = (AllowAny,)

    def post(self, request, *args, **kwargs):
        """Overrides post method to validate OTP and reset password"""
        serializer = PasswordResetSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        user = User.objects.get(email=serializer.validated_data["email"])

        if validate_otp(
            serializer.validated_data["email"], serializer.validated_data["otp"]
        ):
            # OTP Validated, Change Password
            user.set_password(serializer.validated_data["password"])
            user.save()
            return JsonResponse(
                content="Password Updated Successfully.",
                status=status.HTTP_202_ACCEPTED,
            )
