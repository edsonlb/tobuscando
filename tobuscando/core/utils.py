# coding: utf-8
from django.template.defaultfilters import slugify


def slug(instance, model, title):
    if not instance.slug:
        slug = slugify(title)
        new_slug = slug

        count = 0
        while model.objects.filter(slug=new_slug)\
                   .exclude(pk=instance.pk).count() > 0:
            count += 1
            new_slug = '{slug}-{counter}'.format(slug=slug, counter=count)

        return new_slug
