#coding:utf-8
from django.contrib import admin
from django.contrib.admin import widgets, helpers
from django.contrib.contenttypes.models import ContentType
from django.core.exceptions import PermissionDenied
from django.forms.formsets import all_valid
from django.forms.util import ErrorList
from django.http import HttpResponseRedirect, Http404
from django.shortcuts import get_object_or_404 
from django.utils.encoding import force_unicode
from django.utils.safestring import mark_safe
from django.utils.translation import ugettext as _
from django.views.generic.simple import direct_to_template


class ModifyModelAdmin(admin.ModelAdmin):
    """
    Update admin model class.
    Add view for formset page
    """
    inlines_formsets_pages = []

    def __init__(self, *args, **kwargs):
        """
        Add formset inline instances loader
        """
        super(ModifyModelAdmin, self).__init__(*args, **kwargs)

        self.inline_instances_formset = []
        self.formset_pages = {}
        for item in self.inlines_formsets_pages:
            self.formset_pages[item[1]] = {"title" : item[0], "instances" : []}
            for inline_class in item[2]["models"]:
                inline_instance = inline_class(self.model, self.admin_site)
                self.formset_pages[item[1]]["instances"].append(inline_instance)
                # self.inline_instances_formset.append(inline_instance)

    def get_urls(self):
        from django.conf.urls.defaults import patterns
        keys = "|".join(self.formset_pages.keys())
        return patterns('',
            (r'^(\d+)/(%s)/$' % keys, self.admin_site.admin_view(self.formset_list_page))
        ) + super(ModifyModelAdmin, self).get_urls()
        # return urls + super(ModifyModelAdmin, self).get_urls()
        # return patterns('',
            # (r'^(\d+)/screenshots/$', self.admin_site.admin_view(self.add_screenshots)),
            # (r'^(\d+)/articles/$', self.admin_site.admin_view(self.articles_page))
        # ) + super(ModifyModelAdmin, self).get_urls()

    def formset_list_page(self, request, object_id, page):
        """
        Relate articles view. 
        """
        self.page = page
        model = self.model
        opts = model._meta

        obj = get_object_or_404(self.model, pk=object_id)

        if not self.has_change_permission(request, obj):
            raise PermissionDenied

        if obj is None:
            raise Http404(_('%(name)s object with primary key %(key)r does not exist.') % {'name': force_unicode(opts.verbose_name), 'key': escape(object_id)})

        page_title = self.formset_pages[page]["title"]
        formsets_instances = self.formset_pages[page]["instances"]
        formsets = []
        if request.method == 'POST':
            new_object = obj
            prefixes = {}
            for FormSet, inline in zip(self.get_formsets_new(request, new_object), formsets_instances):
                prefix = FormSet.get_default_prefix()
                prefixes[prefix] = prefixes.get(prefix, 0) + 1
                if prefixes[prefix] != 1:
                    prefix = "%s-%s" % (prefix, prefixes[prefix])
                formset = FormSet(request.POST, request.FILES, instance=new_object, prefix=prefix, 
                    queryset=inline.queryset(request))
                formsets.append(formset)

            if all_valid(formsets):
                for formset in formsets:
                    formset.save()
                
                change_message = self.construct_change_message(request, BlankForm(), formsets)
                self.log_change(request, new_object, change_message)
                return self.response_change_formset(request, new_object)
        else:
            prefixes = {}
            for FormSet, inline in zip(self.get_formsets_new(request, obj), formsets_instances):
                prefix = FormSet.get_default_prefix()
                prefixes[prefix] = prefixes.get(prefix, 0) + 1
                if prefixes[prefix] != 1:
                    prefix = "%s-%s" % (prefix, prefixes[prefix])
                formset = FormSet(instance=obj, prefix=prefix, queryset=inline.queryset(request))
                formsets.append(formset)

        media = self.media
        inline_admin_formsets = []
        for inline, formset in zip(formsets_instances, formsets):
            fieldsets = list(inline.get_fieldsets(request, obj))
            readonly = list(inline.get_readonly_fields(request, obj))
            inline_admin_formset = helpers.InlineAdminFormSet(inline, formset,
                fieldsets, readonly, model_admin=self)
            inline_admin_formsets.append(inline_admin_formset)
            media = media + inline_admin_formset.media
        
        context = {
            'add': False,
            'change': True,
            'title': '%s %s:' % (page_title, obj.name,),
            'object_id': object_id,
            'original': obj,
            'is_popup': False,
            'media': mark_safe(media),
            'inline_admin_formsets': inline_admin_formsets,
            'errors': AdminFormsetErrorList(formsets),
            'root_path': self.admin_site.root_path,
            'app_label': opts.app_label,
            'formset_title' : page_title,
            'has_add_permission': False,
            'has_change_permission': True,
            'has_delete_permission': False,
            'has_file_field': True, # FIXME - this should check if form or formsets have a FileField,
            'has_absolute_url': hasattr(self.model, 'get_absolute_url'),
            'form_url': '',
            'opts': opts,
            'save_as': self.save_as,
            'save_on_top': self.save_on_top,
            'root_path': self.admin_site.root_path,
        }

        return direct_to_template(request, "admin/change_formset_page.html", context)

    def get_formsets_new(self, request, obj=None):
        """
        #TODO: Stupid name need to update
        """
        for inline in self.formset_pages[self.page]["instances"]:
            yield inline.get_formset(request, obj)

    def response_change_formset(self, request, obj, post_url_continue='../../%s/%s/'):
        """
        Determines the HttpResponse for the change_view stage.
        """
        opts = obj._meta
        pk_value = obj._get_pk_val()
        verbose_name = opts.verbose_name
        # msg = _('The %(name)s "%(obj)s" was added successfully.') % {'name': force_unicode(opts.verbose_name), 'obj': force_unicode(obj)}
        msg = _(u'Изменения раздела "%(title)s" для %(name)s "%(obj)s" успешно сохранены.') % \
            {"title" : force_unicode(self.formset_pages[self.page]["title"]), 'name': force_unicode(opts.verbose_name), 'obj': force_unicode(obj)}
        
        if "_continue" in request.POST:
            self.message_user(request, msg + ' ' + _(u"Ниже Вы можете продолжить редактирование."))
            return HttpResponseRedirect(post_url_continue % (pk_value, self.page,))
        else:
            self.message_user(request, msg)
            if self.has_change_permission(request, None):
                return HttpResponseRedirect('../../')
            else:
                return HttpResponseRedirect('../../../../')


class AdminFormsetErrorList(ErrorList):
    """
    Stores all errors for the formsets in an add/change stage view.
    Copy of base admin class but without check form valid
    """
    def __init__(self, inline_formsets):
        for inline_formset in inline_formsets:
            self.extend(inline_formset.non_form_errors())
            for errors_in_inline_form in inline_formset.errors:
                self.extend(errors_in_inline_form.values())


class BlankForm(object):
    """
    Class with fields for similate form behaviour in base admin functions
    """
    changed_data = False
