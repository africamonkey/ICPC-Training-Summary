# -*- coding: utf-8 -*-"""views.py: Django simple_history"""
import json

import logging
from pprint import pformat
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib.contenttypes.models import ContentType
from django.core.exceptions import ObjectDoesNotExist
from django.http import HttpResponse
from django.utils.decorators import method_decorator
from django.views.generic import ListView

__author__ = 'Steven Klass'
__date__ = '9/18/12 10:46 PM'
__copyright__ = 'Copyright 2012 IC Manage. All rights reserved.'
__credits__ = ['Steven Klass', ]

log = logging.getLogger(__name__)

class HistoryListView(ListView):
    """History List View"""
    template_name = "simple_history/historical_list.html"

    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        """Ensure we have access"""
        return super(HistoryListView, self).dispatch(*args, **kwargs)

    def get_model_obj(self):
        """Return the generic model object"""
        if hasattr(self, 'model_obj'): return self.model_obj
        model_ct = ContentType.objects.get(
            app_label=self.kwargs.get('app_label'), model=self.kwargs.get('model'))
        self.model_obj = model_ct.model_class()
        return self.model_obj

    def get_object(self, id=None):
        """If we have a pk then we know the row"""
        if id is None and self.kwargs.get('field') == 'id':
            id = self.kwargs.get('constraint')
        self.object = self.get_model_obj().objects.get(pk=id)
        return self.object

    def get_queryset(self):
        """Narrow this based on your company"""
        filter = {self.kwargs.get('field'): self.kwargs.get('constraint')}
        return self.get_model_obj().history.filter(**filter).order_by("history_id")

    def get_context_data(self, **kwargs):
        context = super(HistoryListView, self).get_context_data(**kwargs)
        context['model'] = self.get_model_obj()
        context['object'] = self.get_object()
        context['app_label'] = self.kwargs.get('app_label')
        context['model'] = self.kwargs.get('model')
        context['field'] = self.kwargs.get('field')
        context['constraint'] = self.kwargs.get('constraint')
        return context

    def get_serialized_data(self):
        """Serialize the historical data.  Used in AJAX requests to load the table data."""
        results = []
        fields = self.get_model_obj()._meta.fields

        user_dict = {}
        object_dict = {}
        related_dict = {}

        object_list = self.get_queryset().distinct().values()

        href = u'<a href="{}">{}</a>'
        type_choices = (('+', u'Created'), ('~', u'Changed'), ('-', u'Deleted'))
        for index, item in enumerate(object_list):
            data = {"DT_RowId": item.get('history_id'), 0: '',
                    1: '', 2: '', 3: '-', 4: '-', 5: '-', 6: '-'}

            # 0 - Date
            # 1 - Who
            # 2 - Object (if not specific)
            # 3 - Action
            # 4 - Field
            # 5 - Previous
            # 6 - Current
            data[0] = item.get('history_date').strftime("%m/%d/%y %H:%M")

            try:
                data[1] = user_dict[item.get('history_user_id')]
            except KeyError:
                link = u''
                try:
                    user = User.objects.get(id=item.get('history_user_id'))
                    link = href.format(user.profile.get_absolute_url(),user.get_full_name())
                except ObjectDoesNotExist:
                    link = u"Administrator*"
                user_dict[item.get('history_user_id')] = link
                data[1] = user_dict[item.get('history_user_id')]

            try:
                data[2] = object_dict[item.get('id')]
            except KeyError:
                link, data_obj = u'', u''
                try:
                    data_obj = self.get_object(id=item.get('id'))
                    name = data_obj.__unicode__()
                    name = name if len(name) < 32 else name[0:32] + u" ..."
                    link = href.format(data_obj.get_absolute_url(), name)
                except ObjectDoesNotExist:
                    link = "Deleted"
                except AttributeError:
                    link = data_obj.__unicode__()
                object_dict[item.get('id')] = link
                data[2] = object_dict[item.get('id')]

            data[3] = next((y for x, y in type_choices if x == item.get('history_type')), u"-")


            try:
                previous_item = object_list[index - 1]
            except AssertionError:
                previous_item = {}
            changed_fields, prev_values, cur_values = [], [], []
            for field in fields:
                if field.name == "modified_date":
                    continue
                prev_value = previous_item.get(field.name, u"-")
                prev_value = prev_value if prev_value else u"-"
                curr_value = item.get(field.name, u"-")
                curr_value = curr_value if curr_value else u"-"

                # Handle nice choices keys
                if hasattr(field, '_choices') and len(field._choices) and curr_value != u'-':
                    curr_value = next((x[1] for x in field._choices if str(x[0]) == str(curr_value)))
                # Handle foreign keys.
                elif hasattr(field, 'related') and curr_value != u'-':
                    try:
                        curr_value = related_dict[(field.name, curr_value)]
                        # log.debug("Related (current) Dict - Query Saved {} = {}".format(field.name, curr_value))
                    except KeyError:
                        _v = u'-'
                        try:
                            _v = field.related.parent_model.objects.get(id=curr_value).__unicode__()
                        except ObjectDoesNotExist:
                            _v = u'Deleted'
                        # log.debug("Setting C Related ({}, {}) = {}".format(field.name, curr_value,_v))
                        related_dict[(field.name, curr_value)] = _v
                        curr_value = related_dict[(field.name, curr_value)]

                if hasattr(field, '_choices') and len(field._choices) and prev_value != u'-':
                    prev_value = next((x[1] for x in field._choices if str(x[0]) == str(prev_value)))

                elif hasattr(field, 'related') and prev_value != u'-':
                    try:
                        prev_value = related_dict[(field.name, prev_value)]
                        # log.debug("Related (prev) Dict - Query Saved {} = {}".format(field.name, prev_value))
                    except KeyError:
                        _v = u'-'
                        try:
                            _v = field.related.parent_model.objects.get(id=prev_value).__unicode__()
                        except ObjectDoesNotExist:
                            _v = u'Deleted'
                        # log.debug("Setting P Related ({}, {}) = {}".format(field.name, prev_value,_v))
                        related_dict[(field.name, prev_value)] = _v
                        prev_value = related_dict[(field.name, prev_value)]

                if prev_value != curr_value:
                    changed_fields.append(field.name)
                    prev_values.append(prev_value)
                    cur_values.append(curr_value)
            if len(changed_fields):
                data[4] = u"<br />".join([unicode(x) for x in changed_fields])
                data[5] = u"<br />".join([unicode(x) for x in prev_values])
                data[6] = u"<br />".join([unicode(x) for x in cur_values])
                results.append(data)

        results.reverse()
        # log.debug(pformat(results))
        return results

    def get(self, context, **kwargs):
        if self.request.is_ajax():
            result = self.get_serialized_data()
            return HttpResponse(json.dumps({"aaData": result}), mimetype="application/json")
        return super(HistoryListView, self).get(context, **kwargs)
