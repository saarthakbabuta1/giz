"""Collection of general helper functions."""
import datetime
from typing import Dict,Optional,Union
import pytz
from django.http import HttpRequest
from django.utils import timezone
from django.utils.text import gettext_lazy as _
from rest_framework.exceptions import APIException,AuthenticationFailed,NotFound,PermissionDenied
from users import update_user_settings
from users.models import AuthTransaction,OTPValidation,User
from .keys import AWS_ACCESS_KEY, AWS_SECRET_KEY,AWS_REGION
from rest_framework.response import Response
from rest_framework import status
from botocore.exceptions import ClientError
import re

import boto3
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.utils import datetime_from_epoch
from drfaddons.utils import send_message

user_settings: Dict[
    str, Union[bool, Dict[str, Union[int, str, bool]]]
] = update_user_settings()
otp_settings: Dict[str, Union[str, int]] = user_settings["OTP"]


def get_client_ip(request: HttpRequest) -> Optional[str]:
    x_forwarded_for = request.META.get("HTTP_X_FORWARDED_FOR")
    if x_forwarded_for:
        return x_forwarded_for.split(",")[0]
    else:
        return request.META.get("REMOTE_ADDR")


def datetime_passed_now(source: datetime.datetime) -> bool:

    if source.tzinfo is not None and source.tzinfo.utcoffset(source) is not None:
        return source <= datetime.datetime.utcnow().replace(tzinfo=pytz.utc)
    else:
        return source <= datetime.datetime.now()


def check_unique(prop: str, value: str) -> bool:
    user = User.objects.extra(where=[prop + " = '" + value + "'"])
    return user.count() == 0


def generate_otp(prop: str, value: str) -> OTPValidation:
    # Create a random number
    random_number: str = User.objects.make_random_password(
        length=otp_settings["LENGTH"], allowed_chars=otp_settings["ALLOWED_CHARS"]
    )

    # Checks if random number is unique among non-validated OTPs and
    # creates new until it is unique.
    while OTPValidation.objects.filter(otp__exact=random_number).filter(
        is_validated=False
    ):
        random_number: str = User.objects.make_random_password(
            length=otp_settings["LENGTH"], allowed_chars=otp_settings["ALLOWED_CHARS"]
        )

    # Get or Create new instance of Model with value of provided value
    # and set proper counter.
    try:
        otp_object: OTPValidation = OTPValidation.objects.get(destination=value)
    except OTPValidation.DoesNotExist:
        otp_object: OTPValidation = OTPValidation()
        otp_object.destination = value
    else:
        if not datetime_passed_now(otp_object.reactive_at):
            return otp_object

    otp_object.otp = random_number
    otp_object.prop = prop

    # Set is_validated to False
    otp_object.is_validated = False

    # Set attempt counter to OTP_VALIDATION_ATTEMPTS, user has to enter
    # correct OTP in 3 chances.
    otp_object.validate_attempt = otp_settings["VALIDATION_ATTEMPTS"]

    otp_object.reactive_at = timezone.now() - datetime.timedelta(minutes=1)
    otp_object.save()
    return otp_object


def send_otp(value: str, otpobj: OTPValidation, recip: str) -> Dict:

    if not datetime_passed_now(otpobj.reactive_at):
        raise PermissionDenied(
            detail=_(f"OTP sending not allowed until: {otpobj.reactive_at}") )

    if value.isdigit():
        client = boto3.client("sns",aws_access_key_id=AWS_ACCESS_KEY,
            aws_secret_access_key=AWS_SECRET_KEY,
        region_name=AWS_REGION)
    
        try:
            print("Phone Number:","+91"+value)
            response = client.publish(
            PhoneNumber="+91"+value,
            Message="Your OTP for login is {}".format(otpobj.otp))
        except ValueError as err:
            raise APIException(_(f"Server configuration error occurred: {err}"))
    
    elif re.match(r"[^@]+@[^@]+\.[^@]+", value):

        # Create an ses client for sending email            
        # The character encoding for the email.
        CHARSET = "UTF-8"

        # Create a new SES resource and specify a region.
        client = boto3.client('ses',
        aws_access_key_id=AWS_ACCESS_KEY,
        aws_secret_access_key=AWS_SECRET_KEY,
        region_name=AWS_REGION)

        # Try to send the email.
        try:
            #Provide the contents of the email.
            response = client.send_email(
                Destination={
                    'ToAddresses': [
                        'project.pvport@gmail.com',
                    ],
                },
                Message={
                    'Body': {
                        'Text': {
                            'Charset': CHARSET,
                            'Data': "OTP is {}".format(otpobj.otp)
                        },
                    },
                    'Subject': {
                        'Charset': CHARSET,
                        'Data': "OTP",
                    },
                },
                Source="project.pvport@gmail.com",
            )
    # Display an error if something goes wrong.	
        except ClientError as e:
            print(e.response['Error']['Message'])
        else:
            print("Email sent! Message ID:"),
            print(response['MessageId'])
    otpobj.reactive_at = timezone.now() + datetime.timedelta(
        minutes=otp_settings["COOLING_PERIOD"])

    otpobj.save()
 

    return {"success":True}


def login_user(user: User, request: HttpRequest) -> Dict[str, str]:
    token: RefreshToken = RefreshToken.for_user(user)

    # Add custom claims
    if hasattr(user, "email"):
        token["email"] = user.email

    if hasattr(user, "mobile"):
        token["mobile"] = user.mobile

    if hasattr(user, "name"):
        token["name"] = user.name

    user.last_login = timezone.now()
    user.save()

    AuthTransaction(
        created_by=user,
        ip_address=get_client_ip(request),
        token=str(token.access_token),
        refresh_token=str(token),
        session=user.get_session_auth_hash(),
        expires_at=datetime_from_epoch(token["exp"]),
    ).save()

    return {
        "refresh_token": str(token),
        "token": str(token.access_token),
        "session": user.get_session_auth_hash(),
    }


def check_validation(value: str) -> bool:
    try:
        otp_object: OTPValidation = OTPValidation.objects.get(destination=value)
        return otp_object.is_validated
    except OTPValidation.DoesNotExist:
        return False


def validate_otp(value: str, otp: int) -> bool:
    try:
        # Try to get OTP Object from Model and initialize data dictionary
        otp_object: OTPValidation = OTPValidation.objects.get(
            destination=value, is_validated=False
        )
    except OTPValidation.DoesNotExist:
        raise NotFound(
            detail=_(
                "No pending OTP validation request found for provided "
                "destination. Kindly send an OTP first"
            )
        )
    # Decrement validate_attempt
    otp_object.validate_attempt -= 1

    if str(otp_object.otp) == str(otp):
        # match otp
        otp_object.is_validated = True
        otp_object.save()
        return True

    elif otp_object.validate_attempt <= 0:
        # check if attempts exceeded and regenerate otp and raise error
        generate_otp(otp_object.prop, value)
        raise AuthenticationFailed(
            detail=_("Incorrect OTP. Attempt exceeded! OTP has been reset.")
        )

    else:
        # update attempts and raise error
        otp_object.save()
        raise AuthenticationFailed(
            detail=_(
                f"OTP Validation failed! {otp_object.validate_attempt} attempts left!"
            )
        )
