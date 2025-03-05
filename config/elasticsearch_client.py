import os
from dotenv import load_dotenv

from elasticsearch import Elasticsearch


load_dotenv()

ELASTICSEARCH_URL = os.getenv("ELASTICSEARCH_URL", "http://localhost:9200")
ELASTICSEARCH_USER = os.getenv("ELASTICSEARCH_USER", "elastic")
ELASTICSEARCH_PASSWORD = os.getenv("ELASTICSEARCH_PASSWORD", "elastic")

es = Elasticsearch(
    ELASTICSEARCH_URL,
    basic_auth=(ELASTICSEARCH_USER, ELASTICSEARCH_PASSWORD),
    verify_certs=False
)

def create_articles_index():

    if not es.indices.exists(index="articles"):
        es.indices.create(
            index="articles",
            body={
                "mappings": {
                    "properties": {
                        "title": {"type": "text"},
                        "description": {"type": "text"},
                        "slug": {"type": "keyword"},
                        "categories": {"type": "keyword"},
                        "user": {
                            "type": "object",
                            "properties": {
                                "name": {"type": "text"},
                                "email": {"type": "text"}
                            }
                        }
                    }
                }
            }
        )

        print("Created 'articles' index")

        return
    print("Already articles index exist")
