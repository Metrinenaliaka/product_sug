from django.http import JsonResponse
from .recommendation.hybrid import hybrid_recommendations
from .recommendation.collaborative import train_collaborative_filtering
import sqlite3
import pandas as pd

def recommend_products_view(request, user_id):
    top_n = int(request.GET.get("top_n", 5))
    conn = sqlite3.connect("user_data.db")

    # Load data
    interactions_df = pd.read_sql_query("SELECT * FROM UserInteractions", conn)
    products_df = pd.read_sql_query("SELECT * FROM Products", conn)

    # Train collaborative filtering model
    algo = train_collaborative_filtering(interactions_df)

    # Generate hybrid recommendations
    recommendations = hybrid_recommendations(user_id, interactions_df, products_df, algo, top_n=top_n)

    # Convert int64 to int
    recommendations = [(int(product_id), float(score)) for product_id, score in recommendations]

    conn.close()

    return JsonResponse({"recommendations": recommendations})
