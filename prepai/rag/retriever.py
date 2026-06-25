import chromadb
from typing import List, Dict


def get_user_context(query_text: str, top_k: int = 3, db_path: str = "./chroma_db") -> List[Dict[str, any]]:
    """
    Search the user_profile collection for relevant chunks based on query text.

    Args:
        query_text: The search query (e.g., "Python experience" or "leadership skills")
        top_k: Number of most relevant chunks to return (default: 3)
        db_path: Path to ChromaDB persistent storage (default: "./chroma_db")

    Returns:
        List of dictionaries containing:
        - text: The chunk text content
        - source: Document source ("resume")
        - chunk_index: Position in the original document (0-based)

    Example return:
        [
            {
                "text": "Experienced software engineer with 5 years...",
                "source": "resume",
                "chunk_index": 0
            },
            ...
        ]
    """
    # Initialize ChromaDB persistent client
    # Connect to the same database where documents were stored
    client = chromadb.PersistentClient(path=db_path)

    try:
        # Get the user_profile collection
        # This collection was created during ingestion phase
        collection = client.get_collection(name="user_profile")

    except Exception as e:
        # If collection doesn't exist, return empty list
        print(f"Warning: user_profile collection not found: {e}")
        return []

    # Check if collection has any documents
    if collection.count() == 0:
        print("Warning: user_profile collection is empty")
        return []

    # Query the collection
    # ChromaDB will automatically embed the query_text and find similar chunks
    results = collection.query(
        query_texts=[query_text],  # The search query
        n_results=top_k  # Number of results to return
    )

    # Parse and format the results
    chunks = []

    # Results structure: results['documents'][0] = list of text chunks
    #                    results['metadatas'][0] = list of metadata dicts
    if results['documents'] and len(results['documents'][0]) > 0:
        for i in range(len(results['documents'][0])):
            chunk = {
                "text": results['documents'][0][i],  # The chunk text
                "source": "resume",  # Document source
                "chunk_index": results['metadatas'][0][i].get('chunk_index', i)  # Position in document
            }
            chunks.append(chunk)

    return chunks


def get_job_context(query_text: str, top_k: int = 3, db_path: str = "./chroma_db") -> List[Dict[str, any]]:
    """
    Search the job_context collection for relevant chunks based on query text.

    Args:
        query_text: The search query (e.g., "required qualifications" or "tech stack")
        top_k: Number of most relevant chunks to return (default: 3)
        db_path: Path to ChromaDB persistent storage (default: "./chroma_db")

    Returns:
        List of dictionaries containing:
        - text: The chunk text content
        - source: Document source ("job_description")
        - chunk_index: Position in the original document (0-based)

    Example return:
        [
            {
                "text": "We're seeking an exceptional Senior Backend Engineer...",
                "source": "job_description",
                "chunk_index": 0
            },
            ...
        ]
    """
    # Initialize ChromaDB persistent client
    # Connect to the same database where documents were stored
    client = chromadb.PersistentClient(path=db_path)

    try:
        # Get the job_context collection
        # This collection was created during ingestion phase
        collection = client.get_collection(name="job_context")

    except Exception as e:
        # If collection doesn't exist, return empty list
        print(f"Warning: job_context collection not found: {e}")
        return []

    # Check if collection has any documents
    if collection.count() == 0:
        print("Warning: job_context collection is empty")
        return []

    # Query the collection
    # ChromaDB will automatically embed the query_text and find similar chunks
    results = collection.query(
        query_texts=[query_text],  # The search query
        n_results=top_k  # Number of results to return
    )

    # Parse and format the results
    chunks = []

    # Results structure: results['documents'][0] = list of text chunks
    #                    results['metadatas'][0] = list of metadata dicts
    if results['documents'] and len(results['documents'][0]) > 0:
        for i in range(len(results['documents'][0])):
            chunk = {
                "text": results['documents'][0][i],  # The chunk text
                "source": "job_description",  # Document source
                "chunk_index": results['metadatas'][0][i].get('chunk_index', i)  # Position in document
            }
            chunks.append(chunk)

    return chunks
