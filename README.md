# CookSense
# CookSense – AI Recipe Recommender 🍳

## Overview

CookSense is a web-based AI system that recommends recipes based on leftover ingredients available with the user. The goal is to reduce food waste and help users quickly decide what they can cook using what they already have.

---

## Features

* Accepts a dynamic list of user-provided ingredients
* Uses graph-based search to find relevant recipes
* Ranks recipes using a heuristic scoring function
* Displays match percentage and missing ingredients
* Provides step-by-step cooking instructions

---

## Tech Stack

* **Backend:** Python, Flask
* **Frontend:** HTML, CSS, JavaScript
* **Core Logic:** BFS (Breadth-First Search), Heuristic Scoring

---

## How It Works

1. User enters available ingredients
2. Ingredients are mapped to a graph of recipes
3. BFS is used to explore all possible recipe matches
4. Recipes are scored based on:

   * Ingredient match percentage
   * Penalty for missing ingredients
5. Top-ranked recipes are displayed to the user

---

## Example

**Input:** rice, egg, onion
**Output:**

* Egg Fried Rice (Best match)
* Masala Omelette
* Veg Pulao

---

## How to Run

1. Clone the repository
2. Install dependencies

   ```
   pip install flask
   ```
3. Run the app

   ```
   python app.py
   ```
4. Open browser and go to

   ```
   http://127.0.0.1:5000
   ```

---

## Future Improvements

* Add machine learning for personalized recommendations
* Integrate grocery APIs for missing ingredients
* Add image recognition for ingredient detection
* Support multiple languages

---

## Contributors

* Arohi Rawat
* Team members

