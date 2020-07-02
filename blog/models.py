from django.db import models
from django.shortcuts import reverse

from django.utils.text import slugify
from time import time

def get_slug(s):
    new_slug = slugify(s, allow_unicode = True)
    return new_slug + '-' + str(int(time()))

class Post(models.Model):
    title = models.CharField(max_length = 150, db_index = True) #Для быстрого поиска
    #slug = models.SlugField(max_length = 150, unique = True) #unique = True автоматом индексируются
    slug = models.SlugField(max_length=150, blank = True, unique=True)
    content = models.TextField(blank = True, db_index = True) #Поле может быть пустым
    # blank = True - не у всех постов могут быть теги
    # related_name = 'posts' - свойство появится у экземпляров класса Tag
    # related_name = 'post_set' - django создаёт автоматически, если бы мы не указали posts
    tags = models.ManyToManyField('Tag', blank = True, related_name = 'posts')
    date_pub = models.DateTimeField(auto_now_add = True) #auto_now_add = True в момент сохранения в базе данных

    #Переопределяем метод save(), чтобы добавлять slug автоматически при создании поста
    def save(self, *args, **kwargs):
        if not self.id: #Если пост не сохранён в базу, у него нет id
            self.slug = get_slug(self.title)
            super().save(*args, **kwargs) #передаю в суперкласс Model позиционные и именованные аргументы


    #Возвращает ссылку на конкретный объект, экземпляр класса Post
    #reverse и url одно и то же. Просто reverse используется в .py-файлах, url - используется
    #в шаблонах
    def get_absolute_url(self):
        return reverse('post_detail_url', kwargs={'slug': self.slug})

    def get_update_url(self):
        return reverse('post_update_url', kwargs={'slug': self.slug})

    def get_delete_url(self):
        return reverse('post_delete_url', kwargs={'slug': self.slug})

    def __str__(self):
        return self.title


class Tag(models.Model):
    title = models.CharField(max_length = 50)
    slug = models.SlugField(max_length = 50, unique = True)

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('tag_detail_url', kwargs={'slug': self.slug})

    def get_update_url(self):
        return reverse('tag_update_url', kwargs={'slug': self.slug})

    def get_delete_url(self):
        return reverse('tag_delete_url', kwargs={'slug': self.slug})