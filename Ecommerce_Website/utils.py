from django.utils.text import slugify
import random
import string
import os
'''
random_string_generator is located here:
http://joincfe.com/blog/random-string-generator-in-python/
'''


def get_filename(path):
    return os.path.basename(path)


def unique_key_generator(instance):
    size = random.randint(30, 45)
    key = random_string_generator(size=size)
    Klass = instance.__class__
    qs_exists = Klass.objects.filter(key=key).exists()
    if qs_exists:
        return unique_slug_generator(instance)
    return key


def unique_ordr_id_generator(instance):
    order_id_new = random_string_generator().upper()
    Klass = instance.__class__
    qs_exists = Klass.objects.filter(order_id=order_id_new).exists()
    if qs_exists:
        return unique_slug_generator(instance)
    return order_id_new


def unique_slug_generator(instance, new_slug=None):
    """
    This is for a Django project and it assumes your instance
    has a model with a slug field and a title character (char) field.
    """
    if new_slug is not None:
        slug = new_slug
    else:
        slug = slugify(instance.title)

    Klass = instance.__class__
    qs_exists = Klass.objects.filter(slug=slug).exists()
    if qs_exists:
        new_slug = "{slug}-{randstr}".format(slug=slug, randstr=random_string_generator(size=4))
        return unique_slug_generator(instance, new_slug=new_slug)
    return slug


def random_string_generator(size=10, chars=string.ascii_lowercase + string.digits):
    return ''.join(random.choice(chars) for _ in range(size))


print(random_string_generator())

print(random_string_generator(size=50))
