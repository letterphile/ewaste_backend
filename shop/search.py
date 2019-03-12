from django.contrib.postgres.search import TrigramSimilarity
from shop.models import *


results = Device.objects.annotate(similarity=TrigramSimilarity('name', "apple"),).filter(similarity__gt=0.0).order_by('-similarity')
print(results)