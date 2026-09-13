import math
import re
from typing import List, Dict, Tuple, Set


class TextVectorizer:
    """TF-IDF Vectorizer with BM25 scoring for fast, grounded transcript retrieval without heavy external models."""

    @staticmethod
    def tokenize(text: str) -> List[str]:
        return [w.lower() for w in re.findall(r"\b\w+\b", text)]

    @classmethod
    def compute_bm25_score(
        cls,
        query_tokens: List[str],
        doc_tokens: List[str],
        avg_doc_len: float,
        idf_dict: Dict[str, float],
        k1: float = 1.5,
        b: float = 0.75,
    ) -> float:
        if not doc_tokens:
            return 0.0

        doc_len = len(doc_tokens)
        doc_tf: Dict[str, int] = {}
        for token in doc_tokens:
            doc_tf[token] = doc_tf.get(token, 0) + 1

        score = 0.0
        for token in query_tokens:
            if token not in doc_tf:
                continue
            tf = doc_tf[token]
            idf = idf_dict.get(token, 0.0)
            numerator = tf * (k1 + 1)
            denominator = tf + k1 * (1 - b + b * (doc_len / avg_doc_len))
            score += idf * (numerator / denominator)

        return score

    @classmethod
    def calculate_idfs(cls, all_docs_tokens: List[List[str]]) -> Dict[str, float]:
        num_docs = len(all_docs_tokens)
        if num_docs == 0:
            return {}

        doc_freq: Dict[str, int] = {}
        for tokens in all_docs_tokens:
            seen: Set[str] = set(tokens)
            for token in seen:
                doc_freq[token] = doc_freq.get(token, 0) + 1

        idf_dict: Dict[str, float] = {}
        for token, freq in doc_freq.items():
            idf_dict[token] = math.log((num_docs - freq + 0.5) / (freq + 0.5) + 1)

        return idf_dict
