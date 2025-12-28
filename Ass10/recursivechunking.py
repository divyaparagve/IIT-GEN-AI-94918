
# 2. Recursive Character Chunking
from langchain_text_splitters import RecursiveCharacterTextSplitter

text_splitter = RecursiveCharacterTextSplitter(
    chunk_size=800,
    chunk_overlap=100,
    separators=["\n\n", "\n", " ", ""]
)

raw_text = """
LangChain is a powerful framework designed to simplify the development of applications
that use large language models. It provides modular components for prompt management,
chains, agents, memory, and retrieval-augmented generation (RAG).

In real-world applications, documents often contain mixed formatting such as paragraphs,
sentences, bullet points, and line breaks. Simple character-based chunking may break
important semantic boundaries, which can reduce the quality of embeddings.

Recursive character chunking addresses this problem by attempting to split text using
larger semantic units first, such as paragraphs. If a paragraph is too large, it then
tries sentence boundaries, followed by words, and finally characters as a last resort.

This approach preserves contextual meaning more effectively, making it ideal for tasks
such as document search, question answering, and knowledge base construction.
"""

docs = text_splitter.create_documents([raw_text])
print("len", len(docs),"vect:", docs[0])



# Good for mixed formatting (paragraphs, sentences, bullet points)
# It try paragraph → sentence → word boundaries
# And preserves semantic meaning better