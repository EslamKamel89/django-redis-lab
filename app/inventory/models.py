from typing import Iterable, Type

from django.db import models
from django.utils.text import slugify
from django_stubs_ext.db.models import TypedModelMeta


def _generate_unique_slug(model: Type[models.Model], value: str) -> str:
    base_slug = slugify(value)
    slug = base_slug
    counter = 1
    while model.objects.filter(slug=slug).exists():
        slug = f"{base_slug}-{counter}"
        counter += 1
    return slug


class Category(models.Model):

    parent = models.ForeignKey(
        "self",
        on_delete=models.RESTRICT,
        null=True,
        blank=True,
        related_name="children",
    )
    name = models.CharField(max_length=100, unique=True)
    slug = models.SlugField(max_length=120, unique=True, blank=True)
    is_active = models.BooleanField(default=True)
    level = models.SmallIntegerField(default=0)

    def save(self, *args, **kwargs) -> None:
        if not self.slug:
            self.slug = _generate_unique_slug(type(self), self.name)
        super().save(*args, **kwargs)

    def __str__(self) -> str:
        return self.name

    class Meta(TypedModelMeta):
        pass


class Product(models.Model):
    category = models.ForeignKey(
        "Category", on_delete=models.CASCADE, related_name="products"
    )
    name = models.CharField(max_length=100, unique=True)
    slug = models.SlugField(max_length=120, unique=True)
    description = models.TextField(null=True, blank=True)
    is_digital = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    created_at = models.DateTimeField(auto_now_add=True, null=True, blank=True)
    updated_at = models.DateTimeField(auto_now=True, null=True, blank=True)

    def save(self, *args, **kwargs) -> None:
        if not self.slug:
            self.slug = _generate_unique_slug(type(self), self.name)
        super().save(*args, **kwargs)

    def __str__(self) -> str:
        return self.name

    class Meta(TypedModelMeta):
        pass
