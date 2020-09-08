from django.forms import widgets


class SelectableSearch(widgets.Input):
    input_type = 'selectable'
    template_name = 'helpers/searchable_combobox.html'

    class Media:
        js = (
            'assets/js/selectable_search.js',
        )

    def __init__(self, attrs=None):
        super().__init__(attrs)

    def get_context(self, name, value, attrs):
        context = super().get_context(name, value, attrs)
        context['widget']['type'] = self.input_type
        return context
