from app.vectorstore.chroma import get_collection


def main():
    data = get_collection().get(include=["metadatas"])
    for chunk_id, meta in zip(data["ids"], data["metadatas"]):
        print(chunk_id, "-", meta["source"], "-", meta["section"])


if __name__ == "__main__":
    main()