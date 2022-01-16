"""Custom Managers for drf-user"""
from typing import Optional
from django.contrib.auth.base_user import BaseUserManager
from users import update_user_settings

class UserManager(BaseUserManager):
    """
    UserManager class for Custom User Model
    """

    use_in_migrations = True

    def _create_user(
        self,
        username: str,
        email: str,
        password: str,
        fullname: str,
        groups: Optional[str],
        mobile: Optional[str] = None,
        **kwargs
    ):
        """
        Creates and saves a User with given details
        """
        email = self.normalize_email(email)
        user = self.model(
            username=username, email=email, name=fullname, 
            mobile=mobile, 
            groups = groups,**kwargs
        )
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_user(
        self,
        username: str,
        email: str,
        password: str,
        name: str,
        groups: Optional[str],
        mobile: Optional[str] = None,
        **kwargs
    ):
        """
        Creates a normal user considering the specified user settings
        from Django Project's settings.py

        Parameters
        ----------
        username: str
        email: str
        password: str
        name: str
        mobile: str, optional
        kwargs

        Returns
        -------
        User Instance
        """
        vals = update_user_settings()

        kwargs.setdefault("is_superuser", False)
        kwargs.setdefault("is_staff", False)
        kwargs.setdefault("is_active", True)
        #kwargs.setdefault("is_active", vals.get("DEFAULT_ACTIVE_STATE", False))

        return self._create_user(username, email, password, name,groups, mobile, **kwargs)

    def create_superuser(
        self,
        username: str,
        email: str,
        password: str,
        name: str,
        groups: Optional[str],
        mobile: Optional[str] = None,
        **kwargs
    ):
        """
        Creates a super user considering the specified user settings
        from Django Project's settings.py
        Parameters
        ----------
        username: str
        email: str
        password: str
        name: str
        mobile: str, optional
        kwargs

        Returns
        -------
        User Instance
        """
        vals = update_user_settings()

        kwargs.setdefault("is_superuser", True)
        kwargs.setdefault("is_staff", True)
        kwargs.setdefault("is_active",True)
        #kwargs.setdefault("is_active", vals.get("DEFAULT_ACTIVE_STATE", False))

        if kwargs.get("is_superuser") is not True:
            raise ValueError("Superuser must have is_superuser=True.")

        if kwargs.get("is_staff") is not True:
            raise ValueError("Superuser must have is_staff=True.")

        return self._create_user(username, email, password, name,groups, mobile, **kwargs)
