"""
Knowledge Base Manager for Wind Power AI Agents
Handles document loading, embedding, and retrieval using ChromaDB
"""
import os
from typing import List, Optional, Dict, Any
from pathlib import Path

from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.embeddings import OpenAIEmbeddings
from langchain.vectorstores import Chroma
from langchain.docstore.document import Document
from langchain.document_loaders import (
    PyPDFLoader,
    TextLoader,
    Docx2txtLoader,
)

from core.config import VectorDBConfig, get_config


class KnowledgeBase:
    """
    Knowledge base manager for document storage and retrieval
    """
    
    def __init__(self, config: Optional[VectorDBConfig] = None):
        """
        Initialize knowledge base
        
        Args:
            config: Vector DB configuration, uses global config if None
        """
        self.config = config or get_config().vector_db
        self.embeddings = OpenAIEmbeddings()
        self.text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=get_config().chunk_size,
            chunk_overlap=get_config().chunk_overlap,
        )
        self.vectorstore = None
        self._initialize_vectorstore()
    
    def _initialize_vectorstore(self):
        """Initialize or load vector store"""
        persist_dir = self.config.persist_directory
        
        # Check if vector store already exists
        if os.path.exists(persist_dir):
            self.vectorstore = Chroma(
                collection_name=self.config.collection_name,
                embedding_function=self.embeddings,
                persist_directory=persist_dir
            )
        else:
            # Create new vector store
            self.vectorstore = Chroma(
                collection_name=self.config.collection_name,
                embedding_function=self.embeddings,
                persist_directory=persist_dir
            )
    
    def load_document(self, file_path: str) -> List[Document]:
        """
        Load a single document
        
        Args:
            file_path: Path to the document
            
        Returns:
            List of Document objects
        """
        file_ext = Path(file_path).suffix.lower()
        
        if file_ext == ".pdf":
            loader = PyPDFLoader(file_path)
        elif file_ext == ".txt":
            loader = TextLoader(file_path)
        elif file_ext in [".docx", ".doc"]:
            loader = Docx2txtLoader(file_path)
        else:
            raise ValueError(f"Unsupported file type: {file_ext}")
        
        documents = loader.load()
        return documents
    
    def load_directory(self, directory: str) -> List[Document]:
        """
        Load all documents from a directory
        
        Args:
            directory: Path to directory
            
        Returns:
            List of Document objects
        """
        all_documents = []
        directory_path = Path(directory)
        
        if not directory_path.exists():
            raise ValueError(f"Directory does not exist: {directory}")
        
        # Supported file extensions
        supported_extensions = [".pdf", ".txt", ".docx", ".doc"]
        
        for file_path in directory_path.rglob("*"):
            if file_path.is_file() and file_path.suffix.lower() in supported_extensions:
                try:
                    documents = self.load_document(str(file_path))
                    all_documents.extend(documents)
                except Exception as e:
                    print(f"Error loading {file_path}: {e}")
        
        return all_documents
    
    def add_documents(self, documents: List[Document]) -> None:
        """
        Add documents to knowledge base
        
        Args:
            documents: List of documents to add
        """
        # Split documents into chunks
        chunks = self.text_splitter.split_documents(documents)
        
        # Add to vector store
        if self.vectorstore is None:
            self._initialize_vectorstore()
        
        self.vectorstore.add_documents(chunks)
        self.vectorstore.persist()
    
    def add_from_directory(self, directory: str) -> None:
        """
        Load and add all documents from a directory
        
        Args:
            directory: Path to directory
        """
        documents = self.load_directory(directory)
        self.add_documents(documents)
        print(f"Added {len(documents)} documents from {directory}")
    
    def search(
        self,
        query: str,
        k: Optional[int] = None
    ) -> List[Document]:
        """
        Search for relevant documents
        
        Args:
            query: Search query
            k: Number of results to return
            
        Returns:
            List of relevant documents
        """
        if self.vectorstore is None:
            return []
        
        k = k or get_config().top_k
        results = self.vectorstore.similarity_search(query, k=k)
        return results
    
    def search_with_score(
        self,
        query: str,
        k: Optional[int] = None
    ) -> List[tuple]:
        """
        Search for relevant documents with similarity scores
        
        Args:
            query: Search query
            k: Number of results to return
            
        Returns:
            List of (document, score) tuples
        """
        if self.vectorstore is None:
            return []
        
        k = k or get_config().top_k
        results = self.vectorstore.similarity_search_with_score(query, k=k)
        return results
    
    def clear(self) -> None:
        """Clear all documents from knowledge base"""
        if self.vectorstore is not None:
            # Delete the collection and reinitialize
            try:
                self.vectorstore._collection.delete()
            except:
                # If delete fails, try to reset by recreating
                pass
            self._initialize_vectorstore()


def create_knowledge_base(config: Optional[VectorDBConfig] = None) -> KnowledgeBase:
    """
    Factory function to create knowledge base
    
    Args:
        config: Optional vector DB configuration
        
    Returns:
        KnowledgeBase instance
    """
    return KnowledgeBase(config)
