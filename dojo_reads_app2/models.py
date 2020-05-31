from django.db import models
import re


class UserManager(models.Manager):
    def user_validator(self, postData):
        errors = {}
        FN_REGEX = re.compile(r'^[a-zA-Z]+$')
        if not FN_REGEX.match(postData['name']):
            errors['name'] = "Only letters can be used in the Name field!"
        ALIAS_REGEX = re.compile(r'^[a-zA-Z]+$')
        if not ALIAS_REGEX.match(postData['alias']):
            errors['alias'] = "Only letters can be used in this field!"
        EMAIL_REGEX = re.compile(
            r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')
        if not EMAIL_REGEX.match(postData['email']):
            errors['email'] = "Invalid Email Address!"
        PW_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+$')
        if not PW_REGEX.match(postData['password']):
            errors['password'] = "Invalid characters!"
        if len(postData['name']) < 2:
            errors['name'] = "Name must be at least 2 characters long!"
        if len(postData['alias']) < 2:
            errors['alias'] = "Alias must be at least 2 characters long!"
        if len(postData['email']) < 2:
            errors['email'] = "Email address is required!"
        if len(postData['password']) < 8:
            errors['password'] = "Password must be at least 8 characters long!"
        return errors


class User(models.Model):
    fullname = models.CharField(max_length=45)
    alias = models.CharField(max_length=45)
    email = models.CharField(max_length=100)
    password = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    objects = UserManager()


class Book(models.Model):
    title = models.CharField(max_length=45)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


class Author(models.Model):
    books = models.ManyToManyField(Book, related_name="authors")
    fullname = models.CharField(max_length=100)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


class Review(models.Model):
    user = models.ForeignKey(
        User, related_name="reviews", on_delete=models.CASCADE)
    book = models.ForeignKey(
        Book, related_name="reviews", on_delete=models.CASCADE)
    content = models.CharField(max_length=255)
    rating = models.IntegerField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
