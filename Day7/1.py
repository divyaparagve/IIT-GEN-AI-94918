from langchain_openai import OpenAIEmbeddings
import numpy as np

embeddings_model =OpenAIEmbeddings(
base_url="http://localhost:1234/v1", 
api_key="dummy-key",
model="text-embedding-nomic-embed-text-v1.5",
check_embedding_ctx_length=False
)
sentences=["I love football", "Soccer is my favoritesport", "You are irritating."]
embeddings=np.array(embeddings_model.embed_documents(sentences))