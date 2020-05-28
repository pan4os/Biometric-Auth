from django.db import models
from django.contrib.auth.models import User, UserManager
from .mixins import AbstractUUID
from django.db.models.signals import post_save
from django.dispatch import receiver

# def content_file_name(instance, filename):
#     timestr = time.strftime("%Y%m%d-%H%M%S")
#     name, extension = os.path.splitext(filename)
#     return os.path.join('biometric_data', instance.user.username, timestr + extension)

def iris_directory_path(instance, filename):
    # file will be uploaded to MEDIA_ROOT/user_<id>/<filename>
    return 'biometric_data/user_{0}/iris/{1}'.format(instance.user.id, filename)

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

class IrisImages(models.Model):
    user = models.ForeignKey(UserBiometry, on_delete=models.CASCADE,related_name='iris_image')
    iris_image = models.ImageField(upload_to=iris_directory_path)

# --------------------------- Модели для алгоритмов распознавания лица и отпечатка пальца

class FaceImages(models.Model):
    pass

class FingerPrintImages(models.Model):
    pass


