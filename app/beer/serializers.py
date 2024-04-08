import os
from django.contrib.auth.hashers import check_password
from django.core.validators import RegexValidator, FileExtensionValidator
from django.core.exceptions import ValidationError
from user.models import User
from beer.models import Malts, Hops, Beer



from rest_framework import serializers 

# Create the form class.
#_AddFavoriteSerializer
class AddFavoriteSerializer(serializers.Serializer):

    def __init__(self, *args, **kwargs):
        serializers.Serializer.__init__(self, *args, **kwargs)

    beer_id = serializers.UUIDField(error_messages={
        'required': "Please enter the beer id",
    })

    def validate_beer_id(self, value):

        favorite = Beer.objects.filter(
            user__public_id = self.context['user_id'],
            id = value,
            is_active = True
        ).exists()

        if favorite:
            raise ValidationError("Beer is already in your favorite")

        beer = Beer.objects.filter(
            id = value,
            is_active = True
        ).exists()

        if not beer:
            raise ValidationError("Beer not found")
        
        return value
    

#_RemoveFavoriteSerializer
class RemoveFavoriteSerializer(serializers.Serializer):

    def __init__(self, *args, **kwargs):
        serializers.Serializer.__init__(self, *args, **kwargs)
        self.user_id = self.context['user_id']

    beer_id = serializers.UUIDField(error_messages={
        'required': "Please enter the beer id",
    })

    def validate_beer_id(self, value):

        favorite = Beer.objects.filter(
            user__public_id = self.context['user_id'],
            id = value,
            is_active = True
        ).exists()

        if not favorite:
            raise ValidationError("Beer is not in your favorite")

        return value

class ListMaltsSerializer(serializers.ModelSerializer):

    class Meta:
        model = Malts
        fields = ['name']

class ListHopsSerializer(serializers.ModelSerializer):

    class Meta:
        model = Hops
        fields = ['name']

# Create the form class.
#_CreateBeerSerializer
class CreateBeerSerializer(serializers.Serializer):

    def __init__(self, *args, **kwargs):
        serializers.Serializer.__init__(self, *args, **kwargs)

    name = serializers.CharField(max_length=10, required=True, error_messages={
        'required': "Please enter the beer id",
    })

    hops = serializers.CharField(max_length=3000, error_messages={
        'required': "Please enter beer hops",
    })

    malts = serializers.CharField(max_length=3000, error_messages={
        'required': "Please enter beer malts",
    })

    def __init__(self, *args, **kwargs):
        serializers.Serializer.__init__(self, *args, **kwargs)

    def validate_hops(self, value):
        
        try:
            eval(value)
        except:
            raise ValidationError("Hops must be a valid list of hops. Exemple: ['Fuggles', 'First Gold']")

        return value

    def validate_malts(self, value):

        try:
            eval(value)
        except:
            raise ValidationError("Malts must be a valid list of malts. Exemple: ['Maris Otter Extra Pale', 'Caramalt']")
    
    def validate_beer_id(self, value):

        beer = Beer.objects.filter(
            user__public_id = self.context['user_id'],
            id = value,
            is_active = True
        ).all()

        print(beer)
        if len(beer) > 0:
            raise ValidationError("Beer is already in your favorite")


# Create the form class.
#_ReadBeerSerializer
class ReadBeerSerializer(serializers.ModelSerializer):

    def __init__(self, *args, **kwargs):
        serializers.Serializer.__init__(self, *args, **kwargs)

    hops = ListHopsSerializer(read_only=True, many=True) 
    malts = ListMaltsSerializer(read_only=True, many=True) 

    class Meta:
        model = Beer
        fields = ['id', 'name', 'hops', 'malts']

#_UpdateBeerSerializer
class UpdateBeerSerializer(serializers.Serializer):

    def __init__(self, *args, **kwargs):
        serializers.Serializer.__init__(self, *args, **kwargs)

    name = serializers.CharField(max_length=10, required=True, error_messages={
        'required': "Please enter a beer name",
    })

    hops = serializers.CharField(max_length=3000, error_messages={
        'required': "Please enter beer hops",
    })

    malts = serializers.CharField(max_length=3000, error_messages={
        'required': "Please enter beer malts",
    })

    def __init__(self, *args, **kwargs):
        serializers.Serializer.__init__(self, *args, **kwargs)

    def validate_hops(self, value):
        
        try:
            eval(value)
        except:
            raise ValidationError("Hops must be a valid list of hops. Exemple: ['Fuggles', 'First Gold']")

        return value

    def validate_malts(self, value):

        try:
            eval(value)
        except:
            raise ValidationError("Malts must be a valid list of malts. Exemple: ['Maris Otter Extra Pale', 'Caramalt']")