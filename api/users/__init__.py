"""Django REST Framework - User! User App for Django with API Views"""

from django.conf import settings

default_app_config = "users.apps.UsersConfig"

user_settings = {
    "MOBILE_OPTIONAL": False,
    "DEFAULT_ACTIVE_STATE": True,
    "OTP": {
        "LENGTH": 5,
        "ALLOWED_CHARS": "1234567890",
        "VALIDATION_ATTEMPTS": 3,
        "SUBJECT": "OTP for Verification",
        "COOLING_PERIOD": 3,
    },
    "MOBILE_VALIDATION": False,
    "EMAIL_VALIDATION": False,
    "REGISTRATION": {
        "SEND_MAIL": False,
        "SEND_MESSAGE": False,
        "MAIL_SUBJECT": "Welcome to DRF-USER",
        "SMS_BODY": "Your account has been created",
        "TEXT_MAIL_BODY": "Your account has been created.",
        "HTML_MAIL_BODY": "Your account has been created.",
    },
}


def update_user_settings() -> dict:
    """
    Updates user setting from django default setting

    TODO: Think of a better way, using Signal preferably.

    Returns
    -------
    user_settings: dict

    """
    custom_settings = getattr(settings, "USER_SETTINGS", None)

    if custom_settings:
        if not isinstance(custom_settings, dict):
            raise TypeError("USER_SETTING must be a dict.")

        for key, value in custom_settings.items():
            if key not in ["OTP", "REGISTRATION"]:
                user_settings[key] = value
            elif key == "OTP":
                if not isinstance(value, dict):
                    raise TypeError("USER_SETTING attribute OTP must be a" " dict.")
                for otp_key, otp_value in value.items():
                    user_settings["OTP"][otp_key] = otp_value
            elif key == "REGISTRATION":
                if isinstance(value, dict):
                    for reg_key, reg_value in value.items():
                        user_settings["REGISTRATION"][reg_key] = reg_value
                else:
                    raise TypeError(
                        "USER_SETTING attribute REGISTRATION" " must be a dict."
                    )
        if user_settings["REGISTRATION"]["SEND_MAIL"]:
            if not getattr(settings, "EMAIL_HOST", None):
                raise ValueError(
                    "EMAIL_HOST must be defined in django setting" " for sending mail."
                )
            if not getattr(settings, "EMAIL_FROM", None):
                raise ValueError(
                    "EMAIL_FROM must be defined in django setting"
                    " for sending mail. Who is sending email?"
                )

    return user_settings
