from difflib import SequenceMatcher
import re

def normalize_text(text):
    """Normalize text for better matching"""
    text = text.lower().strip()
    # Remove punctuation and extra spaces
    text = re.sub(r'[^\w\s]', '', text)
    text = re.sub(r'\s+', ' ', text)
    return text

def extract_keywords(text):
    """Extract meaningful keywords from text"""
    # Common stop words to ignore
    stop_words = {
        'what', 'is', 'are', 'the', 'can', 'i', 'how', 'do', 'does', 
        'where', 'when', 'who', 'which', 'a', 'an', 'to', 'for', 'of',
        'in', 'on', 'at', 'by', 'with', 'from', 'about', 'get', 'my',
        'me', 'you', 'your', 'tell', 'please', 'could', 'would', 'should'
    }
    
    words = normalize_text(text).split()
    keywords = [word for word in words if word not in stop_words and len(word) > 2]
    return set(keywords)

def calculate_similarity(str1, str2):
    """Calculate similarity between two strings"""
    return SequenceMatcher(None, str1, str2).ratio()

def keyword_match_score(user_keywords, faq_keywords):
    """Calculate keyword overlap score"""
    if not user_keywords or not faq_keywords:
        return 0
    
    common_keywords = user_keywords & faq_keywords
    # Weighted score: more weight to exact keyword matches
    score = len(common_keywords) / max(len(user_keywords), len(faq_keywords))
    
    # Boost score if critical keywords match
    if common_keywords:
        return score * 1.2  # 20% boost for keyword matches
    return score

def contains_phrase(user_text, faq_text):
    """Check if user query contains significant phrases from FAQ"""
    user_words = normalize_text(user_text).split()
    faq_words = normalize_text(faq_text).split()
    
    # Check for 2-word and 3-word phrase matches
    score = 0
    for i in range(len(user_words) - 1):
        bigram = ' '.join(user_words[i:i+2])
        if bigram in ' '.join(faq_words):
            score += 0.3
    
    for i in range(len(user_words) - 2):
        trigram = ' '.join(user_words[i:i+3])
        if trigram in ' '.join(faq_words):
            score += 0.5
    
    return min(score, 1.0)  # Cap at 1.0

def semantic_similarity(user_query, faq_question):
    """Enhanced semantic similarity check"""
    user_norm = normalize_text(user_query)
    faq_norm = normalize_text(faq_question)
    
    # Direct string similarity
    string_sim = calculate_similarity(user_norm, faq_norm)
    
    # Keyword matching
    user_keywords = extract_keywords(user_query)
    faq_keywords = extract_keywords(faq_question)
    keyword_score = keyword_match_score(user_keywords, faq_keywords)
    
    # Phrase matching
    phrase_score = contains_phrase(user_query, faq_question)
    
    # Check if one string contains the other (partial match)
    containment_score = 0
    if user_norm in faq_norm or faq_norm in user_norm:
        containment_score = 0.8
    
    # Weighted combination
    final_score = (
        string_sim * 0.25 +      # 25% weight to overall similarity
        keyword_score * 0.35 +    # 35% weight to keyword matching
        phrase_score * 0.25 +     # 25% weight to phrase matching
        containment_score * 0.15  # 15% weight to containment
    )
    
    return final_score

def match_question(user_query, faqs, threshold=0.45):
    """
    Match user query with FAQ database using multiple techniques
    Returns the best matching FAQ if similarity is above threshold
    
    Args:
        user_query: User's question string
        faqs: List of FAQ dictionaries with 'question' and 'answer' keys
        threshold: Minimum similarity score (0-1) to consider a match
    
    Returns:
        FAQ dict if match found, None otherwise
    """
    if not user_query or not faqs:
        return None
    
    user_query = user_query.strip()
    if len(user_query) < 3:  # Too short to match meaningfully
        return None
    
    best_match = None
    best_score = 0
    
    for faq in faqs:
        faq_question = faq.get("question", "")
        if not faq_question:
            continue
        
        # Calculate comprehensive similarity score
        score = semantic_similarity(user_query, faq_question)
        
        # Boost score for very similar questions
        if score > 0.8:
            score = min(score * 1.1, 1.0)
        
        if score > best_score:
            best_score = score
            best_match = faq
    
    # Return match only if above threshold
    if best_score >= threshold:
        return best_match
    
    return None

def get_match_confidence(user_query, faq_question):
    """
    Get confidence level of a match (useful for debugging/logging)
    Returns: 'high', 'medium', 'low', or 'none'
    """
    score = semantic_similarity(user_query, faq_question)
    
    if score >= 0.75:
        return 'high'
    elif score >= 0.55:
        return 'medium'
    elif score >= 0.35:
        return 'low'
    else:
        return 'none'