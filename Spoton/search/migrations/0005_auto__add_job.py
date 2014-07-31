# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'Job'
        db.create_table(u'search_job', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('site', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['search.Site'])),
            ('start_url', self.gf('django.db.models.fields.CharField')(max_length=2000)),
            ('pagelimit', self.gf('django.db.models.fields.IntegerField')(default=100)),
        ))
        db.send_create_signal(u'search', ['Job'])


    def backwards(self, orm):
        # Deleting model 'Job'
        db.delete_table(u'search_job')


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
        u'search.job': {
            'Meta': {'object_name': 'Job'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'pagelimit': ('django.db.models.fields.IntegerField', [], {'default': '100'}),
            'site': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['search.Site']"}),
            'start_url': ('django.db.models.fields.CharField', [], {'max_length': '2000'})
        },
        u'search.site': {
            'Meta': {'object_name': 'Site'},
            'domain': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'last_update': ('django.db.models.fields.DateTimeField', [], {})
        }
    }

    complete_apps = ['search']