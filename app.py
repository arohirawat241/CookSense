from flask import Flask, render_template, request, jsonify
from collections import deque

app = Flask(__name__)

# ─────────────────────────────────────────────
#  RECIPE DATASET  (30 recipes) with full instructions
# ─────────────────────────────────────────────
RECIPES = {
    "Egg Fried Rice": {
        "ingredients": ["rice", "egg", "onion", "soy sauce", "oil"],
        "time": "15 min", "difficulty": "Easy", "emoji": "🍳", "serves": "2",
        "steps": [
            "Cook rice in advance and let it cool completely (cold rice works best).",
            "Heat oil in a pan or wok on high flame.",
            "Add chopped onion and stir-fry for 2 minutes until slightly golden.",
            "Push onion to the side, crack the eggs into the pan and scramble them.",
            "Mix the scrambled egg with the onion.",
            "Add the cooked rice and toss everything together on high heat.",
            "Add soy sauce and mix well. Stir-fry for 2–3 more minutes.",
            "Season with salt and pepper. Serve hot."
        ]
    },
    "Masala Omelette": {
        "ingredients": ["egg", "onion", "tomato", "chilli", "oil"],
        "time": "10 min", "difficulty": "Easy", "emoji": "🥚", "serves": "1",
        "steps": [
            "Finely chop onion, tomato, and green chilli.",
            "Crack 2 eggs into a bowl, add salt and beat well.",
            "Mix in the chopped vegetables.",
            "Heat oil in a flat pan on medium flame.",
            "Pour the egg mixture and spread evenly.",
            "Cook for 2 minutes until the bottom is set.",
            "Flip carefully and cook the other side for 1 minute.",
            "Serve hot with bread or roti."
        ]
    },
    "Veg Pulao": {
        "ingredients": ["rice", "carrot", "beans", "onion", "spices"],
        "time": "25 min", "difficulty": "Easy", "emoji": "🍚", "serves": "3",
        "steps": [
            "Wash and soak rice for 20 minutes, then drain.",
            "Chop carrot, beans, and onion into small pieces.",
            "Heat oil in a pressure cooker or deep pan.",
            "Add whole spices (cumin, bay leaf, cloves) and let them splutter.",
            "Add onion and fry until golden brown.",
            "Add carrots and beans, stir-fry for 3 minutes.",
            "Add drained rice and mix gently.",
            "Add 2 cups of water, salt, and bring to a boil.",
            "Cover and cook for 10–12 minutes until rice is done.",
            "Fluff with a fork and serve hot."
        ]
    },
    "Tomato Rice": {
        "ingredients": ["rice", "tomato", "onion", "oil", "spices"],
        "time": "20 min", "difficulty": "Easy", "emoji": "🍅", "serves": "2",
        "steps": [
            "Cook rice separately and set aside.",
            "Heat oil in a pan, add mustard seeds and let them splutter.",
            "Add chopped onion and fry until translucent.",
            "Add chopped tomatoes, salt, and spices. Cook until mushy.",
            "Add cooked rice to the tomato mixture.",
            "Mix gently on low flame for 3–4 minutes.",
            "Garnish with coriander leaves and serve."
        ]
    },
    "Lemon Rice": {
        "ingredients": ["rice", "lemon", "peanuts", "oil", "mustard"],
        "time": "15 min", "difficulty": "Easy", "emoji": "🍋", "serves": "2",
        "steps": [
            "Cook rice and spread it out to cool.",
            "Heat oil in a pan, add mustard seeds and let them pop.",
            "Add peanuts and roast until golden.",
            "Add turmeric powder and mix.",
            "Add the cooked rice and toss well.",
            "Squeeze fresh lemon juice over the rice.",
            "Add salt to taste and mix thoroughly. Serve at room temperature."
        ]
    },
    "Dal Tadka": {
        "ingredients": ["lentils", "onion", "tomato", "garlic", "spices"],
        "time": "30 min", "difficulty": "Medium", "emoji": "🫘", "serves": "3",
        "steps": [
            "Wash lentils (toor or masoor dal) and pressure cook with water, turmeric, and salt for 3–4 whistles.",
            "Mash the cooked dal lightly and set aside.",
            "Heat ghee or oil in a pan for the tadka.",
            "Add cumin seeds and let them splutter.",
            "Add chopped garlic and fry until golden.",
            "Add chopped onion and fry until brown.",
            "Add chopped tomatoes and cook until soft.",
            "Add chilli powder and garam masala.",
            "Pour this tadka over the cooked dal and mix.",
            "Garnish with coriander. Serve with rice or roti."
        ]
    },
    "Aloo Sabzi": {
        "ingredients": ["potato", "onion", "tomato", "spices", "oil"],
        "time": "20 min", "difficulty": "Easy", "emoji": "🥔", "serves": "2",
        "steps": [
            "Peel and cube potatoes into small pieces.",
            "Heat oil in a pan, add cumin seeds.",
            "Add chopped onion and fry until golden.",
            "Add chopped tomatoes and cook until mushy.",
            "Add turmeric, chilli powder, coriander powder, and salt.",
            "Add the potato cubes and mix well.",
            "Add a splash of water, cover and cook for 12–15 minutes.",
            "Check if potatoes are tender. Garnish with coriander and serve."
        ]
    },
    "Paneer Bhurji": {
        "ingredients": ["paneer", "onion", "tomato", "spices", "oil"],
        "time": "15 min", "difficulty": "Easy", "emoji": "🧀", "serves": "2",
        "steps": [
            "Crumble the paneer into small pieces and set aside.",
            "Heat oil in a pan, add cumin seeds.",
            "Add finely chopped onion and fry until golden.",
            "Add chopped tomatoes and cook until soft.",
            "Add turmeric, chilli powder, and garam masala.",
            "Add crumbled paneer and mix well.",
            "Cook on medium heat for 4–5 minutes, stirring occasionally.",
            "Garnish with fresh coriander and serve with bread or roti."
        ]
    },
    "Vegetable Upma": {
        "ingredients": ["semolina", "onion", "carrot", "beans", "oil"],
        "time": "20 min", "difficulty": "Easy", "emoji": "🥣", "serves": "2",
        "steps": [
            "Dry roast semolina (rava) in a pan until light golden. Set aside.",
            "Heat oil in a pan, add mustard seeds and curry leaves.",
            "Add chopped onion and fry until soft.",
            "Add diced carrot and beans, stir-fry for 3 minutes.",
            "Add 2 cups of water and salt, bring to a boil.",
            "Slowly add roasted semolina while stirring continuously.",
            "Stir well to avoid lumps, cook for 3–4 minutes.",
            "Cover and rest for 2 minutes. Serve hot with chutney."
        ]
    },
    "Poha": {
        "ingredients": ["flattened rice", "onion", "potato", "peanuts", "oil"],
        "time": "15 min", "difficulty": "Easy", "emoji": "🍛", "serves": "2",
        "steps": [
            "Rinse flattened rice (poha) in water for 1 minute, drain and set aside.",
            "Heat oil in a pan, add mustard seeds and let them pop.",
            "Add peanuts and roast until golden.",
            "Add chopped onion and diced potato, cook for 5 minutes.",
            "Add turmeric, salt, and sugar.",
            "Add the soaked poha and mix gently.",
            "Cook on low flame for 3–4 minutes.",
            "Squeeze lemon juice on top and garnish with coriander. Serve hot."
        ]
    },
    "Khichdi": {
        "ingredients": ["rice", "lentils", "onion", "garlic", "spices"],
        "time": "30 min", "difficulty": "Easy", "emoji": "🍲", "serves": "3",
        "steps": [
            "Wash rice and lentils together, soak for 15 minutes.",
            "Heat ghee in a pressure cooker.",
            "Add cumin seeds, chopped garlic, and onion. Fry until golden.",
            "Add turmeric, salt, and a pinch of asafoetida.",
            "Add the soaked rice and lentils. Mix well.",
            "Add 3.5 cups of water.",
            "Pressure cook for 3 whistles.",
            "Let pressure release, open and mash slightly. Serve hot with pickle."
        ]
    },
    "Pasta Arrabiata": {
        "ingredients": ["pasta", "tomato", "garlic", "chilli", "oil"],
        "time": "25 min", "difficulty": "Easy", "emoji": "🍝", "serves": "2",
        "steps": [
            "Boil pasta in salted water until al dente. Drain and set aside.",
            "Heat olive oil in a pan on medium flame.",
            "Add minced garlic and fry for 1 minute until fragrant.",
            "Add chopped red chilli and fry for 30 seconds.",
            "Add chopped tomatoes, salt, and a pinch of sugar.",
            "Cook the sauce for 10–12 minutes until thickened.",
            "Add cooked pasta to the sauce and toss well.",
            "Garnish with basil or parsley and serve immediately."
        ]
    },
    "Garlic Bread": {
        "ingredients": ["bread", "garlic", "butter", "herbs"],
        "time": "10 min", "difficulty": "Easy", "emoji": "🥖", "serves": "2",
        "steps": [
            "Preheat oven or toaster to 180°C.",
            "Soften butter at room temperature.",
            "Mince garlic finely and mix into the butter.",
            "Add dried herbs (oregano or parsley) to the butter mixture.",
            "Slice bread and spread the garlic butter generously on each slice.",
            "Place on a baking tray and bake for 8–10 minutes until golden.",
            "Serve hot immediately."
        ]
    },
    "French Toast": {
        "ingredients": ["bread", "egg", "milk", "sugar", "butter"],
        "time": "15 min", "difficulty": "Easy", "emoji": "🍞", "serves": "2",
        "steps": [
            "Crack eggs into a wide bowl, add milk, sugar, and a pinch of salt.",
            "Whisk together until smooth.",
            "Dip bread slices into the egg mixture, coating both sides.",
            "Heat butter in a flat pan on medium flame.",
            "Place the dipped bread on the pan.",
            "Cook for 2–3 minutes per side until golden brown.",
            "Serve warm with honey, jam, or powdered sugar on top."
        ]
    },
    "Banana Pancakes": {
        "ingredients": ["banana", "egg", "flour", "milk", "butter"],
        "time": "20 min", "difficulty": "Easy", "emoji": "🥞", "serves": "2",
        "steps": [
            "Mash 1 ripe banana in a bowl until smooth.",
            "Add 1 egg, 1/2 cup flour, 1/2 cup milk, and a pinch of salt.",
            "Mix into a smooth batter (don't overmix).",
            "Heat a pan and add a little butter.",
            "Pour a ladleful of batter and spread into a circle.",
            "Cook for 2 minutes until bubbles appear on top.",
            "Flip and cook for 1 more minute.",
            "Repeat for remaining batter. Serve with honey or maple syrup."
        ]
    },
    "Vegetable Soup": {
        "ingredients": ["carrot", "potato", "onion", "tomato", "spices"],
        "time": "30 min", "difficulty": "Easy", "emoji": "🥣", "serves": "3",
        "steps": [
            "Chop all vegetables into small cubes.",
            "Heat oil in a deep pot, add onion and fry until soft.",
            "Add carrots and potatoes, stir for 3 minutes.",
            "Add tomatoes and cook until mushy.",
            "Add 4 cups of water, salt, pepper, and spices.",
            "Bring to a boil, then simmer for 15–20 minutes.",
            "Blend partially if you prefer a thicker soup.",
            "Serve hot with bread."
        ]
    },
    "Fried Potatoes": {
        "ingredients": ["potato", "oil", "salt", "spices"],
        "time": "20 min", "difficulty": "Easy", "emoji": "🍟", "serves": "2",
        "steps": [
            "Peel and slice potatoes into thin strips or wedges.",
            "Soak in cold water for 10 minutes to remove excess starch.",
            "Pat dry completely with a cloth.",
            "Heat oil in a deep pan on medium-high flame.",
            "Fry the potatoes in batches until golden and crispy.",
            "Drain on paper towels.",
            "Sprinkle salt, chilli powder, and spices while hot.",
            "Serve immediately."
        ]
    },
    "Aloo Paratha": {
        "ingredients": ["flour", "potato", "spices", "butter", "onion"],
        "time": "30 min", "difficulty": "Medium", "emoji": "🫓", "serves": "2",
        "steps": [
            "Knead flour with water and a pinch of salt into a soft dough. Rest for 15 minutes.",
            "Boil potatoes, peel and mash them completely.",
            "Mix mashed potato with finely chopped onion, spices, and salt.",
            "Divide dough into balls. Roll one ball into a small disc.",
            "Place a spoonful of filling in the centre, fold edges and seal.",
            "Gently roll out into a flat paratha.",
            "Cook on a hot tawa (griddle) with butter on both sides.",
            "Cook until golden brown spots appear. Serve with curd or pickle."
        ]
    },
    "Onion Pakoda": {
        "ingredients": ["onion", "flour", "chilli", "spices", "oil"],
        "time": "20 min", "difficulty": "Easy", "emoji": "🧅", "serves": "2",
        "steps": [
            "Slice onions thinly and separate the rings.",
            "In a bowl, mix gram flour (besan), chilli, spices, and salt.",
            "Add the onion slices to the flour mixture.",
            "Add very little water — just enough to coat the onions (not a batter).",
            "Heat oil in a deep pan for frying.",
            "Drop small clusters of the onion mixture into the oil.",
            "Fry on medium heat until golden and crispy.",
            "Drain on paper towels. Serve hot with chutney."
        ]
    },
    "Bread Omelette": {
        "ingredients": ["bread", "egg", "onion", "chilli", "butter"],
        "time": "10 min", "difficulty": "Easy", "emoji": "🍳", "serves": "1",
        "steps": [
            "Beat 2 eggs with salt, chopped onion, and chopped chilli.",
            "Heat butter on a flat pan.",
            "Pour the egg mixture and spread evenly.",
            "Before the egg sets, place a bread slice on top.",
            "Press gently so the bread sticks to the egg.",
            "Flip the whole thing together.",
            "Cook for 1 more minute until bread is toasted.",
            "Serve hot with ketchup."
        ]
    },
    "Chana Masala": {
        "ingredients": ["chickpeas", "onion", "tomato", "garlic", "spices"],
        "time": "35 min", "difficulty": "Medium", "emoji": "🫘", "serves": "3",
        "steps": [
            "Soak chickpeas overnight and pressure cook until tender (or use canned).",
            "Heat oil in a pan, add cumin seeds.",
            "Add finely chopped onion and fry until deep golden.",
            "Add minced garlic and ginger, fry for 1 minute.",
            "Add chopped tomatoes and cook until oil separates.",
            "Add chilli powder, coriander powder, garam masala, and salt.",
            "Add cooked chickpeas and mix well.",
            "Add 1 cup water and simmer for 10 minutes.",
            "Garnish with coriander and serve with rice or bhature."
        ]
    },
    "Jeera Rice": {
        "ingredients": ["rice", "cumin", "oil", "salt"],
        "time": "20 min", "difficulty": "Easy", "emoji": "🍚", "serves": "2",
        "steps": [
            "Wash and soak rice for 15 minutes, then drain.",
            "Heat oil or ghee in a pan.",
            "Add cumin seeds and let them splutter.",
            "Add drained rice and stir gently for 1 minute.",
            "Add 2 cups of water and salt.",
            "Bring to a boil, then reduce heat, cover and cook for 12 minutes.",
            "Fluff with a fork and serve hot."
        ]
    },
    "Curd Rice": {
        "ingredients": ["rice", "curd", "mustard", "salt", "oil"],
        "time": "15 min", "difficulty": "Easy", "emoji": "🍚", "serves": "2",
        "steps": [
            "Cook rice until soft and slightly mushy. Let it cool a little.",
            "Mash the rice lightly.",
            "Add fresh curd (yogurt) and salt. Mix well.",
            "Heat oil in a small pan for the tadka.",
            "Add mustard seeds and let them pop.",
            "Add curry leaves and dry red chilli.",
            "Pour the tadka over the curd rice.",
            "Mix gently. Serve at room temperature or chilled."
        ]
    },
    "Tomato Soup": {
        "ingredients": ["tomato", "onion", "garlic", "butter", "salt"],
        "time": "25 min", "difficulty": "Easy", "emoji": "🍅", "serves": "2",
        "steps": [
            "Roughly chop tomatoes, onion, and garlic.",
            "Heat butter in a pot, add garlic and onion, fry for 2 minutes.",
            "Add tomatoes, salt, and a pinch of sugar.",
            "Add 2 cups of water and bring to a boil.",
            "Simmer for 15 minutes until tomatoes are very soft.",
            "Let it cool slightly, then blend until smooth.",
            "Strain the soup for a smooth texture.",
            "Reheat, adjust salt, and serve with cream and bread."
        ]
    },
    "Scrambled Eggs": {
        "ingredients": ["egg", "butter", "salt", "pepper", "milk"],
        "time": "10 min", "difficulty": "Easy", "emoji": "🥚", "serves": "1",
        "steps": [
            "Crack 2–3 eggs into a bowl.",
            "Add a splash of milk, salt, and pepper. Whisk well.",
            "Heat butter in a non-stick pan on LOW heat.",
            "Pour in the egg mixture.",
            "Stir slowly and continuously with a spatula.",
            "Remove from heat while still slightly wet — residual heat finishes cooking.",
            "Serve immediately on toast."
        ]
    },
    "Vegetable Stir Fry": {
        "ingredients": ["carrot", "beans", "onion", "garlic", "soy sauce"],
        "time": "15 min", "difficulty": "Easy", "emoji": "🥦", "serves": "2",
        "steps": [
            "Slice carrot, beans, and onion into thin strips.",
            "Mince garlic finely.",
            "Heat oil in a wok or pan on HIGH flame.",
            "Add garlic and stir for 30 seconds.",
            "Add onion and stir-fry for 1 minute.",
            "Add carrot and beans, stir-fry for 3–4 minutes on high heat.",
            "Add soy sauce and toss everything together.",
            "Serve immediately over rice or noodles."
        ]
    },
    "Banana Smoothie": {
        "ingredients": ["banana", "milk", "sugar", "ice"],
        "time": "5 min", "difficulty": "Easy", "emoji": "🍌", "serves": "1",
        "steps": [
            "Peel and slice 1 ripe banana.",
            "Add banana, 1 cup cold milk, and sugar to a blender.",
            "Add a few ice cubes.",
            "Blend on high speed for 30–45 seconds until smooth.",
            "Pour into a glass and serve immediately."
        ]
    },
    "Peanut Butter Toast": {
        "ingredients": ["bread", "peanuts", "sugar", "salt"],
        "time": "5 min", "difficulty": "Easy", "emoji": "🥜", "serves": "1",
        "steps": [
            "If making peanut butter: blend roasted peanuts with a pinch of salt and sugar until smooth.",
            "Toast bread slices until golden and crispy.",
            "Spread peanut butter generously on the toast.",
            "Optionally top with banana slices or honey.",
            "Serve immediately."
        ]
    },
    "Sabudana Khichdi": {
        "ingredients": ["tapioca", "potato", "peanuts", "spices", "oil"],
        "time": "25 min", "difficulty": "Medium", "emoji": "⚪", "serves": "2",
        "steps": [
            "Soak tapioca pearls (sabudana) in water for 4–6 hours. Drain well.",
            "Boil and cube the potatoes.",
            "Dry roast peanuts and coarsely crush them.",
            "Mix soaked sabudana with crushed peanuts, salt, and sugar.",
            "Heat oil in a pan, add cumin seeds and green chilli.",
            "Add cubed potatoes and fry for 2 minutes.",
            "Add the sabudana mixture and toss gently on medium heat.",
            "Cook for 5–7 minutes, stirring gently. Squeeze lemon juice and serve."
        ]
    },
    "Maggi Noodles": {
        "ingredients": ["noodles", "onion", "tomato", "spices", "oil"],
        "time": "10 min", "difficulty": "Easy", "emoji": "🍜", "serves": "1",
        "steps": [
            "Boil 1.5 cups of water in a pan.",
            "Heat oil in another pan, add chopped onion and fry for 1 minute.",
            "Add chopped tomato and cook for 2 minutes.",
            "Add the noodles to the boiling water.",
            "Add the spice tastemaker and stir.",
            "Cook for 2 minutes until water is mostly absorbed.",
            "Mix in the fried onion-tomato and serve hot."
        ]
    },
}


# ─────────────────────────────────────────────
#  BFS-BASED SEARCH
# ─────────────────────────────────────────────
def bfs_recipe_search(user_ingredients):
    user_set = set(i.strip().lower() for i in user_ingredients)
    visited = set()
    queue = deque()
    results = []

    ingredient_graph = {}
    for recipe_name, data in RECIPES.items():
        for ing in data["ingredients"]:
            ingredient_graph.setdefault(ing, []).append(recipe_name)

    for ing in user_set:
        if ing in ingredient_graph:
            queue.append((ing, 0))

    while queue:
        current_ing, level = queue.popleft()
        if current_ing in visited:
            continue
        visited.add(current_ing)

    for recipe_name, data in RECIPES.items():
        recipe_ings = set(data["ingredients"])
        matched = user_set & recipe_ings
        missing = recipe_ings - user_set

        if not matched:
            continue

        match_score = len(matched) / len(recipe_ings)
        missing_pen = len(missing) / len(recipe_ings)
        heuristic   = round(match_score - 0.3 * missing_pen, 4)

        results.append({
            "name":            recipe_name,
            "emoji":           data["emoji"],
            "time":            data["time"],
            "difficulty":      data["difficulty"],
            "serves":          data["serves"],
            "matched":         sorted(matched),
            "missing":         sorted(missing),
            "all_ingredients": data["ingredients"],
            "steps":           data["steps"],
            "score":           round(heuristic * 100),
            "match_pct":       round(match_score * 100),
        })

    results.sort(key=lambda x: x["score"], reverse=True)
    return results[:8]


# ─────────────────────────────────────────────
#  ROUTES
# ─────────────────────────────────────────────
@app.route("/")
def index():
    return render_template("index.html")


@app.route("/recommend", methods=["POST"])
def recommend():
    data = request.get_json()
    ingredients = [i.strip().lower() for i in data.get("ingredients", []) if i.strip()]
    if not ingredients:
        return jsonify({"error": "No ingredients provided"}), 400
    results = bfs_recipe_search(ingredients)
    return jsonify({"recipes": results, "count": len(results)})


if __name__ == "__main__":
    app.run(debug=True)