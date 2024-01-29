from embedding import Embedding
from dbutils import Pinecone
from dbutils import Pinecone
import sys

class Search:
    
    def __init__(self, input_text):
        self.input_text = input_text
    
    def search(self):
        search_term = self.input_text
        search_vector = Embedding.get_embedding(search_term)
        #output = query({"vector": search_vector})
        output = {"vector": search_vector}
        db = Pinecone("search-engine")
        results = db.query(output)
        for item in results['matches']:
            print("---------------")
            print(item['metadata']['title'])
            print(item['metadata']['source'])
            print(item['metadata']['url'])


if __name__ == "__main__":
    search_term = sys.argv[1]
    search_object = Search(input_text=search_term)
    search_object.search()