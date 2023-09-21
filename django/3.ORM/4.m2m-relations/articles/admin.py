from django.contrib import admin
from django.core.exceptions import ValidationError
from django.forms import BaseInlineFormSet

from .models import Article, Tag, Scope


class ScopeInlineFormset(BaseInlineFormSet):
    def clean(self):
        is_mine_number = 0
        for form in self.forms:
            if form.cleaned_data.get('is_main'):
                is_mine_number += 1

        if is_mine_number > 1:
            raise ValidationError('Основной раздел должен быть только один!')
        elif is_mine_number == 0:
            raise ValidationError('Укажите основной раздел!')
        return super().clean()


class ScopeInline(admin.TabularInline):
    model = Scope
    formset = ScopeInlineFormset


@admin.register(Article)
class ArticleAdmin(admin.ModelAdmin):
    inlines = [ScopeInline]


@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    pass
