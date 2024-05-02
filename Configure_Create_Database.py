from langchain.document_loaders import DirectoryLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.schema import Document
from langchain.embeddings import OpenAIEmbeddings
from langchain.vectorstores.chroma import Chroma
import os
import shutil


class configure_create_database:
    def __init__(self, db_path, directory_path, openapi_apikey):  # initializing database path and directory path containing pdf docs
        self._db = db_path
        self._directory = directory_path
        os.environ["OPENAI_API_KEY"] = openapi_apikey

    def load_docs(self):  # loading documents
        doc_loader = DirectoryLoader(self._directory, glob="*.pdf")
        docs = doc_loader.load()
        self._docs = docs
        print(f'Documents loaded successfully from {self._directory}')
        # return docs

    def doc_splitter(self, docs=None):  # splitting docs in chunks for embedding

        if docs is None:
            docs = self._docs
        splitter = RecursiveCharacterTextSplitter(
            chunk_size=1000,
            chunk_overlap=200,
            length_function=len,
            add_start_index=True,
        )
        chunks = splitter.split_documents(docs)
        print(f'{len(docs)} splitted into {len(chunks)} chunks')
        self._chunks = chunks
        # return chunks

    def save_db(self, chunks=None):  # store chunks in db after embedding

        if chunks is None:
            chunks = self._chunks
        if os.path.exists(self._db):
            shutil.rmtree(self._db)

        db = Chroma.from_documents(
            chunks, OpenAIEmbeddings(), persist_directory=self._db
        )
        db.persist()
        print(f'{len(chunks)} successfully stored in {self._db} path')