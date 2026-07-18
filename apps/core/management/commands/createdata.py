from django.core.management.base import BaseCommand
from django.utils import timezone
from datetime import timedelta
import random

from apps.accounts.models import User
from apps.menu.models import Product, Category
from apps.orders.models import Order, OrderItem
from apps.news.models import Post
from apps.contact.models import Message


class Command(BaseCommand):
    help = "Sample (demo) data yaratish — admin panel to'liq ko'rinsin"

    def handle(self, *args, **options):
        self.create_products()
        self.create_orders()
        self.create_posts()
        self.create_messages()
        self.stdout.write(self.style.SUCCESS("Demo data yaratildi"))

    def create_products(self):
        cat, _ = Category.objects.get_or_create(name="Asosiy taomlar")
        if Product.objects.count() == 0:
            names = ["Shish kebab", "Chicken Shawarma", "Iskender Kebab",
                     "Doner Kebab Wrap", "Lahmacun Pizza", "Grilled Fish"]
            for i, n in enumerate(names):
                Product.objects.create(
                    category=cat,
                    name=n,
                    price=random.randint(25000, 90000),
                    description=f"{n} — ta'mli va sifatli taom.",
                    is_active=True,
                )

    def create_orders(self):
        products = list(Product.objects.all())
        if not products:
            return
        if Order.objects.count() >= 20:
            return
        customers = [
            ("Ali", "+998901111111"),
            ("Vali", "+998902222222"),
            ("Olim", "+998903333333"),
            ("Dilshod", "+998904444444"),
            ("Aziza", "+998905555555"),
            ("Jasur", "+998906666666"),
            ("Malika", "+998907777777"),
            ("Sardor", "+998908888888"),
        ]
        channels = ["online", "offline"]
        statuses = ["completed", "completed", "pending", "processing"]
        for i in range(30):
            c = random.choice(customers)
            order = Order.objects.create(
                customer_name=c[0],
                customer_phone=c[1],
                channel=random.choice(channels),
                status=random.choice(statuses),
                created_at=timezone.now() - timedelta(days=random.randint(0, 30)),
            )
            p = random.choice(products)
            OrderItem.objects.create(
                order=order,
                product=p,
                quantity=random.randint(1, 3),
                price=p.price,
            )
            order.recalculate_total()

    def create_posts(self):
        if Post.objects.count() == 0:
            sample = [
                ("Yangi menyu taqdim etildi", "Bizning yangi taomlarimiz bilan tanishing.",
                 "yangiliklar"),
                ("Hafta aksiyasi", "Tanlangan taomlarga 20% chegirma.", "aksiya"),
                ("Dam olish kuni tadbiri", "Shanba kuni jonli musiqa.", "tadbirlar"),
            ]
            for title, desc, cat in sample:
                Post.objects.create(title=title, desc=desc, category=cat, content=desc)

    def create_messages(self):
        if Message.objects.count() == 0:
            sample = [
                ("Mijoz", "Salom, yetkazib berish qachon bo'ladi?", False),
                ("Aziza", "Menyuda vegetarian taomlari bormi?", False),
                ("Jasur", "Rahmat, juda mazali edi!", True),
            ]
            for name, text, is_read in sample:
                Message.objects.create(name=name, text=text, is_read=is_read)
