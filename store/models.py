from django.db                  import models, transaction

# Create your models here.
from django.contrib.auth.models import AbstractUser
from django.contrib.auth.models import BaseUserManager


# python manage.py dbshell <= pour accéder à la base de données liée au projet

class UserManager(BaseUserManager):
    """Define a model manager for User model with no username field."""

    use_in_migrations = True

    def _create_user(self, email, password, **extra_fields):
        """Create and save a User with the given email and password."""
        if not email:
            raise ValueError('The given email must be set')
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_user(self, email, password=None, **extra_fields):
        """Create and save a regular User with the given email and password."""
        extra_fields.setdefault('is_staff', False)
        extra_fields.setdefault('is_superuser', False)
        return self._create_user(email, password, **extra_fields)

    def create_superuser(self, email, password, **extra_fields):
        """Create and save a SuperUser with the given email and password."""
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')

        return self._create_user(email, password, **extra_fields)

class User(AbstractUser):
    
    email           = models.EmailField(verbose_name='email address', max_length=255, unique=True,) 
    username        = None
    enterprise      = models.CharField(max_length=400,default='')
    date_updated    = models.DateTimeField(auto_now=True)
    picture         = models.ImageField(default='')
    USERNAME_FIELD  = 'email'
    REQUIRED_FIELDS = []
    
    objects = UserManager()

    def __str__(self):
        return self.password

    def active_or_desactive_User(self):
        self.is_active = not self.is_active
        self.save()

        if self.is_active == False:
            self.commands.update(descriptionstatus ="user is desactive")
        else:
            self.commands.update(descriptionstatus ="user is active")

    """def changeUserPassword(self,newPassword):
        
        if newPassword:
            self.set_password(newPassword)
            self.save()
    """






class Categories(models.Model):
    name         = models.CharField(max_length=100, unique=True)
    description  = models.CharField(max_length=100,default='')
    date_created = models.DateTimeField(auto_now_add=True)
    date_updated = models.DateTimeField(auto_now=True)
    availablity  = models.BooleanField(default=True)
    picture      = models.ImageField(upload_to="pictureCategorieBackground") 

    class Meta:
        verbose_name = "categorie"

    def __str__(self):
        return self.name

    
    @transaction.atomic
    def able_or_disable(self):
        self.availablity = not self.availablity
        self.save()
        self.articles.update(availablity=not self.availablity)


class Series(models.Model):
    name         = models.CharField(max_length=10,default="")
    category     = models.ForeignKey(Categories, related_name="series", on_delete=models.CASCADE )
    date_created = models.DateTimeField(auto_now_add=True)
    date_updated = models.DateTimeField(auto_now=True)
    availablity  = models.BooleanField(default=True)



class Articles(models.Model):

    name                 = models.CharField(max_length=100,unique=True,primary_key=True)
    category             = models.ForeignKey(Categories, related_name="articles", on_delete=models.CASCADE )
    availablity          = models.BooleanField(default=True)
    description          = models.CharField(max_length=200,default='')
    content              = models.FileField(upload_to='contents/')#,default=''
    pictureOfDescription = models.ImageField(upload_to="pictureOfDescription/")#,default=''
    #filePrincipal        = models.FileField(upload_to='Article/',default=None)
    filePrincipal        = models.TextField(max_length=70000,default="")
    date_created         = models.DateTimeField(auto_now_add=True)
    date_updated         = models.DateTimeField(auto_now=True)
    serie                = models.ForeignKey(Series, related_name="articles", on_delete=models.CASCADE)
    users                = models.ManyToManyField(User, related_name="articles")

    
    class Meta:
        
        verbose_name = "article"
    
    def __str__(self):
        return self.name

    @transaction.atomic
    def able_or_disable(self):  
        self.availablity =not self.availablity
        self.save()


    @transaction.atomic
    def addUserToArticle(self,request,pk):  
        self.users.set(request.data.get("users"))
        self.save()

    @transaction.atomic
    def deleteUserToArticle(self,request,pk):  
        #if request.data.get("users") in self.users.all():
        self.users.remove(request.data.get("users"))
        self.save()

    



class Comments(models.Model):

    users          = models.ForeignKey(User, related_name="comments", on_delete=models.CASCADE )
    comments       = models.CharField(max_length=2000,default='')
    date_created   = models.DateTimeField(auto_now_add=True)
    date_updated   = models.DateTimeField(auto_now=True)
    availablity    = models.BooleanField(default=True)
    articles       = models.ForeignKey(Articles, related_name="comments", on_delete=models.CASCADE,default=None)
    typeNote       = models.BooleanField(default=False)
    isNoted        = models.BooleanField(default=False)


    class Meta: 
        verbose_name = "commentaires"

    def __str__(self):
        return self.name



    


    

class Pictures(models.Model):
    name         = models.CharField(max_length=100,default="")
    date_created = models.DateTimeField(auto_now_add=True)
    date_updated = models.DateTimeField(auto_now=True)
    picture      = models.ImageField(upload_to="articlesPictures") #
    article      = models.ForeignKey(Articles, related_name="pictures", on_delete=models.CASCADE )
    rank         = models.CharField(max_length=100,default="")

class Note(models.Model):
    articles       = models.ForeignKey(Articles, related_name="note", on_delete=models.CASCADE,default=None)
    likeGood       = models.BigIntegerField(default=0)
    likeBad        = models.BigIntegerField(default=0)
    numberVisited  = models.BigIntegerField(default=0)

