import argparse
from dataclasses import dataclass
from langchain.vectorstores.chroma import Chroma
from langchain.embeddings import OpenAIEmbeddings
from langchain.chat_models import ChatOpenAI
from langchain.prompts import ChatPromptTemplate
import os

class query_processing:  # initializing chroma database path.
    def __init__(self, db_path, openapi_apikey):
        # self._query = query_text
        self._db = db_path
        os.environ["OPENAI_API_KEY"] = openapi_apikey

    def load_db(self):  # loading database
        embedding_function = OpenAIEmbeddings()
        db_loaded = Chroma(persist_directory=self._db, embedding_function=embedding_function)
        self._loaded_db = db_loaded

    def query_db(self, query):  # processing query
        results = self._loaded_db.similarity_search_with_relevance_scores(query, k=3)
        if len(results) == 0 or results[0][1] < 0.6:
            print(f"Unable to find matching results.")
            return

        PROMPT_TEMPLATE = """
      Answer the question based only on the following context:

      {context}

      ---

      Answer the question based on the above context: {question}
      """
        context_text = "\n\n---\n\n".join([doc.page_content for doc, _score in results])
        prompt_template = ChatPromptTemplate.from_template(PROMPT_TEMPLATE)
        prompt = prompt_template.format(context=context_text, question=query)
        print(prompt)

        model = ChatOpenAI()  # fetching response and the source of the response
        response_text = model.predict(prompt)

        sources = set([doc.metadata.get("source", None) for doc, _score in results])
        formatted_response = f"Response: {response_text}\nSources: {sources}"
        print(formatted_response)

        return prompt, response_text, sources
