from celery import shared_task
import csv
import io
import shutil
from apps.article.models import Article


@shared_task(autoretry_for=(Exception,), retry_backoff=True, max_retries=5, name='import', queue='import_csv')
def import_article_from_csv_task(csv_text):
   reader = csv.DictReader(io.StringIO(csv_text))
   articles = []
   for row in reader:
       articles.append(Article(**row))
   Article.objects.bulk_create(articles)

@shared_task(autoretry_for=(Exception,), retry_backoff=True, max_retries=5)
def clear_specific_folder_task(path):
   shutil.rmtree(path)



