import factory
from django.contrib.contenttypes.models import ContentType


class GenericRelationFactory(factory.django.DjangoModelFactory):
    object_id = factory.SelfAttribute('content_object.id')
    content_type = factory.LazyAttribute(
        lambda o: ContentType.objects.get_for_model(o.content_object)
    )

    class Meta:
        exclude = ['content_object']
        abstract = True
