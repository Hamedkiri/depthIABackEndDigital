from django.urls import re_path, include
from store.views import CategoriesView, UserView, ArticleView,  AdminCategoriesViewset,AdminUserViewset,AdminArticleViewset,ChangePasswordView,AdminCommentViewset,CommentViewset , AdminPictureViewset, PictureView , AdminSerieViewset, SeriesView
from rest_framework import routers #importation du module de routing
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

#from django.contrib.auth.views import LoginView


from store.views import LoginViewSet, RegistrationViewSet, RefreshViewSet

app_name="store"

router = routers.SimpleRouter()
#router = routers.DefaultRouter()

router.register('categories', CategoriesView, basename="categories")
router.register('users', UserView, basename='users')
router.register('articles', ArticleView, basename="articles")
router.register('pictures', PictureView, basename="pictures")
router.register('comments',CommentViewset,basename='comments')
router.register('series',SeriesView,basename="series")

router.register('admin/categories', AdminCategoriesViewset, basename='admin-categories')
router.register('admin/users', AdminUserViewset, basename='admin-categories')
router.register('admin/articles',AdminArticleViewset , basename='admin-articles')
router.register('admin/comments', AdminCommentViewset, basename='admin-comments')
router.register('admin/pictures', AdminPictureViewset, basename='admin-pictures')
router.register('admin/series',AdminSerieViewset,basename="admin-series")

router.register(r'auth/login', LoginViewSet, basename='auth-login')
router.register(r'auth/register', RegistrationViewSet, basename='auth-register')
router.register(r'auth/refresh', RefreshViewSet, basename='auth-refresh')


urlpatterns=[
    re_path(r'^api/',include(router.urls)),
    re_path(r'^api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    re_path(r'^api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    re_path(r'^api/accounts/change-password', ChangePasswordView.as_view(), name='register'),
    #re_path(r'^api/accounts/login', LoginView.as_view(), name='register'),
    #re_path(r'^api/accounts/logout', LogoutView.as_view(), name='register'),
]
