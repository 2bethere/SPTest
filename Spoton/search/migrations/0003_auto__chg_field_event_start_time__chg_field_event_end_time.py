# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):

        # Changing field 'Event.start_time'
        db.alter_column(u'search_event', 'start_time', self.gf('django.db.models.fields.DateTimeField')(null=True))

        # Changing field 'Event.end_time'
        db.alter_column(u'search_event', 'end_time', self.gf('django.db.models.fields.DateTimeField')(null=True))

    def backwards(self, orm):

        # Changing field 'Event.start_time'
        db.alter_column(u'search_event', 'start_time', self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime(2014, 7, 31, 0, 0)))

        # Changing field 'Event.end_time'
        db.alter_column(u'search_event', 'end_time', self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime(2014, 7, 31, 0, 0)))

    models = {
        u'search.event': {
            'Meta': {'object_name': 'Event'},
            'end_time': ('django.db.models.fields.DateTimeField', [], {'default': 'None', 'null': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'site': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['search.Site']"}),
            'start_time': ('django.db.models.fields.DateTimeField', [], {'default': 'None', 'null': 'True', 'blank': 'True'}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '200'}),
            'url': ('django.db.models.fields.CharField', [], {'max_length': '2000'})
        },
        u'search.site': {
            'Meta': {'object_name': 'Site'},
            'domain': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'last_update': ('django.db.models.fields.DateTimeField', [], {})
        }
    }

    complete_apps = ['search']