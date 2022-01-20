from django.db import models
import random
import string

# Create your models here.

class Graph(models.Model):
    def __init__(self):
        pass

    def generateGraph(self):
        return ''.join(random.choices(string.ascii_letters + string.digits, k=16))