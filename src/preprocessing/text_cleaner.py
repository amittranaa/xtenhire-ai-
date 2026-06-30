"""NLTK-backed text normalization for resume intelligence."""

from __future__ import annotations

import re
from functools import lru_cache

import nltk
from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer


_FALLBACK_STOPWORDS = {
    "a", "an", "and", "are", "as", "at", "be", "by", "for", "from",
    "has", "in", "is", "it", "of", "on", "or", "that", "the", "to", "with",
}


@lru_cache(maxsize=1)
def init_nltk() -> tuple[set[str], WordNetLemmatizer]:
    """Download and load NLTK resources automatically."""
    try:
        nltk.data.find("corpora/stopwords")
    except LookupError:
        nltk.download("stopwords", quiet=True)
        
    try:
        nltk.data.find("corpora/wordnet")
    except LookupError:
        nltk.download("wordnet", quiet=True)
        
    try:
        nltk.data.find("corpora/omw-1.4")
    except LookupError:
        nltk.download("omw-1.4", quiet=True)

    try:
        stops = set(stopwords.words("english"))
    except Exception:
        stops = _FALLBACK_STOPWORDS

    lemmatizer = WordNetLemmatizer()
    return stops, lemmatizer


def normalize_whitespace(text: str) -> str:
    return re.sub(r"\s+", " ", text or "").strip()


def clean_text(text: str, *, lemmatize: bool = True) -> str:
    """Clean and normalize text for NLP and vector search."""
    text = (text or "").lower()
    text = re.sub(r"http\S+|www\.\S+", " ", text)
    text = re.sub(r"[^a-z0-9+#.\s-]", " ", text)
    text = normalize_whitespace(text)

    stops, lemmatizer = init_nltk()

    # Tokenize using regex (words and special tech terms like c++, .net, c#)
    # We want to keep words, +, #, . and -
    tokens_raw = re.findall(r"\b[a-z0-9+#.-]+\b|c\+\+|c#|\.net", text)
    
    tokens: list[str] = []
    for raw in tokens_raw:
        raw = raw.strip()
        if not raw or raw in stops or len(raw) <= 1:
            if raw not in {"c", "r"}:  # allow single letter R and C
                continue
                
        if raw in {"c++", "c#", ".net"}:
            tokens.append(raw)
            continue
            
        lemma = lemmatizer.lemmatize(raw) if lemmatize else raw
        if lemma and lemma not in stops:
            tokens.append(lemma)

    return " ".join(tokens)
