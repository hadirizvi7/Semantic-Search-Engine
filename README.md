# Semantic Search Engine

This simple search engine leverages functionality from the OpenAI API and Pinecone to provide dynamic query results. Search queries are converted into vector embeddings and subsequently compared to articles maintained in a Pinecone vector database. Comparison is done via cosine similarity and then returned to the user in a minimalistic UI.

## Source Data

The [News API](https://newsapi.org/) is being used here in order to populate our vector database. This script is being run on a recurring basis, guaranteeing recent search results for end users. More specifically, we're hitting the "Top Headlines" endpoint.

## Database Setup

Once an API key is instantiated, you'll have to setup an index where vector embeddings can be stored:

```python
from pinecone import Pinecone

pc = Pinecone(api_key='YOUR_API_KEY')

pc.create_index(
    name="quickstart",
    dimension=1536,
    metric="cosine",
) 
```

From here, any new vector embeddings can be upserted/queried. Refer to `backend/dbutils.py` for implementation details.

Along with this, the following APIs are being utilized:

1. **News API**

Top articles for a given day are converted to vector embeddings and stored in Pinecone, along with relevant metadata (source, title, URL, etc.). Refer to `backend/extract.py` for specifics.

2. **OpenAI API**

In order to convert text data to vector embeddings, the following custom function is used:

```python
def get_embedding(text):
    openai.api_key = get_secret()['OPENAI_KEY']
    response = openai.Embedding.create(
    model= "text-embedding-ada-002",
    input=[text]
    )
    # Extract the AI output embedding as a list of floats
    embedding = response["data"][0]["embedding"]

    return embedding
```

This will return a vector of length 1536, which is standardized across embedded vectors returned.

Once the API configurations are set, you can execute the application as follows:

### 1. Download the repository to your Local Device

```bash
git clone https://github.com/hadirizvi7/Semantic-Search-Engine.git
```

### 2. Install the necessary libraries/dependencies

```bash
pip3 install -r requirements.txt
```

### 3. Startup the Application

```bash
flask run
```

If everything goes as expected, you should be provided a search box. Once a search term is provided, the top 3 results will be returned to the user (based on Cosine Similarity of the existing dataset).

## Next Steps

1. **Historical Backfill of Data**

Since the extract process only started in January of 2024, no results prior to this date would be returned to the user (leading to potential gaps in relevance of results). Doing a one-time population of our Pinecone database is computationally expensive, hence the need for a workaround that will backfill any gaps.

2. **Integration of Third Party Services**

Currently, the web UI is strictly related to search features.In order to enhance our frontend component, integrating third party features such as login authorization and location services would significantly improve the user experience.