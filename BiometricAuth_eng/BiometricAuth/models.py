from django.db import models
from django.contrib.auth.models import User, UserManager
from .mixins import AbstractUUID
from django.db.models.signals import post_save
from django.dispatch import receiver
from .iris_auth.enroll_single import enroll_single
from django.utils.text import get_valid_filename
from django.conf import settings
from PIL import Image


class UserBiometry(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    iris_photo_counter = models.PositiveSmallIntegerField(default=0)


    def change_iris_photo_counter(self, increase=True):
        if increase:
            self.iris_photo_counter += 1
        else:
            self.iris_photo_counter -= 1
        

    def __str__(self):
        return 'user - {0}'.format(self.user)

# Автоматическое создание/изменение модели UserBiometry при создании/изменении модели пользователя
@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        UserBiometry.objects.create(user=instance)

@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    instance.userbiometry.save()



def iris_directory_path(instance, filename):
    # file will be uploaded to MEDIA_ROOT/user_<id>/<filename>
    return 'biometric_data/user_{0}/iris/{1}'.format(instance.user.id, filename)

class IrisImages(models.Model):
    user = models.ForeignKey(UserBiometry, on_delete=models.CASCADE,related_name='iris_image')
    iris_image = models.ImageField(upload_to=iris_directory_path)

    def save(self, *args, **kwargs):
        # valid_image_name = get_valid_filename(self.iris_image.file)

        # img = Image.open(self.iris_image)
        # print('Image: ', img)
        # print('\t path: ', self.iris_image.path)
        # print('\t name: ', self.iris_image.name)
        

        #----------- FIRST REALISATION
        super().save(*args, **kwargs)
        print('\tFile name from model: ', self.iris_image.name)
        print('\tFile path from model: ', self.iris_image.path) 
        print('\tFile url from model: ', self.iris_image.url) 
        print('\tAttributes of file: ', dir(self.iris_image))
        enroll_single(self.iris_image.path) 
       

        # super().save(*args, **kwargs)
        # enroll_single(iris_directory_path(self,self.iris_image),self.iris_image.path)
        # if self.iris_image:
        #     self.iris_image = 

# --------------------------- Модели для алгоритмов распознавания лица и отпечатка пальца

class FaceImages(models.Model):
    pass

class FingerPrintImages(models.Model):
    pass


