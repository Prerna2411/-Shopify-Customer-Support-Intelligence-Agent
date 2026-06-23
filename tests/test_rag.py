from app.rag.retriever import retrieve_policies


def test_policy_retriever_finds_refund_policy():
    results = retrieve_policies("refund delayed shipment")
    assert results
    assert any("refund" in item["source"] for item in results)
