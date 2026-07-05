"""
KontractIQ - Hybrid Search Engine
search combining TF-IDF and BM25 with advanced features
"""

import numpy as np
from typing import List, Dict, Any, Tuple, Optional, Set
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from rank_bm25 import BM25Okapi
import re
from collections import Counter


class SearchEngine:
    """Hybrid search engine using TF-IDF and BM25 with advanced features"""
    
    def __init__(self):
        """Initialize the search engine"""
        self.vectorizer = None
        self.tfidf_matrix = None
        self.bm25 = None
        self.documents = []
        self.doc_ids = []
        self.corpus = []
        self.is_indexed = False
        self.word_frequencies = {}
        self.document_vectors = None
    
    def index_documents(self, documents: List[Dict[str, Any]]):
        """Index documents for search with advanced features"""
        if not documents:
            self.is_indexed = False
            return
        
        self.documents = documents
        self.doc_ids = [doc.get('id', str(i)) for i, doc in enumerate(documents)]
        self.corpus = [doc.get('text', '').lower() for doc in documents]
        
        # Clean corpus with advanced preprocessing
        self.corpus = [self._clean_text(text) for text in self.corpus]
        
        # Build word frequencies for advanced features
        self.word_frequencies = {}
        for text in self.corpus:
            words = text.split()
            for word in set(words):
                self.word_frequencies[word] = self.word_frequencies.get(word, 0) + 1
        
        # Create TF-IDF index with optimized parameters
        self.vectorizer = TfidfVectorizer(
            max_features=10000,  # Increased for better coverage
            stop_words='english',
            ngram_range=(1, 3),  # Added trigrams for better matching
            min_df=1,
            max_df=0.9,
            use_idf=True,
            smooth_idf=True,
            sublinear_tf=True
        )
        self.tfidf_matrix = self.vectorizer.fit_transform(self.corpus)
        
        # Create BM25 index with optimized parameters
        tokenized_corpus = [text.split() for text in self.corpus]
        self.bm25 = BM25Okapi(
            tokenized_corpus,
            k1=1.5,  # Slightly higher k1 for better term frequency impact
            b=0.75,  # Slightly lower b for better document length normalization
            epsilon=0.25
        )
        
        self.is_indexed = True
    
    def search(self, query: str, top_k: int = 10, contracts: Optional[List] = None, 
               min_score: float = 0.1, use_enhanced: bool = True) -> List[Dict[str, Any]]:
        """Search for documents matching the query with advanced options"""
        if not self.is_indexed or not self.documents or not query.strip():
            return []
        
        # Apply contract filtering
        indices = None
        if contracts:
            contract_ids = [c.id for c in contracts]
            indices = [i for i, doc in enumerate(self.documents) if doc.get('id') in contract_ids]
            if not indices:
                return []
            filtered_docs = [self.documents[i] for i in indices]
            filtered_corpus = [self.corpus[i] for i in indices]
            filtered_ids = [self.doc_ids[i] for i in indices]
        else:
            filtered_docs = self.documents
            filtered_corpus = self.corpus
            filtered_ids = self.doc_ids
        
        # Clean query
        query = self._clean_text(query.lower())
        
        # If no documents to search
        if not filtered_corpus:
            return []
        
        # Perform multi-method search
        if use_enhanced:
            results = self._enhanced_search(query, filtered_corpus, filtered_docs, filtered_ids, top_k)
        else:
            results = self._basic_search(query, filtered_corpus, filtered_docs, filtered_ids, top_k)
        
        # Filter by minimum score
        results = [r for r in results if r['score'] >= min_score]
        
        return results
    
    def _enhanced_search(self, query: str, corpus: List[str], docs: List[Dict], 
                          ids: List[str], top_k: int) -> List[Dict[str, Any]]:
        """Enhanced search with multiple ranking signals"""
        
        # TF-IDF search
        query_vector = self.vectorizer.transform([query])
        if len(corpus) < len(self.corpus):
            # For filtered search, create temporary TF-IDF
            temp_vectorizer = TfidfVectorizer(
                max_features=10000,
                stop_words='english',
                ngram_range=(1, 3),
                min_df=1,
                use_idf=True,
                smooth_idf=True,
                sublinear_tf=True
            )
            temp_matrix = temp_vectorizer.fit_transform(corpus)
            temp_query = temp_vectorizer.transform([query])
            tfidf_scores = cosine_similarity(temp_query, temp_matrix).flatten()
        else:
            tfidf_scores = cosine_similarity(query_vector, self.tfidf_matrix).flatten()
        
        # BM25 search
        tokenized_query = query.split()
        if len(corpus) < len(self.corpus):
            temp_bm25 = BM25Okapi([text.split() for text in corpus], k1=1.5, b=0.75)
            bm25_scores = temp_bm25.get_scores(tokenized_query)
        else:
            bm25_scores = self.bm25.get_scores(tokenized_query)
        
        # Additional ranking signals
        query_words = set(query.split())
        word_overlap_scores = []
        
        for text in corpus:
            words = set(text.split())
            overlap = len(query_words & words)
            total = len(query_words | words)
            overlap_score = overlap / total if total > 0 else 0
            word_overlap_scores.append(overlap_score)
        
        # Normalize scores
        tfidf_scores = self._normalize_scores(tfidf_scores)
        bm25_scores = self._normalize_scores(bm25_scores)
        overlap_scores = self._normalize_scores(np.array(word_overlap_scores))
        
        # Hybrid fusion with multiple signals
        hybrid_scores = (
            0.40 * tfidf_scores + 
            0.35 * bm25_scores + 
            0.25 * overlap_scores
        )
        
        # Get top results
        top_indices = np.argsort(hybrid_scores)[::-1][:top_k]
        
        results = []
        for idx in top_indices:
            if hybrid_scores[idx] > 0:
                results.append({
                    'id': ids[idx] if idx < len(ids) else '',
                    'document': docs[idx] if idx < len(docs) else {},
                    'score': float(hybrid_scores[idx]),
                    'tfidf_score': float(tfidf_scores[idx] if idx < len(tfidf_scores) else 0),
                    'bm25_score': float(bm25_scores[idx] if idx < len(bm25_scores) else 0),
                    'overlap_score': float(overlap_scores[idx] if idx < len(overlap_scores) else 0)
                })
        
        return results
    
    def _basic_search(self, query: str, corpus: List[str], docs: List[Dict],
                       ids: List[str], top_k: int) -> List[Dict[str, Any]]:
        """Basic hybrid search (original implementation)"""
        # TF-IDF search
        query_vector = self.vectorizer.transform([query])
        if len(corpus) < len(self.corpus):
            temp_vectorizer = TfidfVectorizer(
                max_features=5000,
                stop_words='english',
                ngram_range=(1, 2)
            )
            temp_matrix = temp_vectorizer.fit_transform(corpus)
            temp_query = temp_vectorizer.transform([query])
            tfidf_scores = cosine_similarity(temp_query, temp_matrix).flatten()
        else:
            tfidf_scores = cosine_similarity(query_vector, self.tfidf_matrix).flatten()
        
        # BM25 search
        tokenized_query = query.split()
        if len(corpus) < len(self.corpus):
            temp_bm25 = BM25Okapi([text.split() for text in corpus])
            bm25_scores = temp_bm25.get_scores(tokenized_query)
        else:
            bm25_scores = self.bm25.get_scores(tokenized_query)
        
        # Normalize scores
        tfidf_scores = self._normalize_scores(tfidf_scores)
        bm25_scores = self._normalize_scores(bm25_scores)
        
        # Hybrid fusion
        hybrid_scores = 0.5 * tfidf_scores + 0.5 * bm25_scores
        
        # Get top results
        top_indices = np.argsort(hybrid_scores)[::-1][:top_k]
        
        results = []
        for idx in top_indices:
            if hybrid_scores[idx] > 0:
                results.append({
                    'id': ids[idx] if idx < len(ids) else '',
                    'document': docs[idx] if idx < len(docs) else {},
                    'score': float(hybrid_scores[idx]),
                    'tfidf_score': float(tfidf_scores[idx] if idx < len(tfidf_scores) else 0),
                    'bm25_score': float(bm25_scores[idx] if idx < len(bm25_scores) else 0)
                })
        
        return results
    
    def _clean_text(self, text: str) -> str:
        """Advanced text cleaning"""
        # Remove special characters but keep meaningful ones
        text = re.sub(r'[^\w\s\.\-]', ' ', text)
        # Remove extra whitespace
        text = re.sub(r'\s+', ' ', text)
        # Trim
        return text.strip()
    
    def _normalize_scores(self, scores: np.ndarray) -> np.ndarray:
        """Robust score normalization"""
        if len(scores) == 0:
            return scores
        min_score = np.min(scores)
        max_score = np.max(scores)
        if max_score - min_score == 0:
            return np.ones_like(scores) if max_score > 0 else np.zeros_like(scores)
        return (scores - min_score) / (max_score - min_score)
    
    def keyword_search(self, query: str, top_k: int = 10) -> List[Dict[str, Any]]:
        """Pure keyword search using BM25"""
        if not self.is_indexed or not self.documents or not query.strip():
            return []
        
        query = self._clean_text(query.lower())
        tokenized_query = query.split()
        bm25_scores = self.bm25.get_scores(tokenized_query)
        
        top_indices = np.argsort(bm25_scores)[::-1][:top_k]
        
        results = []
        for idx in top_indices:
            if bm25_scores[idx] > 0:
                results.append({
                    'id': self.doc_ids[idx],
                    'document': self.documents[idx],
                    'score': float(bm25_scores[idx])
                })
        
        return results
    
    def semantic_search(self, query: str, top_k: int = 10) -> List[Dict[str, Any]]:
        """Semantic search using TF-IDF"""
        if not self.is_indexed or not self.documents or not query.strip():
            return []
        
        query = self._clean_text(query.lower())
        query_vector = self.vectorizer.transform([query])
        tfidf_scores = cosine_similarity(query_vector, self.tfidf_matrix).flatten()
        
        top_indices = np.argsort(tfidf_scores)[::-1][:top_k]
        
        results = []
        for idx in top_indices:
            if tfidf_scores[idx] > 0:
                results.append({
                    'id': self.doc_ids[idx],
                    'document': self.documents[idx],
                    'score': float(tfidf_scores[idx])
                })
        
        return results
    
    def get_search_stats(self) -> Dict[str, Any]:
        """Get search engine statistics"""
        if not self.is_indexed:
            return {'is_indexed': False}
        
        return {
            'is_indexed': True,
            'num_documents': len(self.documents),
            'num_corpus': len(self.corpus),
            'vocabulary_size': len(self.vectorizer.vocabulary_) if self.vectorizer else 0,
            'avg_doc_length': np.mean([len(text.split()) for text in self.corpus]) if self.corpus else 0,
            'total_words': sum(len(text.split()) for text in self.corpus)
        }
    
    def get_related_terms(self, term: str, top_k: int = 10) -> List[Tuple[str, float]]:
        """Get terms related to a given term (for autocomplete/suggestions)"""
        if not self.is_indexed or not self.vectorizer:
            return []
        
        # Get feature names
        feature_names = self.vectorizer.get_feature_names_out()
        
        # Find terms containing the query
        related = []
        for feat in feature_names:
            if term in feat or feat in term:
                # Calculate similarity (simple co-occurrence)
                try:
                    idx = list(feature_names).index(feat)
                    # Get term frequencies
                    freq = sum(self.tfidf_matrix[:, idx].toarray().flatten())
                    related.append((feat, float(freq)))
                except:
                    pass
        
        # Sort by frequency
        related.sort(key=lambda x: x[1], reverse=True)
        
        return related[:top_k]