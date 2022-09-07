#from django.shortcuts import render
from django.contrib.auth import authenticate, login, logout
from rest_framework.views import APIView
from store.utils import get_tokens_for_user

from rest_framework.viewsets import ModelViewSet, ReadOnlyModelViewSet
from rest_framework.response import Response
from rest_framework.decorators import action

from store.models import Categories, Articles, User, Comments,Pictures, Series
from store.serializers import CategoriesListSerializer, CategoriesDetailSerializer, UserListSerializer, ArticleListSerializer, UserDetailSerializer,CommentListSerializer,CommentDetailSerializer, PasswordChangeSerializer,LoginSerializer, RegisterSerializer, PictureListSerializer,PictureDetailSerializer , SerieListSerializer, SerieDetailSerializer, ArticleDetailSerializer

from store.permissions import IsAdminAuthenticated
from rest_framework.permissions import IsAuthenticated
from rest_framework import status

from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework.permissions import AllowAny
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.exceptions import TokenError, InvalidToken
from rest_framework import viewsets
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from rest_framework.parsers import MultiPartParser, FormParser




class MultipleSerializerMixin:
    # Un mixin est une classe qui ne fonctionne pas de façon autonome
    # Elle permet d'ajouter des fonctionnalités aux classes qui les étendent

    detail_serializer_class = None

    def get_serializer_class(self):
        # Notre mixin détermine quel serializer à utiliser
        # même si elle ne sait pas ce que c'est ni comment l'utiliser
        if self.action == 'retrieve' and self.detail_serializer_class is not None:
            # Si l'action demandée est le détail alors nous retournons le serializer de détail
            return self.detail_serializer_class
        return super().get_serializer_class()

class AdminSerieViewset(MultipleSerializerMixin,ModelViewSet):


    serializer_class        = SerieListSerializer
    detail_serializer_class = SerieDetailSerializer
    permission_classes = [IsAdminAuthenticated]
    parser_classes = (MultiPartParser, FormParser)


    def get_queryset(self):
        return Series.objects.all()
        category_id = self.request.GET.get('category_id')

        if category_id is not None:
            queryset = queryset.all()

        return queryset


class SeriesView(MultipleSerializerMixin , ReadOnlyModelViewSet):

    serializer_class        = SerieListSerializer
    detail_serializer_class = SerieDetailSerializer
    
    def get_queryset(self):
       return Series.objects.filter(availablity=True)





class AdminCategoriesViewset(MultipleSerializerMixin,ModelViewSet):
    
    serializer_class        = CategoriesListSerializer
    detail_serializer_class = CategoriesDetailSerializer
    permission_classes = [IsAdminAuthenticated]

    def get_queryset(self):
        return Categories.objects.all()
    
    @action(detail=True, methods=['post','put','patch'])
    def able_or_disable(self, request, pk):
        # Nous pouvons maintenant simplement appeler la méthode disable
        self.get_object().able_or_disable()
        return Response()

class AdminArticleViewset(MultipleSerializerMixin,ModelViewSet):

    serializer_class = ArticleListSerializer
    detail_serializer_class = ArticleDetailSerializer
    permission_classes = [IsAdminAuthenticated]


    parser_classes = (MultiPartParser, FormParser)
    #http_method_names = ['patch',]


    def get_queryset(self):

        queryset = Articles.objects.all()
        category_id = self.request.GET.get('category_id')

        if category_id is not None:
            queryset = queryset.all()

        return queryset

    @action(detail=True, methods=['patch'],permission_classes=[IsAuthenticated])
    def addUserToArticle(self,request,pk):
        # Nous pouvons maintenant simplement appeler la méthode disable
        self.get_object().addUserToArticle(request,pk)
        return Response()

    @action(detail=True, methods=['patch'],permission_classes=[IsAuthenticated])
    def deleteUserToArticle(self,request,pk):  
        self.get_object().deleteUserToArticle(request,pk)
        return Response()

        

    """def patch(self, request, pk=None, *args, **kwargs):

        instance = self.get_object()
        serializer = self.detail_serializer_class(instance=instance,data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(data=serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response(data=serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    """

    
    

      

    
    @action(detail=True, methods=['post','put','patch'])
    def able_or_disable(self, request, pk):
        # Nous pouvons maintenant simplement appeler la méthode disable
        self.get_object().able_or_disable()
        return Response()




class AdminPictureViewset(MultipleSerializerMixin,ModelViewSet):

    serializer_class        = PictureListSerializer
    detail_serializer_class = PictureDetailSerializer
    permission_classes = [IsAdminAuthenticated]


    def get_queryset(self):
         return Pictures.objects.all()
    
    @action(detail=True, methods=['delete'])
    def cancelCommand(self, request, pk):
        self.get_object().cancelCommand()
        return Response()
    
class AdminUserViewset(MultipleSerializerMixin,ModelViewSet):

    serializer_class        = UserListSerializer
    detail_serializer_class = UserDetailSerializer

    permission_classes = [IsAdminAuthenticated]

    def get_queryset(self):
        return User.objects.all()

    @action(detail=True,methods=['post','put','patch'])
    def active_or_desactive_User(self,request,pk):
        
        self.get_object().active_or_desactive_User()
        return Response()
    
    @action(detail=True,methods=['post','put','patch'])
    def changeUserPassword(self,request,pk,newPassword):
        if request.user.is_authenticated:
            self.get_object().changeUserPassword(newPassword)
    

class AdminCommentViewset(MultipleSerializerMixin,ModelViewSet):

    serializer_class        = CommentListSerializer
    detail_serializer_class = CommentDetailSerializer

    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Comments.objects.all() 

   

     

      


class CategoriesView(MultipleSerializerMixin , ReadOnlyModelViewSet):

    serializer_class        = CategoriesListSerializer
    detail_serializer_class = CategoriesDetailSerializer
    
    def get_queryset(self):
       return Categories.objects.filter(availablity=True)
    

class UserView(MultipleSerializerMixin , ReadOnlyModelViewSet):

    serializer_class        = UserListSerializer
    detail_serializer_class = UserDetailSerializer
   
    def get_queryset(self):
        return User.objects.all()


class PictureView( MultipleSerializerMixin , ReadOnlyModelViewSet ):

    serializer_class        = PictureListSerializer
    detail_serializer_class = PictureDetailSerializer
   

    def get_queryset(self):
        return Pictures.objects.all()
    
   

class ArticleView(ReadOnlyModelViewSet):

    serializer_class = ArticleListSerializer

    def get_queryset(self):

        queryset    = Articles.objects.filter(availablity=True)
        category_id = self.request.GET.get('category_id')

        if category_id is not None:
            queryset = queryset.filter(category=category_id)

        return queryset

    """@action(detail=True,methods=['get'])
    def getArticleByname(self,request,pk,name):
        self.get_object().changeUserPassword(newPassword)
    """

class CommentViewset(ReadOnlyModelViewSet):

    serializer_class = CommentListSerializer

    def get_queryset(self):
        return Comments.objects.filter(availablity=True)



        


class LoginViewSet(ModelViewSet, TokenObtainPairView):
    serializer_class = LoginSerializer
    permission_classes = (AllowAny,)
    http_method_names = ['post']

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)

        try:
            serializer.is_valid(raise_exception=True)
        except TokenError as e:
            raise InvalidToken(e.args[0])

        return Response(serializer.validated_data, status=status.HTTP_200_OK)


class RegistrationViewSet(ModelViewSet, TokenObtainPairView):
    serializer_class = RegisterSerializer
    permission_classes = (AllowAny,)
    http_method_names = ['post']

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)

        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        refresh = RefreshToken.for_user(user)
        res = {
            "refresh": str(refresh),
            "access": str(refresh.access_token),
        }

        return Response({
            "user": serializer.data,
            "refresh": res["refresh"],
            "token": res["access"]
        }, status=status.HTTP_201_CREATED)




class RefreshViewSet(viewsets.ViewSet, TokenRefreshView):
    permission_classes = (AllowAny,)
    http_method_names = ['post']

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)

        try:
            serializer.is_valid(raise_exception=True)
        except TokenError as e:
            raise InvalidToken(e.args[0])

        return Response(serializer.validated_data, status=status.HTTP_200_OK)



class ChangePasswordView(APIView):
    permission_classes = [IsAuthenticated, ]

    def post(self, request):
        serializer = PasswordChangeSerializer(context={'request': request}, data=request.data)
        serializer.is_valid(raise_exception=True) #Another way to write is as in Line 17
        request.user.set_password(serializer.validated_data['new_password'])
        request.user.save()
        return Response(status=status.HTTP_204_NO_CONTENT)
