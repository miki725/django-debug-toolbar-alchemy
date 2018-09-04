# -*- coding: utf-8 -*-
from __future__ import absolute_import, print_function, unicode_literals

from debug_toolbar.decorators import require_show_toolbar
from django.http import JsonResponse
from django.template.response import SimpleTemplateResponse
from django.views.decorators.csrf import csrf_exempt

from ...explain import explain
from .forms import AlchemySQLSelectForm


@csrf_exempt
@require_show_toolbar
def sql_select(request):
    """Returns the output of the SQL SELECT statement"""
    form = AlchemySQLSelectForm(request.POST or None)

    if not form.is_valid():
        return JsonResponse(dict(form.errors), status=400)

    with form.cursor:
        query = form.cursor.execute(form.cleaned_data["raw_sql"], *form.cleaned_data["params"])

    context = {
        "result": query.fetchall(),
        "sql": form.reformat_sql(),
        "duration": form.cleaned_data["duration"],
        "headers": list(query.keys()),
        "alias": form.cleaned_data["alias"],
    }

    # Using SimpleTemplateResponse avoids running global context processors.
    return SimpleTemplateResponse("debug_toolbar/panels/sql_select.html", context)


@csrf_exempt
@require_show_toolbar
def sql_explain(request):
    """Returns the output of the SQL EXPLAIN on the given query"""
    form = AlchemySQLSelectForm(request.POST or None)

    if not form.is_valid():
        return JsonResponse(dict(form.errors), status=400)

    with form.cursor:
        query = explain(form.cleaned_data["raw_sql"], form.cursor).execute(*form.cleaned_data["params"])

    context = {
        "result": query.fetchall(),
        "sql": form.reformat_sql(),
        "duration": form.cleaned_data["duration"],
        "headers": list(query.keys()),
        "alias": form.cleaned_data["alias"],
    }

    # Using SimpleTemplateResponse avoids running global context processors.
    return SimpleTemplateResponse("debug_toolbar/panels/sql_explain.html", context)
