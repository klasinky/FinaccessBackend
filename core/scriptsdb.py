def create_currency(apps, schema_editor):
    currency_model = apps.get_model("core", "currency")
    currency_model.objects.create(name="Euro", symbol="€")
    currency_model.objects.create(name="Dolar", symbol="$")


def create_categories(apps, schema_editor):
    category_model = apps.get_model('core', 'category')
    category_model.objects.create(name="Servicios")
    category_model.objects.create(name="Entretenimiento")
    category_model.objects.create(name="Comida")
    category_model.objects.create(name="Otros")


def create_tags(apps, schema_editor):
    tag_model = apps.get_model('core', 'tag')
    tag_model.objects.create(name="Ayuda")
    tag_model.objects.create(name="Off topic")
    tag_model.objects.create(name="Tutorial")
    tag_model.objects.create(name="Ahorro")
    tag_model.objects.create(name="Criptomonedas")
