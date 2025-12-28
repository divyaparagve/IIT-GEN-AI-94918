# 1. Basic Fixed-Size Chunking
from langchain_text_splitters import CharacterTextSplitter
from langchain_openai import OpenAIEmbeddings

text_splitter = CharacterTextSplitter(chunk_size=500, chunk_overlap=50)

raw_text = """LangChain is a framework for developing applications powered by large language models.
It enables chaining, memory, agents, and retrieval-augmented generation.
Text splitting is important to handle long documents efficiently."""

docs = text_splitter.create_documents([raw_text])
# Simple, but can split sentences unexpectedly
print("len", len(docs),"vect:", docs[0])
