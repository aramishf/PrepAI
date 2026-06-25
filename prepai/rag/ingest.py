import chromadb
from chromadb.config import Settings


def load_and_chunk_text(file_path: str, chunk_size: int = 200, overlap: int = 20) -> list[str]:
    """
    Load a text file and split it into overlapping chunks.

    Args:
        file_path: Path to the .txt file to load
        chunk_size: Number of words per chunk (default: 200)
        overlap: Number of words to overlap between chunks (default: 20)

    Returns:
        List of text chunks as strings

    Raises:
        FileNotFoundError: If the file doesn't exist
        ValueError: If overlap >= chunk_size
    """
    # Validate parameters
    if overlap >= chunk_size:
        raise ValueError(f"Overlap ({overlap}) must be less than chunk_size ({chunk_size})")

    # Load the text file
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            text = f.read()
    except FileNotFoundError:
        raise FileNotFoundError(f"File not found: {file_path}")

    # Split text into words (by whitespace)
    words = text.split()

    # If text is shorter than chunk_size, return as single chunk
    if len(words) <= chunk_size:
        return [text]

    # Create overlapping chunks
    chunks = []
    start_idx = 0

    while start_idx < len(words):
        # Get chunk_size words starting from start_idx
        end_idx = start_idx + chunk_size
        chunk_words = words[start_idx:end_idx]

        # Join words back into text
        chunk_text = ' '.join(chunk_words)
        chunks.append(chunk_text)

        # Move start_idx forward by (chunk_size - overlap) for next chunk
        # This creates the overlap
        start_idx += (chunk_size - overlap)

        # Break if we've processed all words
        if end_idx >= len(words):
            break

    return chunks


def store_chunks_in_collection(collection_name: str, chunks: list[str], db_path: str = "./chroma_db") -> chromadb.Collection:
    """
    Store text chunks in a ChromaDB collection with automatic embeddings.

    Args:
        collection_name: Name of the ChromaDB collection (e.g., "user_profile" or "job_context")
        chunks: List of text chunks to store
        db_path: Path to ChromaDB persistent storage directory (default: "./chroma_db")

    Returns:
        The ChromaDB collection object

    Raises:
        ValueError: If chunks list is empty
    """
    # Validate input
    if not chunks:
        raise ValueError("Chunks list cannot be empty")

    # Initialize ChromaDB persistent client
    # Data will be saved to disk at db_path location
    client = chromadb.PersistentClient(path=db_path)

    # Get or create collection
    # ChromaDB will use default embedding function (sentence-transformers)
    # If collection exists, it will be retrieved; otherwise created
    collection = client.get_or_create_collection(
        name=collection_name,
        metadata={"description": f"Collection for {collection_name}"}
    )

    # Generate unique IDs for each chunk
    # Format: "chunk_0", "chunk_1", "chunk_2", etc.
    ids = [f"chunk_{i}" for i in range(len(chunks))]

    # Create metadata for each chunk
    # Includes the chunk index for tracking
    metadatas = [{"chunk_index": i} for i in range(len(chunks))]

    # Add chunks to collection
    # ChromaDB will automatically generate embeddings using its built-in function
    collection.add(
        documents=chunks,  # The text chunks
        ids=ids,          # Unique identifiers
        metadatas=metadatas  # Metadata for each chunk
    )

    return collection
