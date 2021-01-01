import os
import json
import requests

current_path = os.path.dirname(__file__)
static_folder = os.path.join(current_path, "static")

def list_categories(parent):
    """
    Returns a list of categories belonging to the 'restaurant' parent category
    """
    try:
        with open(os.path.join(static_folder, "categories.json")) as f:
            data = json.load(f)
            categories = [category for category in data if parent in category["parents"]]
        return categories
    except FileNotFoundError:
        return None

def update_categories():
    """
    Retrieves updated category list from Yelp API
    """
    url = "https://www.yelp.ca/developers/documentation/v3/all_category_list/categories.json"
    r = requests.get(url, allow_redirects=True)
    
    with open(os.path.join(static_folder, "categories.json"), 'w') as f:
        json.dump(r.json(), f)