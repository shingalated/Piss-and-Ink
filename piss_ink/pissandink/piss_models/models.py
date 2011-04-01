# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#     * Rearrange models' order
#     * Make sure each model has one field with primary_key=True
# Feel free to rename the models, but don't rename db_table values or field names.
#
# Also note: You'll have to insert the output of 'django-admin.py sqlcustom [appname]'
# into your database.

from django.db import models

class Bookmarks(models.Model):
    bookmark_id = models.IntegerField(primary_key=True)
    bookmark1 = models.CharField(max_length=135, blank=True)
    bookmark2 = models.CharField(max_length=135, blank=True)
    bookmark3 = models.CharField(max_length=135, blank=True)
    class Meta:
        db_table = u'bookmarks'
        def __unicode__(self):
			return self.bookmark_id

class rss(models.Model):
    rss_id = models.IntegerField(primary_key=True)
    rss1 = models.CharField(max_length=240, blank=True)
    rss2 = models.CharField(max_length=240, blank=True)
    rss3 = models.CharField(max_length=240, blank=True)
    rss4 = models.CharField(max_length=240, blank=True)
    class Meta:
        db_table = u'rss'
        def __unicode__(self):
			return self.rss_id

class Config(models.Model):
    config_id = models.IntegerField(primary_key=True)
    weather = models.IntegerField(null=True, blank=True)
    google_id = models.CharField(max_length=90, blank=True)
    google_pass = models.CharField(max_length=135, blank=True)
    google_cal_name = models.CharField(max_length=135, blank=True)
    rss = models.ForeignKey(rss)
    configcol = models.CharField(max_length=135, blank=True)
    bookmark = models.ForeignKey(Bookmarks)
    class Meta:
        db_table = u'config'
        def __unicode__(self):
			return self.config

class Event(models.Model):
    event_id = models.IntegerField(primary_key=True)
    title = models.CharField(max_length=75, blank=True)
    time = models.DateTimeField(blank=True) # This field type is a guess.
    date = models.DateField(null=True, blank=True)
    class Meta:
        db_table = u'event'
    def __unicode__(self):
		return self.title
	


class System(models.Model):
    time_zone = models.CharField(max_length=30)
    language = models.CharField(max_length=135, blank=True)
    pissandink_name = models.CharField(max_length=135, blank=True)
    class Meta:
        db_table = u'system'

class Tasks(models.Model):
    task_id = models.IntegerField(primary_key=True)
    title = models.CharField(max_length=75, blank=True)
    time = models.TextField(blank=True) # This field type is a guess.
    date = models.DateField(null=True, blank=True)
    event_status = models.CharField(max_length=135, blank=True)
    class Meta:
        db_table = u'tasks'

class User(models.Model):
    user_id = models.IntegerField(primary_key=True)
    event = models.ManyToManyField(Event)
    first_name = models.CharField(max_length=105)
    last_name = models.CharField(max_length=105)
    zip_code = models.CharField(max_length=45, blank=True)
    avatar = models.TextField(blank=True)
    fk_config = models.ForeignKey(Config)
    status = models.CharField(max_length=135, blank=True)
    passwd = models.CharField(max_length=102, blank=True)
    user_name = models.CharField(max_length=102, blank=True)
    class Meta:
        db_table = u'user'
        def __unicode__(self):
			return self.first_name
        

class UserEvent(models.Model):
    user = models.ForeignKey(User)
    event = models.ForeignKey(Event)
    class Meta:
        db_table = u'user_event'


class UserTasks(models.Model):
    user = models.ForeignKey(User)
    tasks = models.ForeignKey(Tasks)
    class Meta:
        db_table = u'user_tasks'


