import openai
from .s3secrets import get_secret

class Embedding:
    
    def get_embedding(text):
        openai.api_key = get_secret()['OPENAI_KEY']
        response = openai.Embedding.create(
        model= "text-embedding-ada-002",
        input=[text]
        )
        # Extract the AI output embedding as a list of floats
        embedding = response["data"][0]["embedding"]

        return embedding