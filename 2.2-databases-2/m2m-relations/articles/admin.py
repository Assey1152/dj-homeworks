from django.contrib import admin
from django.core.exceptions import ValidationError

from .models import Article, Tag, Scope
from django.forms import BaseInlineFormSet


class ScopeInlineFormset(BaseInlineFormSet):

    def clean(self):
        main_tags = 0
        if any(self.errors):
            return
        for form in self.forms:
            if form.cleaned_data.get('is_main'):
                main_tags += 1
        if not main_tags:
            raise ValidationError('Укажите основной раздел')
        elif main_tags > 1:
            raise ValidationError('Основным может быть только один раздел')

        return super().clean()


class ScopeInline(admin.TabularInline):
    model = Scope
    formset = ScopeInlineFormset
    extra = 3


@admin.register(Article)
class ArticleAdmin(admin.ModelAdmin):
    inlines = [ScopeInline, ]
    pass


@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    list_display = ['id', 'name', ]
