from django.utils.text import slugify

choices = (
    (1, 'Uno'),
    (2, 'Dos'),
    (3, 'Tres'),
    (4, 'Cuatro'),
    (5, 'Cinco'),
    (6, 'Seis'),
    (7, 'Siete'),
    (8, 'Ocho'),
    (9, 'Nueve'),
    (10, 'Diez'),
)

def generate_unique_slug(klass, field):
    """
    return unique slug if origin slug is exist.
    eg: `foo-bar` => `foo-bar-1`

    :param `klass` is Class model.
    :param `field` is specific field for title.
    """
    origin_slug = slugify(field)
    unique_slug = origin_slug
    numb = 1
    while klass.objects.filter(slug=unique_slug).exists():
        unique_slug = '%s-%d' % (origin_slug, numb)
        numb += 1
    return unique_slug
