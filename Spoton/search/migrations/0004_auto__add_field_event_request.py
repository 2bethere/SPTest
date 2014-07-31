# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding field 'Event.request'
        db.add_column(u'search_event', 'request',
                      self.gf('django.db.models.fields.CharField')(default='', max_length=2000),
                      keep_default=False)


    def backwards(self, orm):
        # Deleting field 'Event.request'
        db.delete_column(u'search_event', 'request')


    models = {
        u'search.event': {
            'Meta': {'object_name': 'Event'},
            'end_time': ('django.db.models.fields.DateTimeField', [], {'default': 'None', 'null': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'request': ('django.db.models.fields.CharField', [], {'max_length': '2000'}),
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