import os
import joblib

# ---------- ML BASED CLASSIFIER FOR PAGE TYPE -----------

MODEL_PATH = os.path.join(os.path.dirname(__file__), "page_classifier.joblib")

# Load once
clf = joblib.load(MODEL_PATH)
# ML based classifier
def classify_page(title: str, description: str, content: str) -> str:
    """Classify page type using ML model"""
    text = " ".join(filter(None, [title, description, content]))
    if not text.strip():
        return "unknown"
    return clf.predict([text])[0]


# ---------- RULE BASED CLASSIFIER FOR TOPICS -----------

TOPIC_KEYWORDS = {
    "sports": ["game", "team", "match", "score", "player", "tournament", "league", "coach"],
    "politics": ["government", "election", "policy", "minister", "senate", "parliament", "vote"],
    "tech": ["software", "AI", "hardware", "programming", "device", "machine learning", "cloud"],
    "finance": ["stock", "market", "bank", "investment", "crypto", "loan", "fund", "trading"],
    "health": ["doctor", "hospital", "disease", "treatment", "vaccine", "nutrition", "fitness"],
    "science": ["research", "experiment", "theory", "biology", "physics", "chemistry", "lab"],
    "education": ["school", "university", "student", "teacher", "course", "exam", "degree"],
    "entertainment": ["movie", "music", "concert", "actor", "film", "television", "celebrity"],
    "travel": ["flight", "hotel", "tour", "trip", "destination", "vacation", "beach"],
    "food": ["recipe", "restaurant", "cuisine", "meal", "chef", "ingredient", "dining"],
    "fashion": ["clothing", "style", "trend", "brand", "designer", "outfit", "runway"],
    "real_estate": ["property", "house", "apartment", "rent", "mortgage", "landlord", "buyer"],
    "automotive": ["car", "engine", "vehicle", "drive", "fuel", "battery", "electric", "speed"],
    "law": ["court", "lawyer", "judge", "legal", "case", "trial", "justice", "crime"],
    "environment": ["climate", "pollution", "sustainability", "recycle", "wildlife", "forest"],
    "business": ["company", "startup", "CEO", "employee", "corporate", "merger", "growth"],
    "history": ["ancient", "war", "king", "empire", "revolution", "civilization", "battle"],
    "literature": ["book", "novel", "poem", "author", "story", "fiction", "literary", "read"],
    "religion": ["church", "temple", "god", "faith", "spiritual", "prayer", "belief"],
    "gaming": ["video game", "console", "multiplayer", "esports", "quest", "gamer", "battle"],
}

def extract_topics(text, max_topics=2):
    text = text.lower()
    scores = {}
    for topic, words in TOPIC_KEYWORDS.items():
        scores[topic] = sum(text.count(w) for w in words)
    sorted_topics = sorted(scores.items(), key=lambda x: x[1], reverse=True)
    return [t for t, score in sorted_topics if score > 0][:max_topics]
