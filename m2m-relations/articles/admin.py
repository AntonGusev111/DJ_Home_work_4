from django.contrib import admin
from django.core.exceptions import ValidationError
from django.forms import BaseInlineFormSet
from .models import Article, Tag, ArticleTags
from collections import Counter


class RelationshipInlineFormset(BaseInlineFormSet):
    def clean(self):
        main_flag = False
        self.unic_tags()
        for form in self.forms:
            if main_flag and form.cleaned_data.get('is_main'):
                raise ValidationError('Главный тег должен быть только один')
            if form.cleaned_data.get('is_main'):
                main_flag = True
                continue
            if main_flag == False:
                raise ValidationError('Необходимо указать главный тег')
        return super().clean()

    def unic_tags(self):
        real_forms = [f for f in self.forms]
        tags = [form.cleaned_data.get('tag') for form in real_forms]
        duplicate_tags_list = [k for k, v in Counter(tags).items() if v > 1]
        print(duplicate_tags_list)
        if len(duplicate_tags_list) > 0:
            if duplicate_tags_list[0] != None:
                raise ValidationError('указано 2 одинаковых тэга')


class RelationshipInline(admin.TabularInline):
    model = ArticleTags
    formset = RelationshipInlineFormset


@admin.register(Article)
class ArticleAdmin(admin.ModelAdmin):
    inlines = [RelationshipInline]


@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    tag = Tag.name
    pass
