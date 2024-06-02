from django.core.management.base import BaseCommand
from products.models import Product, SizeChart

class Command(BaseCommand):
    help = 'Fetch and print product details based on size IDs'

    def handle(self, *args, **options):
        product_list = [
            {"size_id": 262, "quantity": 3, "product_id": 262}, 
            {"size_id": 259, "quantity": 1, "product_id": 259}
        ]
        
        for item in product_list:
            try:
                size_chart = SizeChart.objects.get(id=item['size_id'])
                product = size_chart.product
                self.stdout.write(f"SizeChart: {size_chart}")
                self.stdout.write(f"Product: {product.product_name}")
            except SizeChart.DoesNotExist:
                self.stdout.write(f"SizeChart with id {item['size_id']} does not exist.")
            except Product.DoesNotExist:
                self.stdout.write(f"Product with id {item['product_id']} does not exist.")
