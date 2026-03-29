import csv
from decimal import Decimal
from pathlib import Path

from django.contrib.auth.models import User
from django.core.management.base import BaseCommand
from django.db import transaction
from inventory.models import Category, Product

SEED_DIR = Path(__file__).resolve().parents[3] / "seed_data"


class Command(BaseCommand):
    help = "Seed database from CSV files"

    def handle(self, *args, **kwargs) -> str | None:
        with transaction.atomic():
            self.stdout.write("Creating super user .....")
            user, created = User.objects.get_or_create(
                username="admin",
                defaults={
                    "email": "admin@gmail.com",
                    "is_staff": True,
                    "is_superuser": True,
                    "is_active": True,
                },
            )
            if created:
                user.set_password("password")
                user.save()
            self.stdout.write("Truncating categories and products table .....")
            Product.objects.all().delete()
            Category.objects.all().delete()
            self.load_categories()
            self.load_products()

    def load_categories(self):
        with open(SEED_DIR / "categories.csv", encoding="utf-8") as f:
            reader = list(csv.DictReader(f))
        created = {}
        while reader:
            remaining = []
            for row in reader:
                parent_slug = row["parent_slug"]
                if parent_slug == "\\N" or parent_slug in created:
                    parent = created.get(parent_slug)
                    obj = Category.objects.create(
                        name=row["name"],
                        slug=row["slug"],
                        parent=parent,
                        is_active=row["is_active"] == "true",
                        level=int(row["level"]),
                    )
                    created[row["slug"]] = obj
                else:
                    remaining.append(row)
            if len(remaining) == len(reader):
                raise Exception("Unresolved category dependencies")
            reader = remaining

    def load_products(self):
        categories = {c.slug: c.id for c in Category.objects.all()}  # type: ignore

        with open(SEED_DIR / "products.csv", encoding="utf-8") as f:
            reader = csv.DictReader(f)

            objs = []
            for row in reader:
                objs.append(
                    Product(
                        category_id=categories[row["category_slug"]],
                        name=row["name"],
                        slug=row["slug"],
                        description=row["description"],
                        is_digital=row["is_digital"] == "true",
                        is_active=row["is_active"] == "true",
                        price=Decimal(row["price"]),
                    )
                )

            Product.objects.bulk_create(objs)
