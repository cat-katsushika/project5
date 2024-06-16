from django import template

register = template.Library()


@register.simple_tag(takes_context=True)
def get_dynamic_var(context, base_name, index):
    var_name = f"{base_name}{index}"
    return context.get(var_name, "")
