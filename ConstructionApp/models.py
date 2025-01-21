from django.db import models

# Create your models here.
from django.contrib.auth.models import User

#client model
class Client(models.Model):
    profile_picture = models.ImageField(
         upload_to='profile_pics/',  # Directory where images will be saved
         default='profile_pics/default.jpg',  # Default image if none is provided
         blank=True,  # Allows blank entries
         null=True    # Allows null values in the database
     )
    name = models.CharField(max_length=255)
    email = models.EmailField(unique=True)
    phone = models.CharField(max_length=15, null=True, blank=True)
    address = models.TextField(null=True, blank=True)
    message = models.TextField(null=True, blank=True)
    def __str__(self):
        return self.name

# 2. Service Model
class Service(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField(null=True, blank=True)
    image = models.ImageField(upload_to='services/', null=True, blank=True)

    def __str__(self):
        return self.name

class Project(models.Model):
    STATUS_CHOICES = [
        ('PLANNED', 'Planned'),
        ('IN_PROGRESS', 'In Progress'),
        ('COMPLETED', 'Completed'),
    ]
    title = models.CharField(max_length=255)
    description = models.TextField()
    start_date = models.DateField()
    end_date = models.DateField(null=True, blank=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='PLANNED')
    budget = models.DecimalField(max_digits=12, decimal_places=2)
    client = models.ForeignKey(Client, related_name='projects', on_delete=models.CASCADE)
    services = models.ManyToManyField(Service, related_name='projects')

    def _str_(self):
        return f"{self.title} ({self.status})"

class ProjectImage(models.Model):
    project = models.ForeignKey(Project, related_name='images', on_delete=models.CASCADE)
    image = models.ImageField(upload_to='project_images/')
    caption = models.CharField(max_length=255, null=True, blank=True)

    def _str_(self):
        return f"Image for {self.project.title}"

class ProjectVideo(models.Model):
    project = models.ForeignKey(Project, related_name='videos', on_delete=models.CASCADE)
    video = models.FileField(upload_to='project_videos/')
    caption = models.CharField(max_length=255, null=True, blank=True)

    def _str_(self):
        return f"Video for {self.project.title}"

# 6. Review Model
class Review(models.Model):
    client = models.ForeignKey(Client, related_name='reviews', on_delete=models.CASCADE)
    review_text = models.TextField()
    rating = models.PositiveSmallIntegerField()
    date_submitted = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Review by {self.client.name} - {self.rating} Stars"


class Profile(models.Model):
    USER_ROLES = [
        ('ADMIN', 'Admin'),
        ('CLIENT', 'Client'),
    ]
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    role = models.CharField(max_length=10, choices=USER_ROLES, default='CLIENT')

    def __str__(self):
        return f"{self.user.username} - {self.role}"

