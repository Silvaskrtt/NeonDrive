from django.db import models

class Client(models.Model):

    name = models.CharField(max_length=100)
    cpf = models.CharField(max_length=14, unique=True)
    email = models.EmailField()
    phone = models.CharField(max_length=20)

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name