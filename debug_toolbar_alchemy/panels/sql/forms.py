# -*- coding: utf-8 -*-
from __future__ import absolute_import, print_function, unicode_literals

import jsonplus as json
from debug_toolbar.panels.sql.forms import SQLSelectForm
from django.core.exceptions import ValidationError

from .utils import add_newlines, get_connections


class AlchemySQLSelectForm(SQLSelectForm):
    def clean_raw_sql(self):
        return self.cleaned_data["raw_sql"]

    def clean_alias(self):
        value = self.cleaned_data["alias"]

        if value not in get_connections():
            raise ValidationError("Database alias '%s' not found" % value)

        return value

    def clean_params(self):
        value = self.cleaned_data["params"]

        try:
            return json.loads(value)
        except ValueError:
            raise ValidationError("Is not valid JSON")

    @property
    def connection(self):
        return get_connections()[self.cleaned_data["alias"]]

    @property
    def cursor(self):
        return self.connection.connect()

    def reformat_sql(self):
        return add_newlines(super(AlchemySQLSelectForm, self).reformat_sql())
