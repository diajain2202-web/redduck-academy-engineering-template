# 04-content-derived-factory/src/factory.py
# A content-derived factory. Fill in create() and derive(). No framework required.
# Run with: python3 src/factory.py

import hashlib
import json


def create(content):
    """content is a dict of string fields, e.g. {"title": ..., "body": ..., "author": ...}.
    Return {"content": content, "id": <id>}, where id is derived from the content alone.
    """
    item_content = dict(content)
    return {"content": item_content, "id": derive(item_content)}


def derive(content):
    """Recompute the id from the content alone, with no registry and no shared state,
    so the demo passes.
    """
    canonical_content = json.dumps(
        content,
        sort_keys=True,
        separators=(",", ":"),
        ensure_ascii=False,
    ).encode("utf-8")
    return hashlib.sha256(canonical_content).hexdigest()


def demo():
    content = {
        "title": "Quarterly report",
        "body": "Revenue held steady.",
        "author": "avery",
    }

    item = create(content)

    # Second party holds only the content, in a different field order, and derives the id itself.
    same_content = {
        "author": "avery",
        "body": "Revenue held steady.",
        "title": "Quarterly report",
    }
    assert derive(same_content) == item["id"], "same content must derive the same id"

    # Tamper with one field. The derived id must no longer match the original.
    tampered = {**content, "body": "Revenue tripled."}
    assert derive(tampered) != item["id"], "changed content must change the id"

    print("ok:", item["id"])


if __name__ == "__main__":
    demo()
