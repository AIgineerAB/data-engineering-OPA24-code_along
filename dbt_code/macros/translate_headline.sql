{% macro translate_headline(column_name) %}
    CASE
        WHEN {{column_name}} = 'Data Engineer' THEN 'Junior data engineer'
        ELSE {{column_name}}
    END
{% endmacro %}