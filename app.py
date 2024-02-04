from flask import Flask,render_template,request
from backend.embedding import Embedding
from backend.dbutils import Pinecone
app = Flask(__name__)

@app.route('/static/<path:filename>')
def serve_static(filename):
  return app.send_static_file(filename)

@app.route('/')
def search_form():
  return render_template('search_form.html')

@app.route('/search')
def search():
  search_term = request.args.get('query')
  search_vector = Embedding.get_embedding(search_term)
  output = {"vector": search_vector}
  db = Pinecone("search-engine")
  results = db.query(output)
  output = []
  for idx, item in enumerate(results['matches']):
    title = item['metadata']['title']
    source = item['metadata']['source']
    url = item['metadata']['url']
    #obj = f"{title}\n{source}\n{url}"
    obj = f"""
    {title}
    {source}
    {url}
    """
    output.append(obj)
    
  return render_template('search_results.html', query=search_term, results=output)

if __name__ == '__main__':
  app.run(debug=False)