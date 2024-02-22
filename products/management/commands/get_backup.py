import json
from django.core.management.base import BaseCommand
from static_data.models import PrivacyPolicy,RefundCancellationPolicy,TermsAndCondition  # Import your models from static_data app
from static_data.serializers import RefundCancellationPolicySerializer,PrivacyPolicySerializer,TermsAndConditionSerializer

class Command(BaseCommand):
    help = 'Export data from models in static_data app to JSON'

    def handle(self, *args, **kwargs):
        data = []
        privacy = PrivacyPolicySerializer(PrivacyPolicy.objects.all(),many=True).data
        refund = RefundCancellationPolicySerializer(RefundCancellationPolicy.objects.all(),many=True).data
        term = TermsAndConditionSerializer(TermsAndCondition.objects.all(),many=True).data
        with open('refund.json', 'w') as f:
            json.dump(refund, f)
        with open('privacy.json', 'w') as f:
            json.dump(privacy, f)
        with open('termscondition.json', 'w') as f:
            json.dump(term, f)
        self.stdout.write(self.style.SUCCESS('Backup created successfully'))
