from django.contrib.auth.decorators import login_required
from django.urls import reverse
from django.http import JsonResponse, HttpResponseRedirect, HttpResponse
from django.shortcuts import render
from markdown_deux import markdown
from derby_darts.forms.model_forms import RuleForm, RuleCategoryForm
from derby_darts.models import RuleCategory, League, Rule
from .google_docs import google_doc_to_markdown
from django.conf import settings
import os

__author__ = 'Saysell'


def view_rules(request):
    rules = google_doc_to_markdown(settings.RULES_DOC_ID, settings.GOOGLE_SERVICE_ACCOUNT_JSON)
    return render(request,
                  'view.html',
                  {"rules": rules})


@login_required
def add_rule(request, category_id):
    if request.method == 'POST':
        category = RuleCategory.objects.get(league=request.league, id=category_id)
        description = request.POST['description']

        rule = Rule(category=category, description=description)
        rule.save()

    return HttpResponseRedirect(reverse('Rules:browse'))


@login_required
def delete_rule(request, rule_id):
    if request.method == 'POST':
        rule = Rule.objects.get(category__league=request.league, id=int(rule_id))
        rule.delete()
        return JsonResponse(status=200, data={})
    return JsonResponse(status=404, data={})


@login_required
def get_edit_rule_form(request, post_id):
    post = Rule.objects.get(id=post_id)
    if request.method == 'POST':
        form = RuleForm(request.POST, instance=post)
        if form.is_valid():
            form.save()
            return JsonResponse(status=200, data={'id': post_id,
                                                  'description': markdown(form.cleaned_data['description'])})
        return JsonResponse(status=101, data={})
    return HttpResponse(RuleForm(instance=post))


@login_required
def get_edit_category_form(request, category_id):
    post = RuleCategory.objects.get(id=category_id)
    if request.method == 'POST':
        form = RuleCategoryForm(request.POST, instance=post)
        if form.is_valid():
            form.save()
            return JsonResponse(status=200, data={'id': category_id,
                                                  'description': markdown(form.cleaned_data['name'])})
        return JsonResponse(status=101, data={})
    return HttpResponse(RuleCategoryForm(instance=post))


@login_required
def edit_rule(request):
    if request.method == 'POST':
        rule = Rule.objects.get(id=request.POST['rule_id'])
        rule.description = request.POST['rule_text']
        rule.save()
        return JsonResponse(status=200, data={})
    return JsonResponse(status=404, data={})


@login_required
def add_category(request):
    if request.method == 'POST':
        name = request.POST['description']

        category = RuleCategory(league=request.league,
                                name=name)
        category.save()

    return HttpResponseRedirect(reverse('Rules:browse'))


@login_required
def edit_category(request):
    if request.method == 'POST':
        rule = RuleCategory.objects.get(league=request.league, id=request.POST['data_id'])
        rule.name = request.POST['data_text']
        rule.save()
        return JsonResponse(status=200, data={})
    return JsonResponse(status=404, data={})


@login_required
def delete_category(request, category_id):
    if request.method != 'POST':
        rule = RuleCategory.objects.get(league=request.league, id=category_id)
        rule.delete()
        return JsonResponse(status=200, data={'status': 'done'})
    return JsonResponse(status=404, data={})


def import_rules(request):
    if request.method == 'POST':
        file_name = request.FILES['file_upload']
        if not file_name:
            return JsonResponse(status=100, data={'No file received'})
        # with open(file_name) as f:
            # content = f.readlines()

        current_category = None
        current_rule = None
        for line in file_name:
            if line.startswith('+'):
                cat = line.strip(' +\r\n')  # trim trailing spaces and plus
                current_category = RuleCategory.objects.create(league=request.league, name=cat)
                continue
            if line.startswith('-'):
                rule = line.strip(' -\r\n')
                if not current_category:
                    raise Warning('{} skipped, no category found'.format(rule))
                if len(rule) > 300:
                    # raise Warning('{} skipped, too long'.format(rule))
                    continue
                Rule.objects.create(category=current_category, description=rule)
        return JsonResponse(status=200, data={})

    return render(request, 'import.html', {})


