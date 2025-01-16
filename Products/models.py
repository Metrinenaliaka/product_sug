from django.db import models

class User(models.Model):
    username = models.CharField(max_length=100, unique=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.username


class Category(models.Model):
    category_name = models.CharField(max_length=100)

    def __str__(self):
        return self.category_name


class Product(models.Model):
    product_type = models.CharField(max_length=100)
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name="products")
    attributes = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.product_type


class UserInteraction(models.Model):
    INTERACTION_CHOICES = [
        ('like', 'Like'),
        ('dislike', 'Dislike'),
    ]

    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="interactions")
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name="interactions")
    interaction_type = models.CharField(max_length=50, choices=INTERACTION_CHOICES)
    interaction_count = models.PositiveIntegerField(default=1)
    interaction_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username} - {self.interaction_type} - {self.product.product_type}"


class UserPreference(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="preferences")
    preference_category = models.CharField(max_length=100)
    preference_data = models.TextField()
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.user.username} - {self.preference_category}"


class Suggestion(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="suggestions")
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name="suggestions")
    score = models.DecimalField(max_digits=5, decimal_places=2)
    generated_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Suggestion for {self.user.username}: {self.product.product_type} ({self.score})"
