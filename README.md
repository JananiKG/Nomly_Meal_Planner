# Nomly_Meal_Planner
Our first every GenAI driven meal planner! Woohooo! 

# High level architecture
[User Browser]
     │
     │  (localhost:8501)
     ▼
[Streamlit UI]
     │  REST calls (JSON)
     │
     │  (localhost:8000)
     ▼
[FastAPI Backend]
 ┌────────────────────────────────────────────────────────────┐
 │  Routers (HTTP)    |  Services           |  Storage        │
 │  ───────────────── |  ────────────────── |  ─────────────  │
 │  /goals/*          |  AIProvider         |  JSON files     │
 │  /inventory/*      |   └ generate()      |   meals.json    │
 │  /meals/*          |  MealPlanner        |   inventory.json│
 │  /grocery/*        |  InventoryService   |  (later: SQLite)│
 └────────────────────────────────────────────────────────────┘
     │
     │ outbound HTTPS
     ▼
[Gemini API (today)]
[Other LLMs via provider adapter (future)]

# File layout
meal_planner_app/
├── frontend/
│   └── app.py
├── backend/
│   ├── main.py                 # FastAPI app + routers
│   ├── models.py               # pydantic schemas
│   ├── services/
│   │   ├── meal_planner.py
│   │   ├── inventory_service.py
│   │   └── ai/
│   │       ├── base.py         # AIProvider protocol
│   │       ├── gemini.py       # current provider
│   │       └── factory.py      # env VAR selects provider
│   ├── storage/
│   │   ├── repo.py             # read_json(path), write_json(path)
│   │   └── paths.py            # constants for data paths
│   ├── prompts/
│   │   ├── system.txt
│   │   └── examples/
│   └── config.py               # settings (env vars, paths)
└── data/
    ├── inventory.json
    └── meals.json
