# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'Person'
        db.create_table(u'core_person', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('password', self.gf('django.db.models.fields.CharField')(max_length=128)),
            ('last_login', self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime.now)),
            ('is_superuser', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('username', self.gf('django.db.models.fields.CharField')(unique=True, max_length=30)),
            ('first_name', self.gf('django.db.models.fields.CharField')(max_length=30, blank=True)),
            ('last_name', self.gf('django.db.models.fields.CharField')(max_length=30, blank=True)),
            ('email', self.gf('django.db.models.fields.EmailField')(max_length=75, blank=True)),
            ('is_staff', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('is_active', self.gf('django.db.models.fields.BooleanField')(default=True)),
            ('date_joined', self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime.now)),
            ('address', self.gf('django.db.models.fields.CharField')(max_length=100, null=True, blank=True)),
            ('number', self.gf('django.db.models.fields.IntegerField')(null=True, blank=True)),
            ('district', self.gf('django.db.models.fields.CharField')(max_length=100, null=True, blank=True)),
            ('city', self.gf('django.db.models.fields.CharField')(max_length=100, null=True, blank=True)),
            ('state', self.gf('django.db.models.fields.CharField')(max_length=2, null=True, blank=True)),
            ('country', self.gf('django.db.models.fields.CharField')(max_length=60, null=True, blank=True)),
            ('zipcode', self.gf('django.db.models.fields.CharField')(max_length=10, null=True, blank=True)),
            ('language', self.gf('django.db.models.fields.CharField')(max_length=10, null=True, blank=True)),
            ('avatar', self.gf('cloudinary.models.CloudinaryField')(default='avatar.jpg', max_length=100, null=True)),
            ('facebook_link', self.gf('django.db.models.fields.CharField')(max_length=100, null=True, blank=True)),
            ('twitter_link', self.gf('django.db.models.fields.CharField')(max_length=100, null=True, blank=True)),
            ('gplus_link', self.gf('django.db.models.fields.CharField')(max_length=100, null=True, blank=True)),
            ('notification1', self.gf('django.db.models.fields.BooleanField')(default=True)),
            ('notification2', self.gf('django.db.models.fields.BooleanField')(default=True)),
            ('notification3', self.gf('django.db.models.fields.BooleanField')(default=True)),
            ('notification4', self.gf('django.db.models.fields.BooleanField')(default=True)),
            ('validation', self.gf('django.db.models.fields.BooleanField')(default=False)),
        ))
        db.send_create_signal(u'core', ['Person'])

        # Adding M2M table for field groups on 'Person'
        m2m_table_name = db.shorten_name(u'core_person_groups')
        db.create_table(m2m_table_name, (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('person', models.ForeignKey(orm[u'core.person'], null=False)),
            ('group', models.ForeignKey(orm[u'auth.group'], null=False))
        ))
        db.create_unique(m2m_table_name, ['person_id', 'group_id'])

        # Adding M2M table for field user_permissions on 'Person'
        m2m_table_name = db.shorten_name(u'core_person_user_permissions')
        db.create_table(m2m_table_name, (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('person', models.ForeignKey(orm[u'core.person'], null=False)),
            ('permission', models.ForeignKey(orm[u'auth.permission'], null=False))
        ))
        db.create_unique(m2m_table_name, ['person_id', 'permission_id'])

        # Adding model 'Contact'
        db.create_table(u'core_contact', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('full_name', self.gf('django.db.models.fields.CharField')(max_length=100)),
            ('email', self.gf('django.db.models.fields.EmailField')(max_length=75)),
            ('phone', self.gf('django.db.models.fields.CharField')(max_length=20, blank=True)),
            ('message', self.gf('django.db.models.fields.TextField')(max_length=500)),
        ))
        db.send_create_signal(u'core', ['Contact'])


    def backwards(self, orm):
        # Deleting model 'Person'
        db.delete_table(u'core_person')

        # Removing M2M table for field groups on 'Person'
        db.delete_table(db.shorten_name(u'core_person_groups'))

        # Removing M2M table for field user_permissions on 'Person'
        db.delete_table(db.shorten_name(u'core_person_user_permissions'))

        # Deleting model 'Contact'
        db.delete_table(u'core_contact')


    models = {
        u'auth.group': {
            'Meta': {'object_name': 'Group'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '80'}),
            'permissions': ('django.db.models.fields.related.ManyToManyField', [], {'to': u"orm['auth.Permission']", 'symmetrical': 'False', 'blank': 'True'})
        },
        u'auth.permission': {
            'Meta': {'ordering': "(u'content_type__app_label', u'content_type__model', u'codename')", 'unique_together': "((u'content_type', u'codename'),)", 'object_name': 'Permission'},
            'codename': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'content_type': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['contenttypes.ContentType']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '50'})
        },
        u'contenttypes.contenttype': {
            'Meta': {'ordering': "('name',)", 'unique_together': "(('app_label', 'model'),)", 'object_name': 'ContentType', 'db_table': "'django_content_type'"},
            'app_label': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'model': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'})
        },
        u'core.contact': {
            'Meta': {'object_name': 'Contact'},
            'email': ('django.db.models.fields.EmailField', [], {'max_length': '75'}),
            'full_name': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'message': ('django.db.models.fields.TextField', [], {'max_length': '500'}),
            'phone': ('django.db.models.fields.CharField', [], {'max_length': '20', 'blank': 'True'})
        },
        u'core.person': {
            'Meta': {'ordering': "['email']", 'object_name': 'Person'},
            'address': ('django.db.models.fields.CharField', [], {'max_length': '100', 'null': 'True', 'blank': 'True'}),
            'avatar': ('cloudinary.models.CloudinaryField', [], {'default': "'avatar.jpg'", 'max_length': '100', 'null': 'True'}),
            'city': ('django.db.models.fields.CharField', [], {'max_length': '100', 'null': 'True', 'blank': 'True'}),
            'country': ('django.db.models.fields.CharField', [], {'max_length': '60', 'null': 'True', 'blank': 'True'}),
            'date_joined': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'district': ('django.db.models.fields.CharField', [], {'max_length': '100', 'null': 'True', 'blank': 'True'}),
            'email': ('django.db.models.fields.EmailField', [], {'max_length': '75', 'blank': 'True'}),
            'facebook_link': ('django.db.models.fields.CharField', [], {'max_length': '100', 'null': 'True', 'blank': 'True'}),
            'first_name': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
            'gplus_link': ('django.db.models.fields.CharField', [], {'max_length': '100', 'null': 'True', 'blank': 'True'}),
            'groups': ('django.db.models.fields.related.ManyToManyField', [], {'symmetrical': 'False', 'related_name': "u'user_set'", 'blank': 'True', 'to': u"orm['auth.Group']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_active': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'is_staff': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'is_superuser': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'language': ('django.db.models.fields.CharField', [], {'max_length': '10', 'null': 'True', 'blank': 'True'}),
            'last_login': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'last_name': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
            'notification1': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'notification2': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'notification3': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'notification4': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'number': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'password': ('django.db.models.fields.CharField', [], {'max_length': '128'}),
            'state': ('django.db.models.fields.CharField', [], {'max_length': '2', 'null': 'True', 'blank': 'True'}),
            'twitter_link': ('django.db.models.fields.CharField', [], {'max_length': '100', 'null': 'True', 'blank': 'True'}),
            'user_permissions': ('django.db.models.fields.related.ManyToManyField', [], {'symmetrical': 'False', 'related_name': "u'user_set'", 'blank': 'True', 'to': u"orm['auth.Permission']"}),
            'username': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '30'}),
            'validation': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'zipcode': ('django.db.models.fields.CharField', [], {'max_length': '10', 'null': 'True', 'blank': 'True'})
        }
    }

    complete_apps = ['core']