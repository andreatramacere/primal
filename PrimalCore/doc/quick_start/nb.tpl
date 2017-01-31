%%writefile simplepython.tpl

{% extends 'python.tpl'%}

## remove markdown cells
{% block markdowncell -%}
{% endblock markdowncell %}

## remove raw cells
{% block rawcell -%}
{% endblock rawcell %}

## change the appearance of execution count
{% block in_prompt %}
# This was input cell with execution count: {{ cell.execution_count if cell.execution_count else ' ' }}
{%- endblock in_prompt %}
