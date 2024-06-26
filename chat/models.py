from django.db import models
from accounts.models import User

# Create your models here.


class Connection(models.Model):
    sender = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="sent_connections"
    )
    receiver = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="received_connections"
    )
    accepted = models.BooleanField(default=False)
    updated = models.DateField(auto_now=True)
    created = models.DateField(auto_now_add=True)

    def __str__(self):
        return self.sender.username + "-->" + self.receiver.username


class Message(models.Model):
    connection = models.ForeignKey(
        Connection, on_delete=models.CASCADE, related_name="messages"
    )
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="my_messages")
    text = models.TextField()
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.user.username + ": " + self.text
