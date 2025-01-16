from surprise import Dataset, Reader, KNNBasic

def train_collaborative_filtering(interactions_df):
    reader = Reader(rating_scale=(1, interactions_df["InteractionCount"].max()))
    data = Dataset.load_from_df(interactions_df[["UserID", "ProductID", \
                                                 "InteractionCount"]], reader)
    trainset = data.build_full_trainset()

    sim_options = {"name": "cosine", "user_based": True}
    algo = KNNBasic(sim_options=sim_options)
    algo.fit(trainset)
    return algo

def recommend_from_collaborative(algo, user_id, interactions_df, top_n=5):
    all_products = interactions_df["ProductID"].unique()
    interacted_products = interactions_df[interactions_df["UserID"] == \
                                          user_id]["ProductID"].unique()
    products_to_predict = [p for p in all_products if p not in \
                           interacted_products]

    predictions = [(product_id, algo.predict(user_id, product_id).est) \
                   for product_id in products_to_predict]
    recommendations = sorted(predictions, key=lambda x: x[1], \
                             reverse=True)[:top_n]
    print(f"Collaborative Recommendations for User {user_id}: {recommendations}")
    return recommendations
