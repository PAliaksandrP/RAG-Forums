import requests
import chromadb


def fetch_stackoverflow_questions(tag="python", pages=8):
    """Получает вопросы с Stack Overflow по заданному тегу."""
    questions = []
    for page in range(1, pages + 1):
        url = f"https://api.stackexchange.com/2.3/questions?page={page}&pagesize=10&order=desc&sort=activity&tagged={tag}&site=stackoverflow"
        response = requests.get(url)
        if response.status_code == 200:
            data = response.json()
            for item in data.get("items", []):
                questions.append({
                    "id": item["question_id"],
                    "title": item["title"],
                    "link": item["link"],
                    "tags": item["tags"],
                })
    return questions


def store_in_chromadb(questions):
    """Сохраняет вопросы в ChromaDB."""
    client = chromadb.PersistentClient(path="./chromadb_store")
    collection = client.get_or_create_collection("stackoverflow")

    for question in questions:
        collection.add(
            ids=[str(question["id"])],
            documents=[question["title"]],
            metadatas=[{"link": question["link"], "tags": ", ".join(question["tags"])}]
        )
    print("Данные успешно сохранены в ChromaDB.")


if __name__ == "__main__":
    tag = "python"
    pages = 8  # Количество страниц для загрузки
    questions = fetch_stackoverflow_questions(tag, pages)
    store_in_chromadb(questions)
