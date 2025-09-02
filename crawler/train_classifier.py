# train_classifier.py
import joblib
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.naive_bayes import MultinomialNB
from sklearn.pipeline import Pipeline
from sklearn.model_selection import train_test_split
from sklearn.metrics import classification_report

# Example training data (replace with a CSV or DB later)
docs = [
    "Buy cheap shoes online, best price discount",
    "Breaking news: government passes new law",
    "Cuisinart toaster product details and reviews",
    "Match highlights: football world cup final",
    "Latest iPhone product launch announcement",
    "Top 10 tips for fitness and health",
]

labels = [
    "shopping",
    "news",
    "product",
    "sports",
    "tech",
    "lifestyle",
]

# Split train/test
X_train, X_test, y_train, y_test = train_test_split(docs, labels, test_size=0.2, random_state=42)

# Pipeline: TF-IDF + Naive Bayes
clf = Pipeline([
    ("tfidf", TfidfVectorizer(max_features=5000, ngram_range=(1,2))),
    ("nb", MultinomialNB()),
])

clf.fit(X_train, y_train)

# Evaluate
y_pred = clf.predict(X_test)
print(classification_report(y_test, y_pred))

# Save model
joblib.dump(clf, "page_classifier.joblib")
print("✅ Model saved to page_classifier.joblib")
