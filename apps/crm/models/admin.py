from django.contrib.auth.models import AbstractUser, Permission
from django.db import models
from django.utils.translation import gettext_lazy as _


# Define the Group model
class AdminGroup(models.Model):
    GROUP_CHOICES = [
        '北海道', '青森', '岩手', '宮城', '秋田', '山形', '福島', '茨城', 
        '栃木', '群馬', '埼玉', '千葉', '東京', '神奈川', '新潟', '富山', 
        '石川', '福井', '山梨', '長野', '岐阜', '静岡', '愛知', '三重', 
        '滋賀', '京都', '大阪', '兵庫', '奈良', '和歌山', '鳥取', '島根', 
        '岡山', '広島', '山口', '徳島', '香川', '愛媛', '高知', '福岡', 
        '佐賀', '長崎', '熊本', '大分', '宮崎', '鹿児島', '沖縄', '本部'
    ]
    PERMISSION_CHOICES = [
        ('branch', 'Branch'),
        ('head', 'Head')
    ]
    name = models.CharField(max_length=50, choices=[(choice, choice) for choice in GROUP_CHOICES], unique=True)
    permission = models.CharField(max_length=10, choices=PERMISSION_CHOICES)

    def __str__(self):
        return self.name

# Extend the default User model
class AdminUser(AbstractUser):
    groups = models.ManyToManyField(AdminGroup)
    user_permissions = models.ManyToManyField(
        Permission,
        verbose_name=_('user permissions'),
        blank=True,
        help_text=_('Specific permissions for this user.'),
        related_name="adminuser_set",  # Add this line
        related_query_name="adminuser",  # Add this line
    )

    def __str__(self):
        return self.username