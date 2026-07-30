{% macro generate_alias_name(custom_alias_name=none, node=none) -%}
    {%- if custom_alias_name -%}
        {{ target.user | lower }}_{{ custom_alias_name | trim }}
    {%- else -%}
        {{ target.user | lower }}_{{ node.name }}
    {%- endif -%}
{%- endmacro %}