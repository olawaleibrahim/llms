import os
import warnings

os.environ["CUDA_VISIBLE_DEVICES"] = "0"
os.environ["WORLD_SIZE"] = "1"

from llama_index.core import Settings
from llama_index.llms.groq import Groq
from llama_index.core.node_parser import SentenceSplitter
from llama_index.embeddings.huggingface import HuggingFaceEmbedding
from llama_index.core import (
    VectorStoreIndex,
    SimpleDirectoryReader,
    StorageContext,
    load_index_from_storage
)

os.environ["CUDA_VISIBLE_DEVICES"] = "0"
os.environ["WORLD_SIZE"] = "1"

warnings.filterwarnings('ignore')

os.environ["GROQ_API_KEY"] = "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"
GROQ_API_KEY = os.getenv("GROQ_API_KEY")

prompt_template = """
    Use the following pieces of information to answer the user's question.
    If you don't know the answer, just say that you don't know, don't try to make up an answer.

    Context: {context}
    Question: {question}

    Answer the question and provide additional helpful information,
    based on the pieces of information, if applicable. Be succinct.

    Responses should be properly formatted to be easily read.
"""

CONTEXT = "This directory contains multiple academic documents on large language models (llms) and NLP research"
DIRECTORY_PATH = "/home/olawale/Desktop/PROJECTS/llms/beyond-abstracts/data/upload/"
EMBED_MODEL = HuggingFaceEmbedding(
    model_name="sentence-transformers/all-MiniLM-L6-v2")
LLM = Groq(model="llama3-70b-8192", api_key=GROQ_API_KEY)


def create_query_engine(data_path, llm=LLM, context=CONTEXT):
    reader = SimpleDirectoryReader(input_dir=data_path)
    documents = reader.load_data()
    text_splitter = SentenceSplitter(chunk_size=1024, chunk_overlap=200)
    nodes = text_splitter.get_nodes_from_documents(
        documents, show_progress=True)
    Settings.llm = LLM
    Settings.embed_model = EMBED_MODEL
    vector_index = VectorStoreIndex.from_documents(
        documents, show_progress=True, node_parser=nodes)
    vector_index.storage_context.persist(persist_dir="./storage_mini")
    storage_context = StorageContext.from_defaults(
        persist_dir="./storage_mini")
    index = load_index_from_storage(storage_context)
    query_engine = index.as_query_engine()

    return query_engine


# query_engine = create_query_engine(data_path=DIRECTORY_PATH,)
