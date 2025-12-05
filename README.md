# LEWA – AI Tutor for GCE OL & AL Students (Cameroon)

LEWA is an AI‑powered educational assistant designed to help **GCE Ordinary Level (OL)** and **Advanced Level (AL)** students in Cameroon study more effectively. The platform provides subject‑specific AI responses, web research, analytics tools, and exam‑focused guidance.

This project consists of:

* **Next.js Frontend** (UI + interaction)
* **FastAPI Backend** (subject routing, AI logic, tools integration)
* **Lightweight AI model integration** optimized for low‑RAM machines

---

## 🔥 Key Features

### **1. Subject‑Specific AI Chat**

* Sidebar listing **11 subjects**:

  * Mathematics, English, Geography, Literature, Physics, Economics
  * Chemistry, Biology, History, French, Religious Studies
* Each subject has its own AI endpoint.
* AI only answers questions within the activated subject.
* If a user asks a Chemistry question while Mathematics is selected → bot politely declines.

### **2. Subject Mode Selector (OL / AL)**

* A card appears when a subject is selected.
* User selects either **OL** or **AL** mode.
* Activated mode changes color to show it is active.
* Only after selecting the mode can the user click **Start** to open the chat window.

### **3. Integrated Tools Menu**

A small menu with 3 tools:

#### **🧠 Researcher**

* Performs live web searches.
* Gives updated information from trusted sources.

#### **📊 Analytics Tool**

* Plots graphs and mathematical visualizations.
* For example, a math function can be calculated and displayed.

#### **📨 Messenger**

* Fetches announcements & updates from the GCE Board.
* Searches the web for latest exam notices.
* Provides smart notifications.

---

## 🏗️ Project Structure

Recommended monorepo layout:

```
lewa/
│
├── frontend/        # Next.js app
│   ├── app/
│   ├── components/
│   ├── public/
│   └── package.json
│
└── backend/         # FastAPI app
    ├── app/
    │   ├── main.py
    │   ├── routers/
    │   │   ├── maths.py
    │   │   ├── english.py
    │   │   └── ... (all 11 subjects)
    │   ├── tools/
    │   │   ├── researcher.py
    │   │   ├── analytics.py
    │   │   └── messenger.py
    │   └── core/
    ├── requirements.txt
    └── .env.example
```

---

## ⚙️ Backend (FastAPI) Overview

### Features Implemented at Backend Level

* Subject‑specific endpoints → `/api/maths`, `/api/biology`, etc.
* Mode‑aware AI handling (OL / AL)
* Tools endpoints:

  * `/api/tools/researcher`
  * `/api/tools/analytics`
  * `/api/tools/messenger`
* AI model integration using lightweight efficient models.
* Textbook embedding & retrieval (future enhancement).

---

## 🎨 Frontend (Next.js) Overview

The frontend provides:

* Sidebar navigation for all subjects.
* Dynamic chat surface that updates based on subject & mode.
* A Start button that unlocks the chat window.
* Tool menu toggle.
* Reusable components for cards, buttons, chat bubbles.

---

## 🚀 Getting Started

### **1. Run Next.js Frontend**

Assuming dependencies are installed:

```
npm run dev
```

### **2. Start FastAPI Backend**

Assuming dependencies are installed:

```
uvicorn app.main:app --reload
```

---

## 📝 Contribution Guidelines

* Use feature branches
* Push only after testing
* Naming format: `feature-subject-maths`, `fix-tools-analytics`
* Use PR reviews

---

## 📜 License

MIT License.

---

## 🏁 Final Notes

LEWA is designed to support students in Cameroon by providing an affordable, accurate, and subject‑aware AI learning companion. This project aims to make modern AI accessible to students regardless of the device they use.