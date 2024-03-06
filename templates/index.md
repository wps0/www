## MIMUW fandom reader
Ładniejszy reader fandomu MIMUW. Poniżej próbka na kilku wpisach:

{% for entity in entities %}
- [{{entity.name}}]({{entity.exported_url}})
{% endfor %}