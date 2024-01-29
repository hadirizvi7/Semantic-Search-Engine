import requests, sys
from dbutils import Pinecone
from embedding import Embedding
from secrets import get_secret

class Extract:

    def __init__(self):
        API_KEY = get_secret()['NEWS_KEY']
        self.endpoint = url = f'https://newsapi.org/v2/top-headlines?country=us&apiKey={API_KEY}'

    def addData(self):
        response = requests.get(self.endpoint)
        if response.status_code != 200:
            print(response.status_code)
            sys.exit(99)
        
        data = response.json()
        for item in data['articles']:
            if item['source']['id'] == None:
                continue
            source = item['source']['name']
            title = item['title']
            description = item['description']
            url = item['url']

            #Derive vector embedding from input text
            vector = Embedding.get_embedding(description)

            #Package finalized object and push to pinecone DB
            output = {
                "source": source,
                "title": title,
                "description": description,
                "url": url,
                "vector": vector
                }
            
            db = Pinecone("search-engine")
            db.upsert(output)
            #Pinecone().upsert(output)

if __name__ ==  "__main__":
    Extract().addData()