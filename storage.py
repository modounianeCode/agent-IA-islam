import json
import csv
import os
from datetime import datetime

DATA_DIR = os.path.join(os.path.dirname(__file__), "data")


def _ensure_data_dir():
    os.makedirs(DATA_DIR, exist_ok=True)


def _get_filepath(doc_type):
    return os.path.join(DATA_DIR, f"{doc_type}.json")


def load_documents(doc_type):
    _ensure_data_dir()
    filepath = _get_filepath(doc_type)
    if not os.path.exists(filepath):
        return []
    with open(filepath, "r", encoding="utf-8") as f:
        return json.load(f)


def save_documents(doc_type, documents):
    _ensure_data_dir()
    filepath = _get_filepath(doc_type)
    with open(filepath, "w", encoding="utf-8") as f:
        json.dump(documents, f, ensure_ascii=False, indent=2)


def add_document(doc_type, document):
    documents = load_documents(doc_type)
    document["id"] = len(documents) + 1
    document["created_at"] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    documents.append(document)
    save_documents(doc_type, documents)
    return document


def get_document(doc_type, doc_id):
    documents = load_documents(doc_type)
    for doc in documents:
        if doc["id"] == doc_id:
            return doc
    return None


def delete_document(doc_type, doc_id):
    documents = load_documents(doc_type)
    documents = [d for d in documents if d["id"] != doc_id]
    save_documents(doc_type, documents)


def export_to_csv(doc_type):
    documents = load_documents(doc_type)
    if not documents:
        return None

    filepath = os.path.join(DATA_DIR, f"{doc_type}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv")
    headers = documents[0].keys()

    with open(filepath, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=headers)
        writer.writeheader()
        writer.writerows(documents)

    return filepath
