# LEWA Backend - Your Three Subject Endpoints Guide

## 📋 Overview

You are building three subject endpoints for the LEWA AI Tutor platform:
1. **Geography** (`/api/geography`)
2. **Chemistry** (`/api/chemistry`)
3. **Economics** (`/api/economics`)

Each endpoint:
- Accepts a POST request with a **question** and **mode** (OL or AL)
- Returns an AI-powered answer tailored to the subject and level
- Refuses questions from other subjects (subject-aware AI)

---

## 🏗️ Backend Structure (Already Created)

```
backend/
├── app/
│   ├── main.py                    ✅ FastAPI app (DONE - all routers registered)
│   ├── schemas.py                 ✅ Pydantic models (DONE)
│   └── routers/
│       ├── __init__.py            ✅ Package marker (DONE)
│       ├── geography.py           ✅ Geography endpoint (DONE)
│       ├── chemistry.py           ✅ Chemistry endpoint (DONE)
│       └── economics.py           ✅ Economics endpoint (DONE)
├── requirements.txt               ✅ Dependencies (DONE)
└── venv/                          ✅ Virtual environment (DONE)
```

---

## 🚀 Running Your Backend

### Step 1: Activate Virtual Environment
```bash
cd /c/Users/nembobusiness/Desktop/LEWA/backend
source venv/Scripts/activate
```

### Step 2: Start the Server
```bash
uvicorn app.main:app --reload
```

You should see:
```
INFO:     Uvicorn running on http://127.0.0.1:8000 (Press CTRL+C to quit)
INFO:     Application startup complete
```

### Step 3: Access API Documentation
- **Swagger UI**: http://127.0.0.1:8000/docs
- **ReDoc**: http://127.0.0.1:8000/redoc
- **Root endpoint**: http://127.0.0.1:8000/

---

## 📝 Endpoint Specifications

### 1. Geography Endpoint
**URL**: `POST /api/geography`

**Request Body**:
```json
{
  "question": "What are the main relief features of Cameroon?",
  "mode": "OL"
}
```

**Response**:
```json
{
  "response": "[Geography Tutor - OL]: Your answer here...",
  "subject": "Geography",
  "mode": "OL"
}
```

**System Prompt Coverage** (OL):
- General Geography and Map reading
- Basic physical and human geography
- Cameroon's geography and resources
- World geography fundamentals

**System Prompt Coverage** (AL):
- Physical Geography (geomorphology, climatology)
- Human Geography (economic, political, social)
- Geography of Cameroon and Africa
- Regional and world geography
- Geographical research methods

---

### 2. Chemistry Endpoint
**URL**: `POST /api/chemistry`

**Request Body**:
```json
{
  "question": "What is the difference between ionic and covalent bonding?",
  "mode": "OL"
}
```

**Response**:
```json
{
  "response": "[Chemistry Tutor - OL]: Your answer here...",
  "subject": "Chemistry",
  "mode": "OL"
}
```

**System Prompt Coverage** (OL):
- Atomic structure and bonding
- States of matter and kinetic theory
- Chemical reactions and equations
- Acids, bases, and pH
- Periodic table and element properties
- Organic chemistry basics
- Extraction of metals
- Laboratory techniques

**System Prompt Coverage** (AL):
- Advanced atomic structure and bonding theories
- Thermodynamics and energy changes
- Chemical equilibrium and kinetics
- Redox reactions and electrochemistry
- Organic chemistry (mechanisms, synthesis)
- Analytical chemistry (titrations, spectroscopy)
- Coordination chemistry
- Nuclear chemistry and radioactivity

---

### 3. Economics Endpoint
**URL**: `POST /api/economics`

**Request Body**:
```json
{
  "question": "What is the relationship between demand and price?",
  "mode": "OL"
}
```

**Response**:
```json
{
  "response": "[Economics Tutor - OL]: Your answer here...",
  "subject": "Economics",
  "mode": "OL"
}
```

**System Prompt Coverage** (OL):
- Basic economic concepts (scarcity, opportunity cost)
- Demand and supply
- Price mechanism and market structures
- Production and productivity
- National income and living standards
- Money and banking
- Government economic policies
- International trade

**System Prompt Coverage** (AL):
- Microeconomic theory (utility, production, cost analysis)
- Market structures and firm behavior
- Macroeconomic principles (GDP, inflation, unemployment)
- International economics and trade
- Economic growth and development
- Monetary and fiscal policy
- Public finance and taxation
- Development economics

---

## 🧪 Testing Your Endpoints

### Option 1: Using Swagger UI (Easiest)
1. Go to http://127.0.0.1:8000/docs
2. Click on each endpoint (geography, chemistry, economics)
3. Click "Try it out"
4. Enter your test data
5. Click "Execute"

### Option 2: Using curl
```bash
# Geography Example
curl -X POST http://127.0.0.1:8000/api/geography \
  -H "Content-Type: application/json" \
  -d '{"question": "What is Mount Cameroon?", "mode": "OL"}'

# Chemistry Example
curl -X POST http://127.0.0.1:8000/api/chemistry \
  -H "Content-Type: application/json" \
  -d '{"question": "What is an atom?", "mode": "OL"}'

# Economics Example
curl -X POST http://127.0.0.1:8000/api/economics \
  -H "Content-Type: application/json" \
  -d '{"question": "What is supply and demand?", "mode": "OL"}'
```

### Option 3: Using Postman
1. Download Postman (postman.com)
2. Create a new request
3. Method: POST
4. URL: `http://127.0.0.1:8000/api/geography`
5. Body (JSON):
   ```json
   {
     "question": "Your question here",
     "mode": "OL"
   }
   ```
6. Send

---

## 🤖 Next Step: Integrating Real AI

Currently, your endpoints return **mock responses** for development/testing. To make them actually intelligent, you need to:

### Option A: Use OpenAI API (Recommended for production)
```python
import openai

async def call_gpt(system_prompt: str, user_message: str) -> str:
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_message}
        ],
        temperature=0.7,
        max_tokens=500
    )
    return response.choices[0].message.content
```

### Option B: Use Ollama (Free, runs locally)
```bash
# Install Ollama from ollama.ai
# Run: ollama run mistral (or any other model)
# Then use ollama's API endpoint
```

### Option C: Use HuggingFace
```python
from transformers import pipeline

pipe = pipeline("text-generation", model="gpt2")
response = pipe(system_prompt + user_message)
```

---

## 📋 Checklist for You

- [x] Understand the project requirements
- [x] Set up backend structure (routers, schemas)
- [x] Create Geography endpoint with OL/AL prompts
- [x] Create Chemistry endpoint with OL/AL prompts
- [x] Create Economics endpoint with OL/AL prompts
- [x] Register routers in main.py
- [ ] Test all three endpoints (use Swagger UI or curl)
- [ ] Verify responses are correct for OL/AL modes
- [ ] Choose and integrate a real AI model
- [ ] Test with actual AI responses
- [ ] Document your API changes
- [ ] Push to GitHub

---

## 💡 Tips & Best Practices

1. **Subject Awareness**: Each endpoint has rules to refuse questions from other subjects. This ensures the AI stays in its lane.

2. **Mode Awareness**: OL and AL prompts are different. OL is simpler, AL is more advanced. Ensure your AI model uses the right prompt.

3. **Cameroon Context**: All prompts include references to Cameroon (Mount Cameroon, Douala, FCFA, cocoa, etc.). This makes responses more relevant.

4. **Error Handling**: The endpoints check for:
   - Invalid mode (not "OL" or "AL")
   - Empty questions
   - Add more validation as needed

5. **CORS**: The backend allows requests from anywhere (`allow_origins=["*"]`). This lets the frontend call your API. In production, restrict to your frontend URL.

---

## 🔗 Integration with Frontend

The frontend will call your endpoints like this:
```javascript
// Frontend code
async function askQuestion(subject, question, mode) {
  const response = await fetch(`http://127.0.0.1:8000/api/${subject}`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ question, mode })
  });
  return response.json();
}

// Example usage
const answer = await askQuestion("geography", "What is Mount Cameroon?", "OL");
console.log(answer.response);
```

---

## ❓ Troubleshooting

### Problem: "Module not found: fastapi"
**Solution**: Make sure you're in the venv:
```bash
source venv/Scripts/activate
```

### Problem: Port 8000 already in use
**Solution**: Use a different port:
```bash
uvicorn app.main:app --reload --port 8001
```

### Problem: CORS errors in frontend
**Solution**: Already handled! The backend allows CORS for all origins.

### Problem: Endpoint returns 422 error
**Solution**: Check your request JSON format. Mode must be "OL" or "AL", and question must not be empty.

---

## 📚 Resources

- **FastAPI Docs**: https://fastapi.tiangolo.com/
- **Pydantic Docs**: https://docs.pydantic.dev/
- **Uvicorn Docs**: https://www.uvicorn.org/
- **OpenAI API**: https://platform.openai.com/docs/
- **Ollama**: https://ollama.ai

---

**You're all set! Start with running the server and testing the endpoints.**

Questions? Let me know! 🚀
