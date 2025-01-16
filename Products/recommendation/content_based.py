from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

def content_based_recommendations(user_id, products_df, interactions_df, top_n=5):
    # Get products the user has interacted with
    user_interacted_products = interactions_df[interactions_df["UserID"] == user_id]["ProductID"].unique()

    # Generate the TF-IDF matrix for product attributes
    tfidf = TfidfVectorizer(stop_words="english")
    tfidf_matrix = tfidf.fit_transform(products_df["Attributes"])

    # Calculate cosine similarity
    similarity_scores = cosine_similarity(tfidf_matrix)

    # Collect recommended products
    recommended_products = []
    for product_id in user_interacted_products:
        # Map product_id to row index
        product_idx = products_df[products_df["ProductID"] == product_id].index[0]
        
        # Get similarity scores for this product
        scores = list(enumerate(similarity_scores[product_idx]))
        scores = sorted(scores, key=lambda x: x[1], reverse=True)[:top_n]
        
        # Map back to ProductID and filter out already interacted products
        recommended_products.extend([
            (products_df.iloc[s[0]]["ProductID"], s[1]) for s in scores
            if products_df.iloc[s[0]]["ProductID"] not in user_interacted_products
        ])

    # Return top N recommendations
    return sorted(recommended_products, key=lambda x: x[1], reverse=True)[:top_n]

