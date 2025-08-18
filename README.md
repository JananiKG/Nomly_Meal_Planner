# 🍽️ Nomly_Meal_Planner
Our first every GenAI driven meal planner! Woohooo! 


This project is an **AI-driven meal planner** that generates meal plans based on user goals (calories, protein, energy) and available grocery inventory. It integrates **FastAPI** for API exposure, and currently supports **Gemini AI** as the LLM provider.

---

## 📌 Project Status  

We are currently working on **Feature 1.2: AI-Generated Meal Plans**.  
Here’s a detailed breakdown of what has been achieved and what remains.  

---

## ✅ Completed Tasks (Feature 1.2 Progress)

- [x] **AI Provider Abstraction**
  - Base `AIProvider` class (`backend/services/ai/base.py`)
  - `GeminiProvider` (`backend/services/ai/gemini.py`) with `generate` method

- [x] **Data Models with Validation**
  - `Ingredient`, `Meal`, `MealPlan` with Pydantic validation
  - Rules enforced (e.g., at least one meal required)

- [x] **MealPlanner Service**
  - Prompt builder for goals + inventory
  - JSON parsing into `MealPlan` objects
  - Fail-Fast Mode implemented (Safe Mode planned)

- [x] **FastAPI Integration**
  - `/generate-meal-plan` endpoint created
  - Input validation + structured JSON response
  - Error handling for invalid AI output

---

## 🔄 Current Work (Ongoing in Feature 1.2)

- [ ] Debugging Gemini API responses (sometimes invalid JSON)
- [ ] Improving reliability of structured AI output
- [ ] Evaluating **Safe Mode vs Fail-Fast Mode**

---

## 📝 Remaining Work (Feature 1.2 Next Steps)

- [ ] Finalize decision on Safe Mode handling  
- [ ] Improve prompt engineering for better JSON responses  
- [ ] Write **unit tests** for:
  - MealPlanner parsing
  - AIProvider integration
  - FastAPI endpoint responses
- [ ] Update README with API request/response examples  
- [ ] Prepare for **Feature 1.3: Persistence Layer** (DB storage for meal plans)  

---

## 📊 Visual Progress Tracker  

### **Feature 1.2: AI-Generated Meal Plans**
- [x] Setup AI Provider abstraction  
- [x] Define Pydantic models with validation  
- [x] Implement MealPlanner service  
- [x] Integrate FastAPI endpoint  
- [ ] Debug & test Gemini AI responses  
- [ ] Add Safe Mode / finalize validation approach  
- [ ] Write unit tests  
- [ ] Document API usage  

---

## 🚀 How to Run Locally

### 1. Clone the repository
```bash
git clone <repo-url>
cd meal_planner_app
```
2. Install dependencies

`pip install -r requirements.txt`

4. Run FastAPI app
`uvicorn backend.main:app --reload`

5. Test API
```
Send a POST request to:

http://127.0.0.1:8000/generate-meal-plan


Example body:

{
  "goals": {"calories": 2000, "protein": 120},
  "inventory": ["chicken", "rice", "broccoli", "eggs"]
}
```

📅 Roadmap

Feature 1.2 (In Progress) → AI-Generated Meal Plans

Feature 1.3 (Upcoming) → Store Meal Plans in Database

Feature 1.4 (Future) → User Authentication & Personalization

Feature 1.5 (Future) → Frontend UI Integration
