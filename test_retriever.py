from rag import test_retriever

def test_retrieval_smoke_test():
    # Prints results for a narrow factual query and a broader conceptual query.
    test_retriever()

if __name__ == "__main__":
    test_retriever()
