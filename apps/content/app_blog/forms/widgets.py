from django import forms
from django.db import IntegrityError
from django_select2.forms import ModelSelect2TagWidget
from apps.core.app_main.models.tags import Tag

class TagSelect2TagWidget(ModelSelect2TagWidget):
    model = Tag
    search_fields = ["name__icontains"]

    def create_value(self, value):
        cleaned = value.strip()

        if len(cleaned) < 2:
            raise forms.ValidationError("Le nom du tag est trop court.")
        
        # Vérifie si le tag existe déjà (sécurité + perf)
        existing = Tag.objects.filter(name__iexact=cleaned).first()
        if existing:
            return existing

        try:
            return self.get_queryset().create(name=cleaned)
        except IntegrityError:
            raise forms.ValidationError("Ce tag existe déjà (vérification en base).")

    def value_from_datadict(self, data, files, name):
        values = data.getlist(name)
        cleaned_values = []

        for val in values:
            try:
                # Si val est un ID (existant), on le garde
                int(val)
                cleaned_values.append(val)
            except ValueError:
                # Si val n’est pas un ID, c’est une nouvelle valeur à créer
                tag = self.create_value(val)
                cleaned_values.append(str(tag.pk))  # On ajoute son ID

        return cleaned_values

    def build_attrs(self, base_attrs, extra_attrs=None):
        # Empêche Select2 JS de couper les mots saisis (comme "Richard Gotainer")
        attrs = super().build_attrs(base_attrs, extra_attrs)
        attrs["data-token-separators"] = "[]"
        return attrs
