def evaluate_recommendations(user_id, recommendations, interactions_df):
    relevant_products = interactions_df[
        (interactions_df["UserID"] == user_id) & (interactions_df["InteractionType"] == "like")
    ]["ProductID"].unique()

    recommended_products = [rec[0] for rec in recommendations]

    precision = len(set(recommended_products) & set(relevant_products)) / len(recommended_products) if recommended_products else 0
    recall = len(set(recommended_products) & set(relevant_products)) / len(relevant_products) if relevant_products.size > 0 else 0

    print(f"UserID {user_id} - Precision: {precision:.2f}, Recall: {recall:.2f}")
    return precision, recall
