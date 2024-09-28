from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LinearRegression
from sklearn.preprocessing import StandardScaler
import pandas as pd
from transformers import pipeline

def preprocess_data(nutrition_df, mrp_df):
    tfidf_vectorizer = TfidfVectorizer(stop_words='english')
    X_nutrition = tfidf_vectorizer.fit_transform(nutrition_df['label'])
    y_nutrition = [category_health_score(item) for item in nutrition_df['category']]
    
    scaler = StandardScaler()
    X_mrp = scaler.fit_transform(mrp_df[['mrp']])
    
    return X_nutrition, y_nutrition, tfidf_vectorizer, scaler

# Define health criteria for each food category
health_criteria = {
    "bread": {'max_calories': 250, 'max_sugar': 5, 'min_fiber': 3, 'min_protein': 5},
    "cereals": {'max_calories': 200, 'max_sugar': 10, 'min_fiber': 5, 'min_protein': 5},
    "cheese": {'max_calories': 300, 'max_sugar': 2, 'min_fiber': 0, 'min_protein': 20},
    "chips": {'max_calories': 250, 'max_sugar': 2, 'min_fiber': 2, 'min_protein': 2},
    "chocolate": {'max_calories': 200, 'max_sugar': 20, 'min_fiber': 1, 'min_protein': 3},
    "cookies": {'max_calories': 150, 'max_sugar': 15, 'min_fiber': 1, 'min_protein': 2},
    "crackers": {'max_calories': 150, 'max_sugar': 5, 'min_fiber': 3, 'min_protein': 2},
    "energy drinks": {'max_calories': 100, 'max_sugar': 25, 'min_fiber': 0, 'min_protein': 0},
    "fruit juices": {'max_calories': 120, 'max_sugar': 15, 'min_fiber': 0, 'min_protein': 0},
    "granola bars": {'max_calories': 200, 'max_sugar': 10, 'min_fiber': 3, 'min_protein': 3},
    "ice cream": {'max_calories': 200, 'max_sugar': 15, 'min_fiber': 0, 'min_protein': 2},
    "instant_noodles": {'max_calories': 400, 'max_sugar': 3, 'min_fiber': 1, 'min_protein': 10},
    "ketchup": {'max_calories': 100, 'max_sugar': 15, 'min_fiber': 0, 'min_protein': 0},
    "muffins": {'max_calories': 300, 'max_sugar': 15, 'min_fiber': 1, 'min_protein': 3},
    "oats": {'max_calories': 150, 'max_sugar': 2, 'min_fiber': 5, 'min_protein': 6},
    "popcorn": {'max_calories': 150, 'max_sugar': 1, 'min_fiber': 4, 'min_protein': 3},
    "soft drinks": {'max_calories': 150, 'max_sugar': 30, 'min_fiber': 0, 'min_protein': 0},
    "yogurt": {'max_calories': 150, 'max_sugar': 10, 'min_fiber': 0, 'min_protein': 5}
}

def category_health_score(nutrition_info, category):
    # Get health criteria for the specific category
    criteria = health_criteria.get(category.lower(), None)
    if not criteria:
        return 0  # If category is not found, return a score of 0

    score = 100  # Start with full score

    # Reduce score based on calories
    if nutrition_info['calories'] > criteria['max_calories']:
        score -= (nutrition_info['calories'] - criteria['max_calories']) / 10

    # Reduce score based on sugar
    if nutrition_info['sugar'] > criteria['max_sugar']:
        score -= (nutrition_info['sugar'] - criteria['max_sugar']) / 2

    # Reduce score for insufficient fiber
    if nutrition_info['fiber'] < criteria['min_fiber']:
        score -= (criteria['min_fiber'] - nutrition_info['fiber']) * 10

    # Reduce score for insufficient protein
    if nutrition_info['protein'] < criteria['min_protein']:
        score -= (criteria['min_protein'] - nutrition_info['protein']) * 10

    return max(0, score)  # Ensure score does not go below 0
    print(f"Final health score for {item_category}: {health_score}%")
    return health_score

def train_model():
    # Load a pre-trained language model (e.g., BERT) using Hugging Face
    regressor = pipeline('text-classification', model='distilbert-base-uncased')  # Or any model you want to use
    return regressor

if __name__ == '__main__':
    train_model()