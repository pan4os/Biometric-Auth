from django.db import models
from django.contrib.auth.models import User, UserManager
from django.db.models.signals import post_save
from django.dispatch import receiver
from .iris_auth.enroll_single import enroll_single

#----------------------------- Общие классы
class UserBiometry(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    iris_photo_counter = models.PositiveSmallIntegerField(default=0)
    face_photo_counter = models.PositiveSmallIntegerField(default=0)
    fingerprint_photo_counter = models.PositiveSmallIntegerField(default=0)

    def change_iris_photo_counter(self, increase=True):
        if increase:
            self.iris_photo_counter += 1
        else:
            self.iris_photo_counter -= 1
    def change_face_photo_counter(self,increase=True):
        if increase:
            self.face_photo_counter += 1
        else:
            self.face_photo_counter -= 1    

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


def face_directory_path(instance, filename):

     return 'biometric_data/user_{0}/face/{1}'.format(instance.user.id, filename)

# --------------------------- Модели для алгоритмов:
def iris_directory_path(instance, filename):
    # file will be uploaded to MEDIA_ROOT/user_<id>/<filename>
    return 'biometric_data/user_{0}/iris/{1}'.format(instance.user.id, filename)

class IrisImages(models.Model):
    user = models.ForeignKey(UserBiometry, on_delete=models.CASCADE,related_name='iris_image')
    iris_image = models.ImageField(upload_to=iris_directory_path)

    def save(self, *args, **kwargs):
        # ---------- Second realisation
        super().save(*args, **kwargs)
        enroll_single(image = self.iris_image, user_id = self.user.id)


class FaceImages(models.Model):
    user = models.ForeignKey(UserBiometry, on_delete=models.CASCADE,related_name='face_image')
    face_image = models.ImageField(upload_to=face_directory_path)
    def save(self, *args, **kwargs):
        # ---------- Second realisation
        super().save(*args, **kwargs)
        

class FingerPrintImages(models.Model):
    pass


