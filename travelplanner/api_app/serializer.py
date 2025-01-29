from rest_framework import serializers
from .models import CustomUser,Destination,TravelPlan,Activity,Comment
from django.core.exceptions import ValidationError
from datetime import date
import bleach 
from django.utils.text import slugify

from PIL import Image
from io import BytesIO
from django.core.files.base import ContentFile



class CustomUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ("id", "username", "password", "first_name", "last_name", "email", "sex", "birthdate", "bio")

    def create(self, validated_data):
        password = validated_data.pop("password")
        user = CustomUser(**validated_data)
        user.set_password(password)
        user.save()
        return user

    def validate_username(self,value):                          #validate_<field_name>
        restricted_words = ['Satan', 'Voldemort', 'Sex']

        if any(word in value.lower() for word in restricted_words):
            raise serializers.ValidationError("username must not contain these words")
        return value
    
    def validate_bio(self,value):
        if len(value) < 15:
            raise serializers.ValidationError("bio must be at least 15 characters")
        return value
    

    def validate_birthdate(self,value):
        today = date.today()
        age = today.year - value.year 
        if age < 16:
            raise serializers.ValidationError("User must be at least 16 years old.")
        return value
        

    def slugify_username(self,value):
        return slugify(value)
        
    def validate(self, data):

        data['username'] = self.slugify_username(data['username'])

        

        return data
    
    def __str__(self):
        return self.username
        
        
class DestinationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Destination
        fields = "__all__"  

    def validate_name(self,value):                             #validate_<field_name>
        restricted_words = ['Badword', 'evilword', 'forbiddenword']

        if any(word in value.lower() for word in restricted_words):
            raise serializers.ValidationError("name must not contain these words")
        return value

    name = serializers.CharField(required = True, max_length = 100)

    def __str__(self):
        return self.name

    
          
        
      
class TravelPlanSerializer(serializers.ModelSerializer):
    class Meta:
        model = TravelPlan
        fields = "__all__"  
  

    def validate_traveldays(self,value):
 
        if value <= 1:
            raise serializers.ValidationError("The duration has to be at least 2 days.")
        return value
        
    title = serializers.CharField(max_length = 100, required = True)

    def __str__(self):
        return self.name
        
       
class ActivitySerializer(serializers.ModelSerializer):
    class Meta:
        model = Activity
        fields = "__all__"     

    def validate_name(self,value):
        restricted_words = ['Drugs', 'Swinger', 'Sextourism']

        if any(word in value.lower() for word in restricted_words):
            raise serializers.ValidationError("name must not contain these words")
        return value 
    
    name = serializers.CharField(max_length = 100, required = True)
              
    def __str__(self):
        return self.name 
        
class CommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = "__all__"       

    def sanitize_html(self,value):
        allowed_tags = ['b', 'i', 'u', 'em', 'strong']
        return bleach.clean(value, tags=allowed_tags, strip=True)

    def validate(self, data):

        data['comment'] = self.sanitize_html(data['comment'])

        return data   

    