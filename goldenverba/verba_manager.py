import os
import ssl

import weaviate

from typing import Optional
from weaviate import Client
from weaviate.embedded import EmbeddedOptions
from wasabi import msg

from goldenverba.components.reader.manager import ReaderManager
from goldenverba.components.chunking.manager import ChunkerManager
from goldenverba.components.embedding.manager import EmbeddingManager
from goldenverba.components.retriever.manager import RetrieverManager
from goldenverba.components.generation.manager import GeneratorManager
from goldenverba.components.reader.document import Document
from goldenverba.components.chunking.chunk import Chunk
from goldenverba.components.reader.interface import Reader
from goldenverba.components.chunking.interface import Chunker
from goldenverba.components.embedding.interface import Embedder
from goldenverba.components.retriever.interface import Retriever
from goldenverba.components.generation.interface import Generator

from goldenverba.components.component import VerbaComponent

import goldenverba.components.schema.schema_generation as schema_manager

from dotenv import load_dotenv

load_dotenv()


class VerbaManager:
    """Manages all Verba Components"""

    def __init__(self) -> None:
        self.reader_manager = ReaderManager()
        self.chunker_manager = ChunkerManager()
        self.embedder_manager = EmbeddingManager()
        self.retriever_manager = RetrieverManager()
        self.generator_manager = GeneratorManager()
        self.environment_variables = {}
        self.installed_libraries = {}
        self.weaviate_type = ""
        self.client = self.setup_client()

        self.verify_installed_libraries()
        self.verify_variables()

        # Check if all schemas exist for all possible vectorizers
        for vectorizer in schema_manager.VECTORIZERS:
            schema_manager.init_schemas(self.client, vectorizer, False, True)

        for embedding in schema_manager.EMBEDDINGS:
            schema_manager.init_schemas(self.client, embedding, False, True)

    def import_data(
        self,
        bytes: list[str],
        contents: list[str],
        paths: list[str],
        fileNames: list[str],
        document_type: str,
        units: int = 100,
        overlap: int = 50,
    ) -> list[Document]:
        loaded_documents = self.reader_manager.load(
            bytes, contents, paths, fileNames, document_type
        )

        filtered_documents = []

        # Check if document names exist in DB
        for document in loaded_documents:
            if not self.check_if_document_exits(document):
                filtered_documents.append(document)

        modified_documents = self.chunker_manager.chunk(
            filtered_documents, units, overlap
        )

        if self.embedder_manager.embed(modified_documents, client=self.client):
            msg.good("Embedding successful")
            return modified_documents
        else:
            msg.fail("Embedding failed")
            return []

    def reader_set_reader(self, reader: str) -> bool:
        available, message = self.check_verba_component(
            self.reader_manager.readers[reader]
        )

        if available:
            msg.good(f"Set Reader to {reader}")
            return self.reader_manager.set_reader(reader)
        else:
            msg.warn(message)
            return False

    def reader_get_readers(self) -> dict[str, Reader]:
        return self.reader_manager.get_readers()

    def chunker_set_chunker(self, chunker: str) -> bool:
        available, message = self.check_verba_component(
            self.chunker_manager.chunker[chunker]
        )
        if available:
            msg.good(f"Set Chunker to {chunker}")
            return self.chunker_manager.set_chunker(chunker)
        else:
            msg.warn(message)
            return False

    def chunker_get_chunker(self) -> dict[str, Chunker]:
        return self.chunker_manager.get_chunkers()

    def embedder_set_embedder(self, embedder: str) -> bool:
        available, message = self.check_verba_component(
            self.embedder_manager.embedders[embedder]
        )
        if available:
            msg.good(f"Set Embedder to {embedder}")
            return self.embedder_manager.set_embedder(embedder)
        else:
            msg.warn(message)
            return False

    def embedder_get_embedder(self) -> dict[str, Embedder]:
        return self.embedder_manager.get_embedders()

    def retriever_set_retriever(self, retriever: str) -> bool:
        available, message = self.check_verba_component(
            self.retriever_manager.retrievers[retriever]
        )
        if available:
            msg.good(f"Set Retriever to {retriever}")
            return self.retriever_manager.set_retriever(retriever)
        else:
            msg.warn(message)
            return False

    def retriever_get_retriever(self) -> dict[str, Retriever]:
        return self.retriever_manager.get_retrievers()

    def generator_set_generator(self, generator: str) -> bool:
        available, message = self.check_verba_component(
            self.generator_manager.generators[generator]
        )
        if available:
            msg.good(f"Set Generator to {generator}")
            return self.generator_manager.set_generator(generator)
        else:
            msg.warn(message)
            return False

    def generator_get_generator(self) -> dict[str, Generator]:
        return self.generator_manager.get_generators()

    def setup_client(self) -> Optional[Client]:
        """
        @returns Optional[Client] - The Weaviate Client
        """

        msg.info("Setting up client")

        additional_header = {}
        client = None

        # Check OpenAI ENV KEY
        try:
            import openai

            openai_key = os.environ.get("OPENAI_API_KEY", "")
            if openai_key != "":
                additional_header["X-OpenAI-Api-Key"] = openai_key
                self.environment_variables["OPENAI_API_KEY"] = True
                openai.api_key = openai_key
                msg.info("OpenAI API key detected")
            else:
                self.environment_variables["OPENAI_API_KEY"] = False
        except Exception as e:
            self.environment_variables["OPENAI_API_KEY"] = False

        # Check Verba URL ENV
        weaviate_url = os.environ.get("VERBA_URL", "")
        if weaviate_url != "":
            weaviate_key = os.environ.get("VERBA_API_KEY", "")
            self.environment_variables["VERBA_URL"] = True
            self.weaviate_type = "Weaviate Cluster"
            auth_config = weaviate.AuthApiKey(api_key=weaviate_key)
            client = weaviate.Client(
                url=weaviate_url,
                additional_headers=additional_header,
                auth_client_secret=auth_config,
            )
        # Use Weaviate Embedded
        else:
            try:
                _create_unverified_https_context = ssl._create_unverified_context
            except AttributeError:
                pass
            else:
                ssl._create_default_https_context = _create_unverified_https_context

            msg.info("Using Weaviate Embedded")
            self.weaviate_type = "Weaviate Embedded"
            client = weaviate.Client(
                additional_headers={"X-OpenAI-Api-Key": openai.api_key},
                embedded_options=EmbeddedOptions(
                    persistence_data_path="./.verba/local/share/",
                    binary_path="./.verba/cache/weaviate-embedded",
                ),
            )

        if client != None:
            msg.good("Connected to Weaviate")

            # Batch Configuration
            def batch_callback(logs: dict):
                if logs is not None:
                    for result in logs:
                        if "result" in result and "errors" in result["result"]:
                            if "error" in result["result"]["errors"]:
                                msg.fail(result["result"])

            client.batch.configure(callback=batch_callback)

        else:
            msg.fail("Connection to Weaviate failed")

        return client

    def verify_installed_libraries(self) -> None:
        """
        Checks which libraries are installed and fills out the self.installed_libraries dictionary for the frontend to access
        """

        # spaCy, used for Chunking
        try:
            import spacy

            self.installed_libraries["spacy"] = True
        except Exception as e:
            self.installed_libraries["spacy"] = False

        try:
            import openai

            self.installed_libraries["openai"] = True
        except Exception as e:
            self.installed_libraries["openai"] = False

        try:
            import huggingface_hub
            from huggingface_hub import login

            login(token=os.environ.get("HF_TOKEN", ""), add_to_git_credential=True)

            self.installed_libraries["huggingface_hub"] = True
        except Exception as e:
            self.installed_libraries["huggingface_hub"] = False

        try:
            import transformers

            self.installed_libraries["transformers"] = True
        except Exception as e:
            self.installed_libraries["transformers"] = False

        try:
            import torch

            self.installed_libraries["torch"] = True
        except Exception as e:
            self.installed_libraries["torch"] = False

    def verify_variables(self) -> None:
        """
        Checks which environment variables are installed and fills out the self.environment_variables dictionary for the frontend to access
        """

        # OpenAI API Key
        if os.environ.get("OPENAI_API_KEY", "") != "":
            self.environment_variables["OPENAI_API_KEY"] = True
        else:
            self.environment_variables["OPENAI_API_KEY"] = False

        # HuggingFace Key
        if os.environ.get("HF_TOKEN", "") != "":
            self.environment_variables["HF_TOKEN"] = True
        else:
            self.environment_variables["HF_TOKEN"] = False

        # LLAMA2-7B-CHAT-HF
        if os.environ.get("LLAMA2-7B-CHAT-HF", "") != "":
            self.environment_variables["LLAMA2-7B-CHAT-HF"] = True
        else:
            self.environment_variables["LLAMA2-7B-CHAT-HF"] = False

    def get_schemas(self) -> dict:
        """
        @returns dict - A dictionary with the schema names and their object count
        """

        schema_info = self.client.schema.get()
        schemas = {}

        for _class in schema_info["classes"]:
            results = (
                self.client.query.get(_class["class"])
                .with_limit(100000)
                .with_additional(properties=["id"])
                .do()
            )

            schemas[_class["class"]] = len(results["data"]["Get"][_class["class"]])

        return schemas

    def retrieve_chunks(self, queries: list[str]) -> list[Chunk]:
        chunks, context = self.retriever_manager.retrieve(
            queries, self.client, self.embedder_manager.selected_embedder
        )
        return chunks, context

    def retrieve_all_documents(self, doc_type: str) -> list:
        """Return all documents from Weaviate
        @returns list - Document list
        """

        class_name = "Document_" + schema_manager.strip_non_letters(
            self.embedder_manager.selected_embedder.vectorizer
        )

        if doc_type == "":
            query_results = (
                self.client.query.get(
                    class_name=class_name,
                    properties=["doc_name", "doc_type", "doc_link"],
                )
                .with_additional(properties=["id"])
                .with_limit(10000)
                .do()
            )
        else:
            query_results = (
                self.client.query.get(
                    class_name=class_name,
                    properties=["doc_name", "doc_type", "doc_link"],
                )
                .with_additional(properties=["id"])
                .with_where(
                    {
                        "path": ["doc_type"],
                        "operator": "Equal",
                        "valueText": doc_type,
                    }
                )
                .with_limit(10000)
                .do()
            )

        results = query_results["data"]["Get"][class_name]
        return results

    def retrieve_document(self, doc_id: str) -> dict:
        """Return a document by it's ID (UUID format) from Weaviate
        @parameter doc_id : str - Document ID
        @returns dict - Document dict
        """
        class_name = "Document_" + schema_manager.strip_non_letters(
            self.embedder_manager.selected_embedder.vectorizer
        )

        document = self.client.data_object.get_by_id(
            doc_id,
            class_name=class_name,
        )
        return document

    async def generate_answer(
        self, queries: list[str], contexts: list[str], conversation: dict
    ):
        semantic_query = self.embedder_manager.selected_embedder.conversation_to_query(
            queries, conversation
        )
        (
            semantic_result,
            distance,
        ) = self.embedder_manager.selected_embedder.retrieve_semantic_cache(
            self.client, semantic_query
        )

        if semantic_result != None:
            return {
                "message": str(semantic_result),
                "finish_reason": "stop",
                "cached": True,
                "distance": distance,
            }

        else:
            full_text = await self.generator_manager.selected_generator.generate(
                queries, contexts, conversation
            )
            self.embedder_manager.selected_embedder.add_to_semantic_cache(
                self.client, semantic_query, full_text
            )
            return full_text

    async def generate_stream_answer(
        self, queries: list[str], contexts: list[str], conversation: dict
    ):
        semantic_query = self.embedder_manager.selected_embedder.conversation_to_query(
            queries, conversation
        )
        (
            semantic_result,
            distance,
        ) = self.embedder_manager.selected_embedder.retrieve_semantic_cache(
            self.client, semantic_query
        )

        if semantic_result != None:
            yield {
                "message": str(semantic_result),
                "finish_reason": "stop",
                "cached": True,
                "distance": distance,
            }

        else:
            full_text = ""
            async for result in self.generator_manager.selected_generator.generate_stream(
                queries, contexts, conversation
            ):
                full_text += result["message"]
                yield result

            self.embedder_manager.selected_embedder.add_to_semantic_cache(
                self.client, semantic_query, full_text
            )

    def reset(self):
        self.client.schema.delete_all()
        # Check if all schemas exist for all possible vectorizers
        for vectorizer in schema_manager.VECTORIZERS:
            schema_manager.init_schemas(self.client, vectorizer, False, True)

        for embedding in schema_manager.EMBEDDINGS:
            schema_manager.init_schemas(self.client, embedding, False, True)

    def reset_cache(self):
        # Check if all schemas exist for all possible vectorizers
        for vectorizer in schema_manager.VECTORIZERS:
            class_name = "Cache_" + schema_manager.strip_non_letters(vectorizer)
            self.client.schema.delete_class(class_name)
            schema_manager.init_schemas(self.client, vectorizer, False, True)

        for embedding in schema_manager.EMBEDDINGS:
            class_name = "Cache_" + schema_manager.strip_non_letters(embedding)
            self.client.schema.delete_class(class_name)
            schema_manager.init_schemas(self.client, embedding, False, True)

    def check_if_document_exits(self, document: Document) -> bool:
        """Return a document by it's ID (UUID format) from Weaviate
        @parameter document : Document - Document object
        @returns bool - Whether the doc name exist in the cluster
        """

        class_name = "Document_" + schema_manager.strip_non_letters(
            self.embedder_manager.selected_embedder.vectorizer
        )

        results = (
            self.client.query.get(
                class_name=class_name,
                properties=[
                    "doc_name",
                ],
            )
            .with_where(
                {
                    "path": ["doc_name"],
                    "operator": "Equal",
                    "valueText": document.name,
                }
            )
            .with_limit(1)
            .do()
        )

        if results["data"]["Get"][class_name]:
            msg.warn(f"{document.name} already exists")
            return True
        else:
            return False

    def check_verba_component(self, component: VerbaComponent) -> tuple[bool, str]:
        for library in component.requires_library:
            if library in self.installed_libraries:
                if not self.installed_libraries[library]:
                    return (False, f"{library} not installed")
            else:
                return (False, f"{library} not installed")

        for env in component.requires_env:
            if env in self.environment_variables:
                if not self.environment_variables[env]:
                    return (False, f"{env} not set")
            else:
                return (False, f"{env} not set")

        return (True, f"Available")

    def delete_document_by_id(self, doc_id: str) -> None:
        self.embedder_manager.selected_embedder.remove_document_by_id(
            self.client, doc_id
        )

    def search_documents(self, query: str, doc_type: str) -> list:
        return self.embedder_manager.selected_embedder.search_documents(
            self.client, query, doc_type
        )