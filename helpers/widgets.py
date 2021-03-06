from django.forms import widgets
from django.urls import resolve


class SelectableSearch(widgets.Input):
    input_type = 'selectable'
    template_name = 'helpers/searchable_combobox.html'
    text = ''

    class Media:
        js = (
            'helpers/js/selectable_search.js',
        )

    def __init__(self, search_url, model=None, attrs=None):
        if attrs is not None:
            attrs = attrs.copy()
        self.search_url = search_url
        if model:
            self.model = model
        super().__init__(attrs)

    def get_context(self, name, value, attrs):
        if value and self.model and self.text != ' ':
            self.text = self.model.objects.get(pk=value).designator
        context = super().get_context(name, value, attrs)
        context['widget']['type'] = self.input_type
        context['widget']['search_url'] = self.search_url
        context['widget']['text'] = self.text
        return context

    def value_from_datadict(self, data, files, name):
        self.text = data.get(name+'_selector')
        return super().value_from_datadict(data, files, name)
