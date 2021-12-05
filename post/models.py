from django.contrib.auth import get_user_model
from django.db import models
from django.core.validators import MaxValueValidator, MinValueValidator

User = get_user_model()


class Post(models.Model):
    title = models.CharField(verbose_name='title', max_length=100)
    body = models.TextField(verbose_name='body')

    def __str__(self):
        return f'{self.title}'


class UserPostScore(models.Model):
    user = models.ForeignKey(User, verbose_name='user', related_name='scored_posts', on_delete=models.PROTECT)
    post = models.ForeignKey(Post, verbose_name='post', related_name='scores', on_delete=models.CASCADE)
    score = models.PositiveSmallIntegerField(verbose_name='score',
                                             validators=[MinValueValidator(0), MaxValueValidator(5)]
                                             )

    def __str__(self):
        return f'{self.user} >> {self.post} : ({self.score})'

    class Meta:
        unique_together = ('user', 'post')
