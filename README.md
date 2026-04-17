# CookSense
This project presents an AI-Based Recipe Recommender System designed to suggest suitable
recipes based on leftover ingredients available to the user. The primary objective of the system
is to reduce food waste and assist users in making efficient use of ingredients already present
in their kitchen. By bridging the gap between available resources and possible meal options,
the system provides a practical and intelligent solution to a common real-world problem.
The system accepts a dynamic list of ingredients as input and models the relationship between
ingredients and recipes in the form of a graph. It employs the Breadth-First Search (BFS)
algorithm as its core search mechanism to traverse this ingredient–recipe graph, ensuring that
all possible relevant recipes connected to the input ingredients are efficiently explored. This
guarantees that no viable recipe option is missed during the search process.

To further refine the results, a heuristic scoring function is applied to rank the discovered
recipes. The scoring is based on two key factors: the proportion of matched ingredients and the
penalty for missing ingredients. This approach ensures that recipes requiring fewer additional
ingredients are prioritized, while still allowing partially matching recipes to be considered.
Additionally, rule-based filtering is used to eliminate irrelevant results, thereby improving the
accuracy and usefulness of recommendations.

The system is implemented as a web-based application using Python and Flask for the backend,
and HTML, CSS, and JavaScript for the frontend interface. A curated dataset of approximately
30 recipes, including common Indian dishes and everyday meals, is used for demonstration.
The application provides clear outputs, including recipe names, match percentages, ingredient
availability status, and step-by-step cooking instructions, making it both user-friendly and
explainable.

Overall, the proposed system is lightweight, efficient, and easy to deploy, making it suitable
for academic demonstration as well as practical use. By combining fundamental Artificial
Intelligence concepts such as graph search, heuristic evaluation, and rule-based filtering, the
project successfully delivers a functional tool that promotes smarter cooking decisions and
contributes to the reduction of household food waste.
