import pinecone
from secrets import get_secret

class Pinecone:
    #Instantiate connection to Pinecone DB
    def __init__(self, index_name):
        API_KEY = get_secret()['PINECONE_KEY']
        pinecone.init(api_key=API_KEY, environment="gcp-starter")
        self.index = pinecone.Index(index_name)

    def upsert(self, input_object):
        source,title,url,vector = input_object['source'],input_object['title'],input_object['url'],input_object['vector']
        index = self.index
        index.upsert(
            vectors=[
                (
                url,
                vector,
                {"title": title,"source":source, "url":url}
                )
            ],
            namespace="namespace"
        )

    def delete(self, vector_id):
        index = self.index
        index.delete(ids=[vector_id], namespace="namespace")

    def query(self, input_object):
        vector = input_object['vector']
        index = self.index
        query_response = index.query(
            namespace="namespace",
            top_k=3,
            include_values=False,
            include_metadata=True,
            vector=vector,
            #filter={
            #    "genre": {"$in": ["comedy", "documentary", "drama"]}
            # }
        )
        output = query_response.to_dict()
        return output