from django.db import models
from django.contrib.auth.models import (BaseUserManager, AbstractUser)

# Create your models here.

class Clase(models.Model):
    # def clase_directory_path(self, filename):
        # Se subira en MEDIA_ROOT / video/<id_nivel>/<filename>
        # return f'videos/{self.codigo}/({self.nombre})-{filename}'
    
    #video=models.FileField(upload_to=clase_directory_path,null=True,blank=True)
    codigo=models.CharField(max_length=50,unique=True)
    nombre=models.CharField(max_length=50)
    video=models.CharField(max_length=250,null=True,blank=True)
    
    class Meta:
        ordering = ["id"]
        verbose_name = "clase"
        verbose_name_plural = "clases"
    
    def __str__(self):
        return self.nombre

class Nivel(models.Model):
    nombre=models.CharField(max_length=50)
    clases=models.ManyToManyField(Clase,verbose_name="Clases",default="Ninguna",blank=True)
    
    class Meta:
        ordering = ["id"]
        verbose_name = "nivel"
        verbose_name_plural = "niveles"
    
    def __str__(self):
        return self.nombre

class UsuarioManager(BaseUserManager):
    def create_user(self, username, email, password=None):
        """
        Creates and saves a User with the given username, email and password.
        """
        if not username:
            raise ValueError('Users must have an username address')

        user = self.model(
            username=username,
            email=self.normalize_email(email),
        )

        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, username, email, password=None):
        """
        Creates and saves a superuser with the given username, email and password.
        """
        user = self.create_user(
            username,
            password=password,
            email=email,
        )
        user.is_admin = True
        user.save(using=self._db)
        return user

class Usuario(AbstractUser):
     
    username=models.CharField(verbose_name="Usuario",max_length=25,unique=True)
    telefono=models.CharField(verbose_name="Teléfono",max_length=25,null=True,blank=True)
    direccion=models.TextField(verbose_name="Dirección",max_length=500,null=True,blank=True)
    niveles=models.ManyToManyField(Nivel,verbose_name="Niveles")
    fecha_registro=models.DateField(verbose_name="Fecha de registro",auto_now=True)
    
    clases_vistas=models.ManyToManyField(Clase,verbose_name="Clases vistas",default="Ninguna",blank=True)

    is_active = models.BooleanField(default=True)
    is_admin = models.BooleanField(default=False)
    is_maestro = models.BooleanField(default=False)

    objects = UsuarioManager()

    EMAIL_FIELD = "email"
    USERNAME_FIELD = "username"
    REQUIRED_FIELDS = ["email"]

    class Meta:
        ordering = ["id"]
        verbose_name = "usuario"
        verbose_name_plural = "usuarios"
    
    def __str__(self):
        if self.first_name and self.last_name:
            texto = "{0} {1} ({2})"
            return texto.format(self.first_name, self.last_name, self.username)
        else:
            return self.username

    def has_perm(self, perm, obj=None):
        "Does the user have a specific permission?"
        # Simplest possible answer: Yes, always
        return True

    def has_module_perms(self, app_label):
        "Does the user have permissions to view the app `app_label`?"
        # Simplest possible answer: Yes, always
        return True

    @property
    def is_staff(self):
        "Is the user a member of staff?"
        # Simplest possible answer: All admins are staff
        return self.is_admin
 
