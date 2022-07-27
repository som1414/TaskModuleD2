from django.db import models
from django.contrib.auth.models import User
from django.db.models import Sum


class Author(models.Model):
    authUser = models.OneToOneField(User, on_delete=models.CASCADE)
    ratingAuth = models.SmallIntegerField(default=0)

    def update_rating(self):
        postRating = self.post_set.all().aggregate(postRat=Sum('rating'))
        pRat = 0
        pRat += postRating.get('postRat')

        commentRating = self.authUser.comment_set.all().aggregate(commentRat=Sum('rating'))
        cRat = 0
        cRat += commentRating.get('commentRat')

        self.ratingAuth = pRat * 3 + cRat
        self.save()


class Category(models.Model):
    designation = models.CharField(max_length=64, unique=True)


class Post(models.Model):
    author = models.ForeignKey(Author, on_delete=models.CASCADE)
    NEWS = 'NW'
    ARTICLE = 'AR'
    CATEGORY_CHOICES = [
        (NEWS, 'Новость'),
        (ARTICLE, 'Статья'),
    ]
    categorySort = models.CharField(max_length=2, choices=CATEGORY_CHOICES, default=NEWS)
    dateCreation = models.DateTimeField(auto_now_add=True)
    title = models.CharField(max_length=128)
    text = models.TextField()
    rating = models.SmallIntegerField(default=0)
    postCategory = models.ManyToManyField(Category, through='PostCategory')

    def like(self):
        self.rating += 1
        self.save()

    def dislike(self):
        self.rating -= 1
        self.save()

    def preview(self):
        return self.text[0:124] + '...'


class PostCategory(models.Model):
    postThrough = models.ForeignKey(Post, on_delete=models.CASCADE)
    categoryThrough = models.ForeignKey(Category, on_delete=models.CASCADE)


class Comment(models.Model):
    commentPost = models.ForeignKey(Post, on_delete=models.CASCADE)
    commentUser = models.ForeignKey(User, on_delete=models.CASCADE)
    dateCreation = models.DateTimeField(auto_now_add=True)
    text = models.TextField()
    rating = models.SmallIntegerField(default=0)

    def __str__(self):
        return self.commentUser.username

    def like(self):
        self.rating += 1
        self.save()

    def dislike(self):
        self.rating -= 1
        self.save()
