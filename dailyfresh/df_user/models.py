#coding=utf-8
from __future__ import unicode_literals

from django.db import models


class UserInfo(models.Model):
    uname = models.CharField(max_length=20)
    upwd = models.CharField(max_length=40)
    uemail = models.CharField(max_length=30)
    ushow = models.CharField(max_length=20, default='')
    uaddress = models.CharField(max_length=100, default='')
    upostid = models.CharField(max_length=6, default='')
    uphone = models.CharField(max_length=11, default='')

    #default和black 是python 层面的约束，不影响数据库表结构

