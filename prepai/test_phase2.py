"""
Test script for Phase 2: Data Ingestion
Tests loading, chunking, and storing documents in ChromaDB collections
"""
import os
import sys

# Add parent directory to path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from rag.ingest import load_and_chunk_text, store_chunks_in_collection

def test_ingestion():
    """Test the complete ingestion pipeline"""

    print("=" * 60)
    print("PHASE 2 TEST: Data Ingestion")
    print("=" * 60)

    # Define file paths
    resume_path = os.path.join(os.path.dirname(__file__), "data", "resume.txt")
    job_desc_path = os.path.join(os.path.dirname(__file__), "data", "job_description.txt")

    print("\n1. Loading and chunking resume.txt...")
    # Load and chunk resume
    resume_chunks = load_and_chunk_text(resume_path, chunk_size=200, overlap=20)
    print(f"   ✓ Resume loaded and chunked into {len(resume_chunks)} chunks")

    print("\n2. Loading and chunking job_description.txt...")
    # Load and chunk job description
    job_chunks = load_and_chunk_text(job_desc_path, chunk_size=200, overlap=20)
    print(f"   ✓ Job description loaded and chunked into {len(job_chunks)} chunks")

    print("\n3. Storing resume chunks in 'user_profile' collection...")
    # Store resume chunks in ChromaDB
    user_profile_collection = store_chunks_in_collection(
        collection_name="user_profile",
        chunks=resume_chunks
    )
    stored_resume_count = user_profile_collection.count()
    print(f"   ✓ Stored {stored_resume_count} chunks in 'user_profile' collection")

    print("\n4. Storing job description chunks in 'job_context' collection...")
    # Store job description chunks in ChromaDB
    job_context_collection = store_chunks_in_collection(
        collection_name="job_context",
        chunks=job_chunks
    )
    stored_job_count = job_context_collection.count()
    print(f"   ✓ Stored {stored_job_count} chunks in 'job_context' collection")

    print("\n" + "=" * 60)
    print("RESULTS SUMMARY")
    print("=" * 60)
    print(f"✓ user_profile collection: {stored_resume_count} chunks")
    print(f"✓ job_context collection: {stored_job_count} chunks")
    print(f"✓ Total chunks stored: {stored_resume_count + stored_job_count}")
    print("\n✓ Phase 2 test completed successfully!")
    print("=" * 60)

if __name__ == "__main__":
    test_ingestion()
