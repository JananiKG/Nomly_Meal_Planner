# 🍽️ Nomly Meal Planner

> **AI-Powered Meal Planning with Smart Inventory Management**

Transform your cooking experience with our intelligent meal planner that generates personalized meal plans based on your nutritional goals and available ingredients, while automatically tracking your inventory usage.

---

## ✨ **Features**

### 🤖 **AI-Generated Meal Plans**
- **Personalized nutrition**: Set calorie and protein targets
- **Inventory-aware**: Uses only ingredients you have available
- **Detailed recipes**: Step-by-step cooking instructions with precise measurements
- **Multiple providers**: Currently supports Gemini AI, extensible to OpenAI, Claude, etc.

### 📦 **Smart Inventory Tracking**
- **Automatic updates**: Tracks ingredient usage after meal generation
- **Quantity management**: Handles various units (grams, cups, pieces, liters)
- **Over-consumption alerts**: Warns when meal plans exceed available ingredients
- **Error handling**: Gracefully manages invalid quantities and unit mismatches

### 🏗️ **Clean Architecture**
- **Modular design**: Separate concerns for AI providers, business logic, and data models
- **Extensible**: Easy to add new AI providers or features
- **Type-safe**: Full Pydantic validation for data integrity
- **RESTful API**: FastAPI backend with automatic documentation

---

## 🏛️ **Architecture Overview**

```
┌─────────────────┐    HTTP/JSON    ┌──────────────────┐
│   Frontend      │◄──────────────►│   FastAPI        │
│   (Future)      │   localhost:8501│   Backend        │
└─────────────────┘                 │   localhost:8000 │
                                    └──────────┬───────┘
                                               │
                    ┌──────────────────────────┼──────────────────────────┐
                    │                          │                          │
            ┌───────▼────────┐    ┌───────────▼──────────┐    ┌─────────▼────────┐
            │  AI Providers  │    │   Business Logic     │    │   Data Layer     │
            │                │    │                      │    │                  │
            │ • GeminiAI     │    │ • MealPlanner        │    │ • Models         │
            │ • OpenAI (fut) │    │ • InventoryService   │    │ • Storage        │
            │ • Claude (fut) │    │ • Quantity Parser    │    │ • JSON Files     │
            └────────────────┘    └──────────────────────┘    └──────────────────┘
                    │
                    ▼
            ┌───────────────┐
            │  External AI  │
            │   Services    │
            │               │
            │ • Gemini API  │
            └───────────────┘
```

---

## 🚀 **Quick Start**

### **Prerequisites**
- Python 3.12+
- Gemini API Key

### **Installation**
```bash
# Clone the repository
git clone https://github.com/JananiKG/Nomly_Meal_Planner.git
cd Nomly_Meal_Planner

# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Set up environment variables
export GEMINI_API_KEY="your-gemini-api-key-here"
```

### **Run the Application**
```bash
# Start the FastAPI server
uvicorn backend.main:app --reload --host 0.0.0.0 --port 8000

# API Documentation available at: http://localhost:8000/docs
```

---

## 📡 **API Reference**

### **Base URL**
```
http://localhost:8000
```

### **Endpoints**

#### **Generate Meal Plan**
```http
POST /meals/generate
```

Generate AI-powered meal plan with automatic inventory tracking.

**Request Body:**
```json
{
  "goals": {
    "calories": 1800,
    "protein": 100
  },
  "inventory": [
    "chicken: 400g",
    "rice: 2 cups", 
    "broccoli: 300g",
    "eggs: 6 pieces"
  ]
}
```

**Response:**
```json
{
  "meal_plan": {
    "goals": {"calories": 1800, "protein": 100},
    "meals": [
      {
        "name": "Breakfast",
        "calories": "350 kcal",
        "protein": "30g",
        "ingredients_used": [
          {"name": "eggs", "quantity": "3 pieces"},
          {"name": "broccoli", "quantity": "50g"}
        ],
        "notes": [
          "Scrambled Eggs with Broccoli",
          "1. Steam 50g broccoli for 3 minutes",
          "2. Whisk 3 eggs with salt and pepper",
          "3. Cook eggs in pan until set",
          "4. Serve with steamed broccoli"
        ]
      }
    ],
    "notes": ["Nutritional values are estimates"]
  },
  "inventory_updates": {
    "before": {
      "chicken": "400g",
      "rice": "2 cups",
      "broccoli": "300g", 
      "eggs": "6 pieces"
    },
    "used": {
      "chicken": "250g",
      "rice": "1.5 cups",
      "broccoli": "150g",
      "eggs": "3 pieces"
    },
    "remaining": {
      "chicken": "150g",
      "rice": "0.5 cups", 
      "broccoli": "150g",
      "eggs": "3 pieces"
    },
    "warnings": []
  }
}
```

**Error Response:**
```json
{
  "detail": [
    {
      "loc": ["field_name"],
      "msg": "Error description",
      "type": "error_type"
    }
  ]
}
```

### **Future Endpoints (Roadmap)**
```http
GET    /meals                 # List saved meal plans
GET    /meals/{id}           # Get specific meal plan  
PUT    /meals/{id}           # Update meal plan
DELETE /meals/{id}           # Delete meal plan
POST   /meals/{id}/favorite  # Mark as favorite

GET    /inventory            # Get current inventory
POST   /inventory/items      # Add inventory items
PUT    /inventory/items/{id} # Update inventory item
DELETE /inventory/items/{id} # Remove inventory item
```

---

## 🗂️ **Project Structure**

```
nomly_meal_planner/
├── backend/
│   ├── main.py                    # FastAPI application entry point
│   ├── models/
│   │   └── meal_models.py         # Pydantic data models
│   ├── services/
│   │   ├── meal_planner.py        # Core business logic
│   │   ├── inventory_service.py   # Inventory management
│   │   └── ai/
│   │       ├── base.py           # AI provider interface
│   │       ├── gemini.py         # Gemini AI implementation
│   │       └── factory.py        # Provider factory (future)
│   ├── utils/
│   │   └── quantity_parser.py    # Quantity parsing & calculations
│   └── storage/
│       ├── repo.py               # JSON file operations
│       └── paths.py              # Storage paths
├── data/
│   ├── inventory.json            # Inventory storage
│   └── meals.json               # Meal history (future)
├── test/                        # Unit tests
├── requirements.txt             # Python dependencies
└── README.md                   # This file
```

---

## 🧪 **Key Features in Detail**

### **🎯 Smart Quantity Handling**
- **Multiple units**: Supports grams, cups, pieces, liters, etc.
- **Fraction support**: Handles "1/2 cup", "0.5 liters"
- **Unit normalization**: Recognizes "cup" vs "cups"
- **Error detection**: Identifies invalid quantities and unit mismatches

### **⚠️ Intelligent Error Handling**
```json
{
  "inventory_updates": {
    "remaining": {
      "chicken": "INSUFFICIENT: Need 500g, have 200g"
    },
    "warnings": [
      "Over-consumed chicken: Need 500g, have 200g",
      "Used ingredient not in inventory: beef",
      "Invalid quantity for rice: INVALID_QUANTITY: invalid"
    ]
  }
}
```

### **🔧 Extensible AI Provider System**
```python
# Easy to add new AI providers
class OpenAIProvider(AIProvider):
    def generate_meal_plan(self, goals, inventory):
        # OpenAI-specific implementation
        pass

# Just change one line in main.py
ai_client = OpenAIProvider()  # Instead of GeminiProvider()
```

---

## 🛠️ **Development**

### **Adding New AI Providers**
1. Create new provider class inheriting from `AIProvider`
2. Implement `generate_meal_plan()` method
3. Add provider-specific prompt engineering and response parsing
4. Update main.py to use new provider

### **Running Tests**
```bash
# Run unit tests
python -m pytest test/

# Run edge case tests
python test_edge_cases.py

# Run comprehensive validation
python test_final_validation.py
```

### **API Documentation**
Visit `http://localhost:8000/docs` for interactive API documentation powered by FastAPI's automatic OpenAPI generation.

---

## 🎯 **Roadmap**

### **✅ Completed (v1.2)**
- [x] AI-generated meal plans with detailed recipes
- [x] Automatic inventory tracking and updates
- [x] Comprehensive error handling and edge cases
- [x] Clean, modular architecture
- [x] Full API documentation

### **🚧 In Progress**
- [ ] Streamlit frontend interface
- [ ] SQLite database integration
- [ ] Meal history and favorites
- [ ] Grocery list generation

### **🔮 Future Features**
- [ ] Multiple AI provider support (OpenAI, Claude)
- [ ] Advanced unit conversions
- [ ] Nutritional analysis and recommendations
- [ ] Recipe sharing and community features
- [ ] Mobile app integration

---

## 🤝 **Contributing**

We welcome contributions! Please see our contributing guidelines and feel free to submit issues or pull requests.

### **Development Setup**
```bash
# Fork the repository
# Clone your fork
# Create feature branch
git checkout -b feature/your-feature-name

# Make changes and test
python test_final_validation.py

# Submit pull request
```

---

## 📄 **License**

This project is licensed under the MIT License - see the LICENSE file for details.

---

## 🙏 **Acknowledgments**

- **Google Gemini AI** for powering our meal plan generation
- **FastAPI** for the excellent web framework
- **Pydantic** for robust data validation
- **Contributors** who help make this project better

---

<div align="center">

**Made with ❤️ for better meal planning**

[🌟 Star this repo](https://github.com/JananiKG/Nomly_Meal_Planner) | [🐛 Report Bug](https://github.com/JananiKG/Nomly_Meal_Planner/issues) | [💡 Request Feature](https://github.com/JananiKG/Nomly_Meal_Planner/issues)

</div>
