from .collaborative import recommend_from_collaborative
from .content_based import content_based_recommendations
def hybrid_recommendations(user_id, interactions_df, products_df, algo, \
                           cf_weight=0.6, cb_weight=0.4, top_n=5):
    cf_recommendations = recommend_from_collaborative(algo, user_id, \
                                                      interactions_df, top_n)
    cb_recommendations = content_based_recommendations(user_id, products_df, \
                                                       interactions_df, top_n)

    combined_scores = {}
    for product_id, score in cf_recommendations:
        combined_scores[product_id] = cf_weight * score
    for product_id, score in cb_recommendations:
        combined_scores[product_id] = combined_scores.get(product_id, 0) + \
            cb_weight * score

    ranked_recommendations = sorted(combined_scores.items(), key=lambda x: x[1], \
                                    reverse=True)[:top_n]
    return ranked_recommendations
