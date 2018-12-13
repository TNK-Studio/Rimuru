## {{ name }}

{{desc}}

### 请求地址

`{{method}}`  `{{url}}`


{% if headers | length > 0 %}
### 请求头

| 参数名  | 必填 | 参考值                           |
| ------- | ---- | -------------------------------- |
{%- for header in headers %}
|{{ header.name}}|{{header.required}}|{{header.value}}|
{%- endfor -%}
{%- endif -%}

{% if params | length > 0 %}

### 请求参数

| 参数名   | 类型   | 必填 | 描述 | 默认值 | 参考值 |
| -------- | ------ | ---- | ---- | ------ | ------ |
{%- for param in params %}
|{{ param.name}}|{{param.type}}|{{param.required}}|{{param.desc}}|{{param.default}}|{{param.value}}|
{%- endfor -%}
{%- endif -%}


{% set success_responses = (responses |  success_responses_filter) %}
{% set error_responses = (responses |  error_responses_filter) %}

{% if success_responses | length %}
### 返回正确
{% for response in success_responses %}
{{response.header}}

状态码 `{{response.status_code}}`

```{{response.type}}
{{response.body}}
```
{% endfor %}
{% endif %}

{% if error_responses | length %}
### 返回错误
{% for response in error_responses %}
{{response.header}}

状态码 `{{response.status_code}}`

```{{response.type}}
{{response.body | safe}}
```
{% endfor %}
{% endif %}


{% if note %}
### 备注说明

{{note}}
{% endif %}