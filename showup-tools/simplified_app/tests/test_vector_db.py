import json
import os
import sys
from types import SimpleNamespace
import importlib.util

import pytest

REPO_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), "../../.."))
module_path = os.path.join(REPO_ROOT, "showup-tools", "simplified_app", "rag_system", "textbook_vector_db.py")
spec = importlib.util.spec_from_file_location("textbook_vector_db", module_path)
textbook_vector_db = importlib.util.module_from_spec(spec)
sys.modules["textbook_vector_db"] = textbook_vector_db
spec.loader.exec_module(textbook_vector_db)


class DummyFAISS:
    """Minimal FAISS replacement for tests."""

    def __init__(self, texts, embeddings, metadatas=None):
        self.data = [SimpleNamespace(page_content=t, metadata=m or {})
                     for t, m in zip(texts, metadatas or [{}] * len(texts))]

    @classmethod
    def from_texts(cls, texts, embeddings, metadatas=None):
        return cls(texts, embeddings, metadatas)

    def add_texts(self, texts, metadatas=None):
        self.data.extend(SimpleNamespace(page_content=t, metadata=m or {})
                         for t, m in zip(texts, metadatas or [{}] * len(texts)))

    def save_local(self, path):
        with open(path, "w", encoding="utf-8") as fh:
            json.dump([(d.page_content, d.metadata) for d in self.data], fh)

    @classmethod
    def load_local(cls, path, embeddings):
        with open(path, "r", encoding="utf-8") as fh:
            items = json.load(fh)
        texts, metas = zip(*items) if items else ([], [])
        return cls(list(texts), embeddings, list(metas))

    def similarity_search(self, query, k=3):
        results = [d for d in self.data if query.lower() in d.page_content.lower()]
        if not results:
            results = self.data
        return results[:k]


class DummyEmbeddings:
    def __init__(self, *args, **kwargs):
        pass


def test_index_and_query_reuse(tmp_path, monkeypatch):
    cache_dir = tmp_path / "cache"
    cache_dir.mkdir()

    monkeypatch.setattr(textbook_vector_db, "FAISS", DummyFAISS, raising=False)
    monkeypatch.setattr(textbook_vector_db, "HuggingFaceEmbeddings", DummyEmbeddings, raising=False)
    monkeypatch.setattr(textbook_vector_db, "VECTOR_LIBS_AVAILABLE", True, raising=False)

    db = textbook_vector_db.TextbookVectorDB(cache_dir=str(cache_dir))

    content = (
        "# Chapter 1\n" + "FooBarBaz is a unique term here. " * 10 +
        "\n\n# Chapter 2\n" + "Other content. " * 10
    )

    assert db.index_textbook(content, "sample", force_rebuild=True)
    first_index = cache_dir / "sample.faiss"
    first_meta = cache_dir / "sample.meta.json"
    assert first_index.exists() and first_meta.exists()
    first_index_mtime = first_index.stat().st_mtime
    first_meta_mtime = first_meta.stat().st_mtime

    results = db.query_textbook("sample", "FooBarBaz")
    assert results and "FooBarBaz" in results[0]["content"]

    # Second indexing should reuse existing files
    assert db.index_textbook(content, "sample", force_rebuild=False)
    assert first_index.stat().st_mtime == first_index_mtime
    assert first_meta.stat().st_mtime == first_meta_mtime

    second_results = db.query_textbook("sample", "FooBarBaz")
    assert second_results == results
