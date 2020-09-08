from django.forms import widgets


class SelectableSearch(widgets.Input):
    input_type = 'selectable'
    template_name = 'helpers/searchable_combobox.html'
    text = ''

    class Media:
        js = (
            'assets/js/selectable_search.js',
        )

    def __init__(self, search_url, attrs=None):
        if attrs is not None:
            attrs = attrs.copy()
        self.search_url = search_url
        super().__init__(attrs)

    def get_context(self, name, value, attrs):
        context = super().get_context(name, value, attrs)
        context['widget']['type'] = self.input_type
        context['widget']['search_url'] = self.search_url
        context['widget']['text'] = self.text
        return context

    def value_from_datadict(self, data, files, name):
        self.text = data.get(name+'_selector')
        return super().value_from_datadict(data, files, name)
