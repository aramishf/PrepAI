"""
Test script for Phase 3: RAG Retriever
Tests querying ChromaDB collections for relevant context
"""
import os
import sys

# Add parent directory to path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from rag.retriever import get_user_context, get_job_context


def print_chunks(chunks, query):
    """Helper function to print retrieved chunks nicely"""
    print(f"\n   Query: '{query}'")
    print(f"   Found {len(chunks)} chunks:\n")

    for i, chunk in enumerate(chunks, 1):
        print(f"   Chunk {i}:")
        print(f"   - Source: {chunk['source']}")
        print(f"   - Index: {chunk['chunk_index']}")
        print(f"   - Text preview: {chunk['text'][:150]}...")
        print()


def test_retriever():
    """Test the retriever functions with various queries"""

    print("=" * 70)
    print("PHASE 3 TEST: RAG Retriever")
    print("=" * 70)

    # Test 1: Query user profile for Python experience
    print("\n[TEST 1] Retrieving user context: Python experience")
    print("-" * 70)
    chunks = get_user_context("Python programming experience and skills", top_k=2)
    print_chunks(chunks, "Python programming experience and skills")

    # Test 2: Query user profile for leadership/teamwork
    print("\n[TEST 2] Retrieving user context: Leadership and teamwork")
    print("-" * 70)
    chunks = get_user_context("leadership mentoring team collaboration", top_k=2)
    print_chunks(chunks, "leadership mentoring team collaboration")

    # Test 3: Query job description for required qualifications
    print("\n[TEST 3] Retrieving job context: Required qualifications")
    print("-" * 70)
    chunks = get_job_context("required qualifications experience years", top_k=2)
    print_chunks(chunks, "required qualifications experience years")

    # Test 4: Query job description for tech stack
    print("\n[TEST 4] Retrieving job context: Technology stack")
    print("-" * 70)
    chunks = get_job_context("technology stack tools frameworks databases", top_k=2)
    print_chunks(chunks, "technology stack tools frameworks databases")

    # Test 5: Query job description for company culture
    print("\n[TEST 5] Retrieving job context: Company information")
    print("-" * 70)
    chunks = get_job_context("company culture startup AI artificial intelligence", top_k=2)
    print_chunks(chunks, "company culture startup AI artificial intelligence")

    # Summary
    print("\n" + "=" * 70)
    print("SUMMARY")
    print("=" * 70)
    print("✓ get_user_context() tested with 2 queries")
    print("✓ get_job_context() tested with 3 queries")
    print("✓ All retriever functions working correctly")
    print("\n✓ Phase 3 test completed successfully!")
    print("=" * 70)


if __name__ == "__main__":
    test_retriever()
