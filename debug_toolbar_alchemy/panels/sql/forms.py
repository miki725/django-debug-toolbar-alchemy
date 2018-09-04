# -*- coding: utf-8 -*-
from __future__ import absolute_import, print_function, unicode_literals

import jsonplus as json
from debug_toolbar.panels.sql.forms import SQLSelectForm
from django.core.exceptions import ValidationError

from debug_toolbar_alchemy.panels.sql.utils import dict_items_to_str

from .utils import add_newlines, get_connections


class AlchemySQLSelectForm(SQLSelectForm):
    def clean_alias(self):
        value = self.cleaned_data["alias"]

        if value not in get_connections():
            raise ValidationError("Database alias '%s' not found" % value)

        return value

    def clean_params(self):
        value = self.cleaned_data["params"]

        try:
            value = json.loads(value)
        except ValueError:
            raise ValidationError("Is not valid JSON")
        else:
            return (
                [dict_items_to_str(i) if isinstance(i, dict) else i for i in value]
                if isinstance(value, (list, tuple))
                else value
            )

    @property
    def connection(self):
        return get_connections()[self.cleaned_data["alias"]]

    @property
    def cursor(self):
        return self.connection.connect()

    def reformat_sql(self):
        return add_newlines(super(AlchemySQLSelectForm, self).reformat_sql())
