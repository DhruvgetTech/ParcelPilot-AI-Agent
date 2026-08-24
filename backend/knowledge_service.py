from backend.pdf_loader import load_pdf_text


documents = load_pdf_text()


def search_knowledge(query: str):
    query_words = query.lower().split()

    results = []

    for doc in documents:
        filename = doc["filename"].lower()
        content = doc["content"]

        # Deprecated documents ko current answers me use nahi karna
        if "deprecated" in filename:
            continue

        score = sum(
            content.lower().count(word)
            for word in query_words
            if len(word) > 2
        )

        if score > 0:
            results.append({
                "filename": doc["filename"],
                "score": score,
                "content": content[:3000]
            })

    results.sort(key=lambda x: x["score"], reverse=True)

    return results[:3]


if __name__ == "__main__":
    results = search_knowledge("cancellation policy")

    for result in results:
        print("\n" + "=" * 60)
        print("FILE:", result["filename"])
        print("SCORE:", result["score"])
        print("=" * 60)
        print(result["content"][:1000])