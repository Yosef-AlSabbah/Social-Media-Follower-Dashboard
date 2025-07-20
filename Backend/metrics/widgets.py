from django import forms
from django.utils.html import format_html


class ColorPickerWidget(forms.TextInput):
    """
    Custom widget that renders a color picker input for hex color values.
    Shows both a color picker and a text input for manual entry.
    """

    def __init__(self, attrs=None):
        default_attrs = {'type': 'color'}
        if attrs:
            default_attrs.update(attrs)
        super().__init__(default_attrs)

    def render(self, name, value, attrs=None, renderer=None):
        # Ensure the value is in proper hex format
        if value and not value.startswith('#'):
            value = f'#{value}'
        elif not value:
            value = '#000000'  # default to black

        # Create the color input
        color_input = super().render(name, value, attrs, renderer)

        # Create a text input for manual hex entry
        text_attrs = attrs.copy() if attrs else {}
        text_attrs.update({
            'type': 'text',
            'maxlength': '7',
            'pattern': '^#[0-9A-Fa-f]{6}$',
            'placeholder': '#FFFFFF',
            'style': 'width: 100px; margin-left: 10px;'
        })
        text_input = format_html(
            '<input type="text" name="{}_text" value="{}" {}/>',
            name,
            value,
            ' '.join([f'{k}="{v}"' for k, v in text_attrs.items()])
        )

        # JavaScript to sync both inputs
        js_code = format_html("""
        <script>
        (function() {{
            var colorInput = document.querySelector('input[name="{}"]');
            var textInput = document.querySelector('input[name="{}_text"]');
            
            if (colorInput && textInput) {{
                // Sync color picker to text input
                colorInput.addEventListener('input', function() {{
                    textInput.value = this.value.toUpperCase();
                }});
                
                // Sync text input to color picker
                textInput.addEventListener('input', function() {{
                    var hex = this.value;
                    if (/^#[0-9A-Fa-f]{{6}}$/.test(hex)) {{
                        colorInput.value = hex;
                        this.style.borderColor = '';
                    }} else {{
                        this.style.borderColor = 'red';
                    }}
                }});
                
                // Override form submission to use text input value
                var form = colorInput.closest('form');
                if (form) {{
                    form.addEventListener('submit', function() {{
                        colorInput.value = textInput.value;
                    }});
                }}
            }}
        }})();
        </script>
        """, name, name)

        return format_html(
            '<div style="display: flex; align-items: center;">'
            '{} <span style="margin-left: 5px;">Hex:</span> {}'
            '</div>{}',
            color_input, text_input, js_code
        )

    class Media:
        css = {
            'all': ('admin/css/widgets.css',)
        }
