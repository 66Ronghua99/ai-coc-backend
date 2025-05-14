#!/usr/bin/env python3
"""
Example script for searching Call of Cthulhu rulebook content using PGVectorStorage.
"""

import sys
from pgvector_storage import PGVectorStorage

def search_specific_document(storage, document_name, query, limit=5):
    """Search for content in a specific document."""
    print(f"\n=== Searching for '{query}' in {document_name} ===\n")
    
    results = storage.search_document(
        document_name=document_name,
        query=query,
        limit=limit
    )
    
    if not results:
        print(f"No results found in {document_name} for query: '{query}'")
        return
    
    for i, result in enumerate(results, 1):
        print(f"Result {i} (Similarity: {result['similarity']:.4f})")
        print(f"Page: {result['page']}")
        print(f"Content excerpt: {result['content'][:150]}...")
        print("-" * 80)

def search_all_documents(storage, query, limit=3):
    """Search for content across all documents."""
    print(f"\n=== Searching for '{query}' across all documents ===\n")
    
    all_results = storage.search_all_documents(
        query=query,
        limit=limit
    )
    
    if not all_results:
        print(f"No results found in any document for query: '{query}'")
        return
    
    for doc_name, results in all_results.items():
        print(f"\n== Results from {doc_name} ==\n")
        
        for i, result in enumerate(results, 1):
            print(f"Result {i} (Similarity: {result['similarity']:.4f})")
            print(f"Page: {result['page']}")
            print(f"Content excerpt: {result['content'][:150]}...")
            print("-" * 80)

def main():
    """Main function."""
    # Initialize storage with default connection parameters
    # Modify these if your PostgreSQL setup is different
    storage = PGVectorStorage(
        host="localhost",
        port=5432,
        dbname="coc_db",
        user="postgres",
        password="postgres"
    )
    
    # Example 1: Search in a specific document
    search_specific_document(
        storage,
        document_name="investigator.pdf",
        query="How to create a character?",
        limit=3
    )
    
    # Example 2: Search for game mechanics in specific documents
    search_specific_document(
        storage,
        document_name="sanity.pdf",
        query="Sanity loss mechanics",
        limit=3
    )
    
    # Example 3: Search for combat rules
    search_specific_document(
        storage,
        document_name="battle.pdf",
        query="How does combat work?",
        limit=3
    )
    
    # Example 4: Search across all documents
    search_all_documents(
        storage,
        query="Cthulhu mythos",
        limit=2
    )
    
    # Example 5: Search for specific game term across all documents
    search_all_documents(
        storage,
        query="Luck roll",
        limit=2
    )

if __name__ == "__main__":
    main() 