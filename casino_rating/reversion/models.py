"""Database models used by django-reversion."""

import warnings

from django.contrib.auth.models import User
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes import generic
from django.core import serializers
from django.conf import settings
from django.db import models, IntegrityError
from django.utils import simplejson
from django.utils.translation import ugettext as _


def deprecated(original, replacement):
    """Decorator that defines a deprecated method."""
    def decorator(func):
        if not settings.DEBUG:
            return func
        def do_pending_deprication(*args, **kwargs):
            warnings.warn(
                "%s is deprecated, and will be removed in django-reversion 1.7. Use %s instead" % (original, replacement),
                PendingDeprecationWarning,
            )
            return func(*args, **kwargs)
        return do_pending_deprication
    return decorator


class RevertError(Exception):    
    """Exception thrown when something goes wrong with reverting a model."""


REVISION_TYPE_CHOICES = ((1, _("Initial")), (4, _("Previous")), (5, _("Current")), (2, _("Discard")), 
    (3, _("Accept")))
REVISION_INITIAL = 1
REVISION_DISCARD = 2
REVISION_ACCEPT = 3
REVISION_PREVIOUS = 4
REVISION_CURRENT = 5


class Revision(models.Model):
    """A group of related object versions."""
    content_type = models.ForeignKey(ContentType, help_text="Content type of the model under version control.", null=True)
    object_repr = models.TextField(help_text="A string representation of the object.", null=True)
    changes = models.TextField(help_text="Revision changes")
    manager_slug = models.CharField(max_length=200, db_index=True, default="default")
    date_created = models.DateTimeField(auto_now_add=True, help_text="The date and time this revision was created.")
    user = models.ForeignKey(User, blank=True, null=True, help_text="The user who created this revision.")
    comment = models.TextField(blank=True, help_text="A text comment on this revision.")
    type = models.PositiveSmallIntegerField(choices=REVISION_TYPE_CHOICES, db_index=True, default=1)

    def get_changes(self):
        """
        Get list of revision changes
        """
        if not self.changes:
            return None

        def get_choices_title(choices, value):
            for item in choices:
                if int(value) == item[0]:
                    return item[1]
            return ""
        
        changes = simplejson.loads(self.changes)
        _cont_types = {}
        result = []
        for key in changes.keys():
            item = {}
            content_type_id, obj_id = key.split("-")
            if not _cont_types.has_key(content_type_id):
                _cont_types[content_type_id] = ContentType.objects.get_for_id(content_type_id).model_class()
            
            if changes[key].get("type", None) == "delete":
                item = changes[key]
            else:
                obj = _cont_types[content_type_id].objects.get(pk=obj_id)
                item = {"title" : "%s %s" % (obj._meta.verbose_name, unicode(obj)), "type" : None}
                if changes[key].has_key("type"):
                    item["type"] = changes[key]["type"]

                f = changes[key]["fields"]
                fields = []
                for fkey in f.keys():
                    if "id" == fkey:
                        continue
                    
                    field = obj._meta.get_field_by_name(fkey)[0]
                    values = {"title" : field.verbose_name}
                    if item["type"]:
                        f[fkey] = {"old" : None,  "new" : f[fkey]}

                    values.update({"old" : f[fkey]["old"], "new" : f[fkey]["new"]})
                    
                    if field.choices:
                        if f[fkey]["old"] is not None:
                            values["old"] = get_choices_title(field.choices, f[fkey]["old"])
                        else:
                            values["old"] = "---"
                        values["new"] = get_choices_title(field.choices, f[fkey]["new"])
                    elif isinstance(field, models.ForeignKey):
                        if item["type"]:
                            continue
                        values["old"] = ""
                        try:
                            values["new"] = getattr(obj, field.name)
                        except Exception, e:
                            print e
                    elif isinstance(field, models.ManyToManyField):
                        values["new"] = getattr(obj, field.name).filter(pk__in=values["new"])
                        values["old"] = getattr(obj, field.name).filter(pk__in=values["old"])
                        values["manytomany"] = True

                    fields.append(values)
                item["fields"] = fields

            result.append(item)
        
        # print result
        return result


    def revert(self, delete=False):
        """Reverts all objects in this revision."""
        version_set = self.version_set.all()
        # Optionally delete objects no longer in the current revision.
        if delete:
            # Get a dict of all objects in this revision.
            old_revision = {}
            for version in version_set:
                try:
                    obj = version.object
                except ContentType.objects.get_for_id(version.content_type_id).model_class().DoesNotExist:
                    pass
                else:
                    old_revision[obj] = version
            # Calculate the set of all objects that are in the revision now.
            from reversion.revisions import RevisionManager
            current_revision = RevisionManager.get_manager(self.manager_slug)._follow_relationships(old_revision.keys())
            # Delete objects that are no longer in the current revision.
            for item in current_revision:
                if item in old_revision:
                    if old_revision[item].type == VERSION_DELETE:
                        item.delete()
                else:
                    item.delete()
        # Attempt to revert all revisions.
        def do_revert(versions):
            unreverted_versions = []
            for version in versions:
                try:
                    version.revert()
                except IntegrityError:
                    unreverted_versions.append(version)
            if len(unreverted_versions) == len(versions):
                raise RevertError("Could not revert revision, due to database integrity errors.")
            if unreverted_versions:
                do_revert(unreverted_versions)
        do_revert([version for version in version_set if version.type != VERSION_DELETE])
        
    def __unicode__(self):
        """Returns a unicode representation."""
        # return u", ".join(unicode(version) for version in self.version_set.all())
        return u"#%s" % self.pk


# Version types.

VERSION_ADD = 0
VERSION_CHANGE = 1
VERSION_DELETE = 2

VERSION_TYPE_CHOICES = (
    (VERSION_ADD, "Addition"),
    (VERSION_CHANGE, "Change"),
    (VERSION_DELETE, "Deletion"),
)

def has_int_pk(model):
    """Tests whether the given model has an integer primary key."""
    pk = model._meta.pk
    return (
        (
            isinstance(pk, (models.IntegerField, models.AutoField)) and
            not isinstance(pk, models.BigIntegerField)
        ) or (
            isinstance(pk, models.ForeignKey) and has_int_pk(pk.rel.to)
        )
    )


class VersionManager(models.Manager):
    
    """Manager for Version models."""
    
    @deprecated("Version.objects.get_for_object_reference()", "reversion.get_for_object_reference()")
    def get_for_object_reference(self, model, object_id):
        """
        Returns all versions for the given object reference.
        
        This method was deprecated in django-reversion 1.5, and will be removed in django-reversion 1.7.
        
        New applications should use reversion.get_for_object_reference(). The new version of this method
        returns results ordered with the most recent versions first. This legacy version of the method
        continues to return the results ordered with the oldest versions first.
        """
        from reversion.revisions import default_revision_manager
        return default_revision_manager.get_for_object_reference(model, object_id).order_by("pk")
    
    @deprecated("Version.objects.get_for_object()", "reversion.get_for_object()")
    def get_for_object(self, object):
        """
        Returns all the versions of the given object, ordered by date created.
        
        This method was deprecated in django-reversion 1.5, and will be removed in django-reversion 1.7.
        
        New applications should use reversion.get_for_object(). The new version of this method
        returns results ordered with the most recent versions first. This legacy version of the method
        continues to return the results ordered with the oldest versions first.
        """
        from reversion.revisions import default_revision_manager
        return default_revision_manager.get_for_object(object).order_by("pk")
    
    @deprecated("Version.objects.get_unique_for_object()", "reversion.get_unique_for_object()")
    def get_unique_for_object(self, obj):
        """
        Returns unique versions associated with the object.
        
        This method was deprecated in django-reversion 1.5, and will be removed in django-reversion 1.7.
        
        New applications should use reversion.get_unique_for_object(). The new version of this method
        returns results ordered with the most recent versions first. This legacy version of the method
        continues to return the results ordered with the oldest versions first.
        """
        from reversion.revisions import default_revision_manager
        versions = default_revision_manager.get_unique_for_object(obj)
        versions.reverse()
        return versions
    
    @deprecated("Version.objects.get_for_date()", "reversion.get_for_date()")
    def get_for_date(self, object, date):
        """
        Returns the latest version of an object for the given date.
        
        This method was deprecated in django-reversion 1.5, and will be removed in django-reversion 1.7.
        
        New applications should use reversion.get_for_date().
        """
        from reversion.revisions import default_revision_manager
        return default_revision_manager.get_for_date(object, date)
    
    @deprecated("Version.objects.get_deleted_object()", "reversion.get_for_object_reference()[0]")
    def get_deleted_object(self, model_class, object_id, select_related=None):
        """
        Returns the version corresponding to the deletion of the object with
        the given id.
        
        This method was deprecated in django-reversion 1.5, and will be removed in django-reversion 1.7.
        
        New applications should use reversion.get_for_date()[0].
        """
        from reversion.revisions import default_revision_manager
        return default_revision_manager.get_for_object_reference(model_class, object_id)[0]
    
    @deprecated("Version.objects.get_deleted()", "reversion.get_deleted()")
    def get_deleted(self, model_class, select_related=None):
        """
        Returns all the deleted versions for the given model class.
        
        This method was deprecated in django-reversion 1.5, and will be removed in django-reversion 1.7.
        
        New applications should use reversion.get_deleted(). The new version of this method
        returns results ordered with the most recent versions first. This legacy version of the method
        continues to return the results ordered with the oldest versions first.
        """
        from reversion.revisions import default_revision_manager
        return list(default_revision_manager.get_deleted(model_class).order_by("pk"))


class Version(models.Model):
    """A saved version of a database model."""
    objects = VersionManager()    
    revision = models.ForeignKey(Revision, help_text="The revision that contains this version.")
    object_id = models.TextField(help_text="Primary key of the model under version control.")
    object_id_int = models.IntegerField(blank=True, null=True, db_index=True, 
        help_text="An indexed, integer version of the stored model's primary key, used for faster lookups.")
    content_type = models.ForeignKey(ContentType, help_text="Content type of the model under version control.")
    
    # A link to the current instance, not the version stored in this Version!
    object = generic.GenericForeignKey()
    format = models.CharField(max_length=255, help_text="The serialization format used by this model.")
    serialized_data = models.TextField(help_text="The serialized form of this version of the model.")
    updated_data = models.TextField(help_text="The serialized list of changed fields of this version.")
    object_repr = models.TextField(help_text="A string representation of the object.")
    
    @property
    def object_changes(self):    
        """
        Get unserialized list of object updated data
        """
        def get_choices_title(choices, value):
            for item in choices:
                if int(value) == item[0]:
                    return item[1]
            return ""

        if not hasattr(self, "_updated_data_cache"):
            result = {"list" : [], "changes" : False}
            if self.updated_data:
                values = simplejson.loads(self.updated_data)
                if values in ("add", "delete",):
                    result = {"status" : values}
                    result["changes"] = True
                else:
                    for key in values.keys():
                        if "_type" == key:
                            result["status"] = values[key]
                            continue

                        field = self.object._meta.get_field_by_name(key)[0]
                        if field.choices:
                            if values[key]["old"] is not None:
                                values[key]["old"] = get_choices_title(field.choices, values[key]["old"])
                            else:
                                values[key]["old"] = "---"
                            values[key]["new"] = get_choices_title(field.choices, values[key]["new"])
                        result["list"].append({"title" : field.verbose_name, "key" : key, 
                            "value" : values[key]})
                    result["changes"] = True
            setattr(self, "_updated_data_cache", result)
        return getattr(self, "_updated_data_cache")

    def get_updated_data(self):
        """
        Get unserialized updated data of version
        """
        if not hasattr(self, "_updated_data_unpack_cache"):
            values = ""
            if self.updated_data:
                values = simplejson.loads(self.updated_data)
            setattr(self, "_updated_data_unpack_cache", values)
        return getattr(self, "_updated_data_unpack_cache")

    @property
    def object_version(self):
        """The stored version of the model."""
        data = self.serialized_data
        if isinstance(data, unicode):
            data = data.encode("utf8")
        return list(serializers.deserialize(self.format, data))[0]
    
    type = models.PositiveSmallIntegerField(choices=VERSION_TYPE_CHOICES, db_index=True)
    
    @property   
    def field_dict(self):
        """
        A dictionary mapping field names to field values in this version
        of the model.
        
        This method will follow parent links, if present.
        """
        if not hasattr(self, "_field_dict_cache"):
            object_version = self.object_version
            obj = object_version.object
            result = {}
            for field in obj._meta.fields:
                result[field.name] = field.value_from_object(obj)
            result.update(object_version.m2m_data)
            # Add parent data.
            for parent_class, field in obj._meta.parents.items():
                content_type = ContentType.objects.get_for_model(parent_class)
                if field:
                    parent_id = unicode(getattr(obj, field.attname))
                else:
                    parent_id = obj.pk
                try:
                    parent_version = Version.objects.get(revision__id=self.revision_id,
                                                         content_type=content_type,
                                                         object_id=parent_id)
                except parent_class.DoesNotExist:
                    pass
                else:
                    result.update(parent_version.field_dict)
            setattr(self, "_field_dict_cache", result)
        return getattr(self, "_field_dict_cache")
       
    def revert(self):
        """Recovers the model in this version."""
        self.object_version.save()
        
    def __unicode__(self):
        """Returns a unicode representation."""
        return self.object_repr