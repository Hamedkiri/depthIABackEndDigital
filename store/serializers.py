from rest_framework.serializers import ModelSerializer
from .models             import Categories, User, Articles,Comments,Pictures , Series
from rest_framework             import serializers
from rest_framework import serializers
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework_simplejwt.settings import api_settings
from django.contrib.auth.models import update_last_login
from django.core.exceptions import ObjectDoesNotExist

from django.contrib.auth import authenticate, get_user_model
from djoser.conf import settings
from djoser.serializers import TokenCreateSerializer


class ArticleListSerializer(ModelSerializer):
    
    pictureOfDescription = serializers.ImageField(required=False)


    class Meta:
        model  = Articles
        fields = ['name','availablity','category','date_created','date_updated', 'pictureOfDescription',"content","pictures","filePrincipal","description","serie","users"]#
    
    def validate(self,data):

        if Articles.objects.filter(name=data['name']).exists():
            raise serializers.ValidationError('article already exists')
        
        return data   

class SerieListSerializer(ModelSerializer):

    class Meta:
        model  = Series
        fields = ["id","name","date_updated","date_created","articles","category","availablity"]



class SerieDetailSerializer(ModelSerializer):
    
    articles = serializers.SerializerMethodField()

    class Meta:
        model  = Series
        fields = ["id","name","date_updated","date_created","articles","category","availablity"]

    def get_articles(self,instance):

        queryset   = instance.articles.all()

        serializer = ArticleListSerializer(queryset, many=True)

        return serializer.data

class CategoriesListSerializer(ModelSerializer):

    class Meta:
        model  = Categories
        fields = ['id','name','description','picture']
 
    def validate(self,data):

        if Categories.objects.filter(name=data['name']).exists():
            raise serializers.ValidationError('category already exists')
        
        return data    

 


class CategoriesDetailSerializer(ModelSerializer):

    articles = serializers.SerializerMethodField()

    class Meta:
        model  = Categories
        fields = ['id','name','description','availablity','picture','articles','description']

    def get_articles(self,instance):

        #queryset   = instance.articles.filter(availablity=True)
        queryset   = instance.articles.all()

        serializer = ArticleListSerializer(queryset, many=True)

        return serializer.data


class UserListSerializer(ModelSerializer):

    class Meta:
        model  = User
        fields = ['id','first_name', 'last_name','enterprise','email','password']

class ArticleDetailSerializer(ModelSerializer):
    
    pictureOfDescription = serializers.ImageField(required=False)
    users                = serializers.SerializerMethodField()


    class Meta:
        model  = Articles
        fields = ['name','availablity','category','date_created','date_updated', 'pictureOfDescription',"content","pictures","filePrincipal","description","serie","users"]#
    
    def get_users(self,instance):

        #queryset   = instance.articles.filter(availablity=True)
        queryset   = instance.users.all()

        serializer = UserListSerializer(queryset, many=True)

        return serializer.data






class PictureListSerializer(ModelSerializer):

    class Meta:
        model  = Pictures
        fields = ['name','picture','article']


class PictureDetailSerializer(ModelSerializer):

    user = serializers.SerializerMethodField()

    class Meta:
        model  = Pictures
        fields = ['name','picture','article','date_created','date_updated']
    
    def get_user(self,instance):

        queryset   = instance.user
        serializer = UserListSerializer(queryset,many=False)

        return serializer.data

class UserDetailSerializer(ModelSerializer):

    comments = serializers.SerializerMethodField()

    class Meta:
        model  = User
        fields = ['id','first_name','last_name','email','password','enterprise','date_joined','date_updated','is_active','comments','is_superuser','articles']

    def get_comments(self,instance):

        queryset   = instance.comments
        serializer = PictureListSerializer(queryset,many=True)

        return serializer.data

class PasswordChangeSerializer(serializers.Serializer):
    current_password = serializers.CharField(style={"input_type": "password"}, required=True)
    new_password = serializers.CharField(style={"input_type": "password"}, required=True)

    def validate_current_password(self, value):
        if not self.context['request'].user.check_password(value):
            raise serializers.ValidationError({'current_password': 'Does not match'})
        return value

class CommentListSerializer(ModelSerializer):

    class Meta:
        model  = Comments
        fields = ['id','users','comments','date_updated','date_created','availablity','articles','typeNote','isNoted']


class CommentDetailSerializer(ModelSerializer):

    articles = serializers.SerializerMethodField()

    class Meta:
        model  = Comments
        fields = ['id','users','comments','date_updated','date_created','availablity','articles','typeNote','isNoted']


    def get_articles(self,instance):

        queryset   = instance.articles.all()
        serializer = CommentListSerializer(queryset,many=True)

        return serializer.data




class LoginSerializer(TokenObtainPairSerializer):

    def validate(self, attrs):
        data = super().validate(attrs)

        refresh = self.get_token(self.user)

        data['user'] = UserDetailSerializer(self.user).data
        data['refresh'] = str(refresh)
        data['access'] = str(refresh.access_token)

        if api_settings.UPDATE_LAST_LOGIN:
            update_last_login(None, self.user)

        return data


class RegisterSerializer(UserListSerializer):
    password = serializers.CharField(max_length=128, min_length=8, write_only=True, required=True)
    email = serializers.EmailField(required=True, write_only=True, max_length=128)

    class Meta:
        model = User
        fields = ['id', 'email', 'password', 'is_active',  'date_updated']

    def create(self, validated_data):
        try:
            user = User.objects.get(email=validated_data['email'])
        except ObjectDoesNotExist:
            validated_data['is_active']=False
            user = User.objects.create_user(**validated_data)
        return user




class CustomTokenCreateSerializer(TokenCreateSerializer):

    def validate(self, attrs):
        password = attrs.get("password")
        params = {settings.LOGIN_FIELD: attrs.get(settings.LOGIN_FIELD)}
        self.user = authenticate(
            request=self.context.get("request"), **params, password=password
        )
        if not self.user:
            self.user = User.objects.filter(**params).first()
            if self.user and not self.user.check_password(password):
                self.fail("invalid_credentials")
        # We changed only below line
        if self.user: # and self.user.is_active: 
            return attrs
        self.fail("invalid_credentials")
    
