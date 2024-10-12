from django.contrib.auth.models import AbstractUser
from django.db import models
import qrcode
from io import BytesIO
from django.core.files.base import ContentFile

class Player(AbstractUser):
    points = models.IntegerField(default=0)
    qr_code = models.ImageField(upload_to='qr_codes/', blank=True)

    # Add unique related_name for groups and user_permissions
    groups = models.ManyToManyField(
        'auth.Group',
        related_name='player_set',  # Avoid conflict with auth.User
        blank=True
    )
    user_permissions = models.ManyToManyField(
        'auth.Permission',
        related_name='player_set_permissions',  # Avoid conflict with auth.User
        blank=True
    )

    def save(self, *args, **kwargs):
        # Call the parent class's save method to ensure the Player has an ID
        super().save(*args, **kwargs)

        # Generate the QR code
        qr_content = f'player-{self.id}'  # Content for the QR code
        qr = qrcode.make(qr_content)  # Generate QR code

        # Save the QR code as an image in memory
        qr_io = BytesIO()
        qr.save(qr_io, format='PNG')  # Save QR code as PNG in memory

        # Create a Django File object and assign it to qr_code field
        qr_file = ContentFile(qr_io.getvalue(), name=f'{self.username}_qr.png')

        # Save the generated QR code to the qr_code field
        self.qr_code.save(f'{self.username}_qr.png', qr_file, save=False)

        # Save the model again to update the qr_code field
        super().save(*args, **kwargs)
