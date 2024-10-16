from django.contrib.auth.models import AbstractUser
from django.db import models
import qrcode
from io import BytesIO
from django.core.files.base import ContentFile

class Player(AbstractUser):
    points = models.IntegerField(default=0)
    qr_code = models.ImageField(upload_to='qr_codes/', blank=True)

    # Explicitly set related_name to avoid clashes
    groups = models.ManyToManyField(
        'auth.Group',
        verbose_name='groups',
        blank=True,
        help_text='The groups this user belongs to. A user will get all permissions granted to each of their groups.',
        related_name='player_set',
        related_query_name='player',
    )
    user_permissions = models.ManyToManyField(
        'auth.Permission',
        verbose_name='user permissions',
        blank=True,
        help_text='Specific permissions for this user.',
        related_name='player_set',
        related_query_name='player',
    )

    def generate_qr_code(self):
        if not self.qr_code:
            qr_content = f'player-{self.id}'
            qr = qrcode.make(qr_content)
            qr_io = BytesIO()
            qr.save(qr_io, format='PNG')
            qr_file = ContentFile(qr_io.getvalue(), name=f'{self.username}_qr.png')
            self.qr_code.save(f'{self.username}_qr.png', qr_file, save=False)
            self.save()

    def save(self, *args, **kwargs):
        is_new = self.pk is None
        super().save(*args, **kwargs)
        if is_new:
            self.generate_qr_code()