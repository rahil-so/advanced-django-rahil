from django.db import models
from apps.users.models import User
from apps.core.models import BaseModel
from pathlib import Path
from uuid import uuid4

class Tag(BaseModel):
    name = models.CharField(max_length=100)
    def __str__(self):
        return self.name


class Article(BaseModel):
    title = models.CharField(max_length=100)
    body = models.TextField()
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    tags = models.ManyToManyField(Tag)
    is_published = models.BooleanField(default=False)

    def __str__(self):
        return self.title

def upload_to(instance, filename):
    extension = Path(filename).suffix
    filename = f"{uuid4()}{extension}"

    return f"uploads/%Y/%m/%d/{filename}"
class JobStatus(models.TextChoices):
    PENDING = 'pending', 'Pending'
    RUNNING = 'running', 'Running'
    SUCCESS = 'success', 'Success'
    FAILED = 'failed', 'Failed'

class UploadJob(BaseModel):
    upload_by = models.ForeignKey(User, on_delete=models.CASCADE)
    original_file_name = models.CharField(max_length=100)
    file = models.FileField(upload_to=upload_to)
    status = models.CharField(max_length=10, choices=JobStatus.choices, default=JobStatus.PENDING)
    total_rows = models.PositiveSmallIntegerField()
    processed_rows = models.PositiveSmallIntegerField()
    failed_rows = models.PositiveSmallIntegerField()
    error_message = models.TextField()

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f'UploadJob: {self.id}: {self.status}'

    @property
    def progress_percent(self):
        if self.total_rows == 0:
            return 0
        return self.processed_rows / self.total_rows




