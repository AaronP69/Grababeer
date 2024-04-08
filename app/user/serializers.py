import os
from django.contrib.auth.hashers import check_password
from django.core.validators import RegexValidator, FileExtensionValidator
from django.core.exceptions import ValidationError
from user.models import User



from rest_framework import serializers 

# Create the form class.
#_UserSubscriptionSerializer
class UserSubscriptionSerializer(serializers.Serializer):

    first_name = serializers.CharField(max_length=30, validators=[RegexValidator(r'^[a-zA-ZàâäôéèëêïîçùûüÿæœÀÂÄÔÉÈËÊÏÎŸÇÙÛÜÆŒàèéìíîòóùúÀÈÉÌÍÎÒÓÙÚáéíñóúüÁÉÍÑÓÚÜ\'\- ]+$', "Please enter a valid first name. It can only contain the following special characters: -\' and space")], error_messages={
        'required': "Please enter your first name",
        'max_length': "Your first name cannot exceed 30 characters"
    })

    last_name = serializers.CharField(max_length=30, validators=[RegexValidator(r'^[a-zA-ZàâäôéèëêïîçùûüÿæœÀÂÄÔÉÈËÊÏÎŸÇÙÛÜÆŒàèéìíîòóùúÀÈÉÌÍÎÒÓÙÚáéíñóúüÁÉÍÑÓÚÜ\'\- ]+$', "Please enter a valid name. It can only contain the following special characters: -\' and a space.")],error_messages={
        'required': "Please enter your name",
        'max_length': "Your name cannot exceed 30 characters"
    })

    email = serializers.EmailField(max_length=200, error_messages={
        'required': "Please enter your email",
        'invalid' : "Please enter a valid email address in the format: exemple@exemple.com",
        'max_length': "Your email cannot exceed 200 characters"
    })

    password = serializers.CharField(max_length=200, validators=[RegexValidator(r'^(?=.*\d).{8,}$', "Your password must contain at least eight characters, one number and one letter.")], error_messages={
        'required': "Please enter your password",
        'max_length': "Your password cannot exceed 200 characters."
    })

    confirm_password = serializers.CharField(error_messages={
        'required': "Please confirm your password"
    })

    def __init__(self, *args, **kwargs):
        serializers.Serializer.__init__(self, *args, **kwargs)

    def validate_email(self, value):
        
        try:
            email = value
            user_exist = User.objects.filter(username=email, is_active=True).count()
        except:
            user_exist = False

        if user_exist > 0:
            raise ValidationError("An account already uses this email address")

        return value

    def validate_password(self, value):

        # Check if password is matching with his confirmation
        try:
            password = value
            confirm_password = self.initial_data['confirm_password']
        except KeyError:
            password = True
            confirm_password = True

        if password != confirm_password:
            raise ValidationError("Your password confirmation must be the same as your password")
        
        return value

#_UpdateUserSerializer
class UpdateUserSerializer(serializers.Serializer):
    def __init__(self, *args, **kwargs):
        serializers.Serializer.__init__(self, *args, **kwargs)
        self.user_id = self.context['user_id']

    first_name = serializers.CharField(max_length=200, validators=[RegexValidator(r'^[a-zA-Z\'\- ]+$', "Please enter a valid first name. It can only contain the following characters: -\and a space.")], error_messages={
        'required': "Please enter your first name",
        'max_length': "Your first name cannot exceed 200 characters"
    })

    last_name = serializers.CharField(max_length=200, validators=[RegexValidator(r'^[a-zA-Z\'\- ]+$', "Please enter a valid first name. It can only contain the following characters: -\and a space.")],error_messages={
        'required': "Please enter your name",
        'max_length': "Your name cannot exceed 200 characters"
    })

    email = serializers.EmailField(max_length=200, error_messages={
        'required': "Please enter your email",
        'invalid' : "Please enter a valid email address in the format: exemple@exemple.com",
        'max_length': "Your email cannot exceed 200 characters"
    })

    password = serializers.CharField(max_length=200, error_messages={
        'max_length': "Your password cannot exceed 200 characters."
    })

    def validate_email(self, value):

        try:
            email = value
            user = User.objects.get(email=email, is_active=True)
            user_id = self.user_id
            current_user = User.objects.get(
                public_id = user_id,
                is_active = True
            )

            if current_user.id != user.id and user:
                raise ValidationError("An account already uses this email address")
        except:
            print('')

        return value


    def validate_password(self, value):

        try:
            user_id = self.user_id
            user = User.objects.get(
                public_id = user_id,
                is_active = True
            )

            password = value
            password_match = check_password(password, user.password)

            if not password_match:
                raise ValidationError("Your account password was not recognized")

        except KeyError:
            print('')

        return value

#_DeleteUserSerializer
class DeleteUserSerializer(serializers.Serializer):

    def __init__(self, *args, **kwargs):
        serializers.Serializer.__init__(self, *args, **kwargs)
        self.user_id = self.context['user_id']

    password = serializers.CharField(max_length=200, error_messages={
        'required': "Please enter your password",
        'max_length': "Your password cannot exceed 200 characters."
    })

    def validate_password(self, value):

        try:
            user_id = self.user_id
            user = User.objects.get(
                public_id = user_id,
                is_active = True
            )

            password = self.initial_data['password']
            password_match = check_password(password, user.password)

            if not password_match:
                raise ValidationError("Your account password was not recognized")

        except KeyError:
            print('')

        return value