import imp
from django.urls import reverse
from django.db import models
from django.template.defaultfilters import slugify 
from django.contrib.auth.models import (BaseUserManager, AbstractUser)

# Create your models here.

class Nivel(models.Model):
    nombre=models.CharField(max_length=50,null=False,unique=True)
    slug=models.SlugField(verbose_name="Indicador URL",null=False,unique=True)
    
    class Meta:
        ordering = ["id"]
        verbose_name = "nivel"
        verbose_name_plural = "niveles"
    
    def __str__(self):
        return self.nombre
    
    def get_absolute_url(self):
        return reverse("clase", kwargs={"slug": self.slug})
    
    def save(self, *args, **kwargs):
        self.slug = slugify(self.nombre)
        return super().save(*args, **kwargs)
    

class Clase(models.Model):
    def clase_directory_path(self, filename):
        #4 Se subira en MEDIA_ROOT/material/<id_nivel>/<nombre>/<filename>
        return f"material/{self.pk}/{self.titulo}/{filename}"
    
    titulo=models.CharField(verbose_name="Título",max_length=50,null=False,unique=True)
    p_general=models.TextField(verbose_name="Propósito general",null=True,blank=True)
    p_especifico=models.TextField(verbose_name="Propósito específico",null=True,blank=True)
    material=models.FileField(upload_to=clase_directory_path,default="",null=True,blank=True)
    video=models.FileField(upload_to=clase_directory_path,null=True,blank=True)
    
    nivel=models.ForeignKey(Nivel,models.CASCADE,related_name='clases',null=False)
    STATUS = [
        (False, "No disponible"),
        (True, "Disponible"),
    ]
    is_available=models.BooleanField(verbose_name="Disponibilidad",choices=STATUS,default=False)
    #3 video=models.CharField(max_length=250,null=True,blank=True)
    
    class Meta:
        ordering = ["id"]
        verbose_name = "clase"
        verbose_name_plural = "clases"
    
    def __str__(self):
        return self.titulo

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
    #4 DATA
    username=models.CharField(verbose_name="Usuario",max_length=25,unique=True)
    telefono=models.CharField(verbose_name="Teléfono",max_length=25,null=True,blank=True)
    fecha_registro=models.DateField(verbose_name="Fecha de registro",auto_now=True)
    
    #4 AULA
    niveles=models.ManyToManyField(Nivel,verbose_name="Niveles",related_name='usuarios',default="No asignado")
    clases_vistas=models.ManyToManyField(Clase,verbose_name="Clases vistas",related_name='usuarios',default="Ninguna",blank=True)
    
    #4 ADMINISTRATION
    is_active = models.BooleanField(default=True)
    is_admin = models.BooleanField(default=False)
    is_maestro = models.BooleanField(default=False)
    
    #4 STYLE
    TEMA = [
        ("light", "light"),
        ("dark", "dark"),
    ]
    tema = models.CharField(max_length=10,choices=TEMA,default="light")

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
 
