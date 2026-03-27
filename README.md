# 🏦 Agentic AI for Intelligent Account Opening & Onboarding


---

## 🚀 Overview

An AI-powered digital banking onboarding system that automates identity verification and decision-making using intelligent agents.

This project simulates a **next-generation fintech onboarding system** that reduces fraud, speeds up verification, and enables **real-time decision making (Approve / Reject / Review)**.

---

## 🎬 Demo (Live Preview)

![Demo GIF](screenshots/demo.gif)

> 📌 Add a screen recording GIF of your project inside `screenshots/demo.gif`

---

## ✨ Key Features

* 🔐 Secure User Authentication (JWT-based)
* 🧾 PAN Card Verification (AI-based OCR)
* 🪪 Aadhaar Verification
* 🤳 Face Recognition & Matching (OpenCV)
* 🚨 Fraud Detection System
* 🧠 Automated Decision Engine
* 📊 Risk Score Visualization (Graphs)
* 📄 PDF Report Generation
* 💾 Auto Save & Resume Application
* 🛠 Admin Dashboard for Monitoring

---

## 🧠 System Architecture

![Architecture Diagram](screenshots/architecture.png)

### 🔹 AI Agent Flow

* **PAN Agent** → Extracts & validates PAN details using OCR
* **Aadhaar Agent** → Verifies identity data
* **Face Agent** → Matches selfie with ID using face recognition
* **Fraud Agent** → Detects anomalies and suspicious patterns
* **Decision Engine** → Generates final decision

---

## 🔄 Workflow

1. User fills account opening form
2. Uploads identity documents
3. Captures selfie
4. AI agents process data:

   * PAN Verification
   * Aadhaar Validation
   * Face Matching
   * Fraud Detection
5. Decision Engine evaluates risk
6. Final result generated:

   * ✅ Approved
   * ❌ Rejected
   * ⚠️ Under Review
7. Dashboard displays insights

---

## 🔌 API Endpoints

### 🔐 Authentication

| Method | Endpoint        | Description            |
| ------ | --------------- | ---------------------- |
| POST   | `/api/register` | Register new user      |
| POST   | `/api/login`    | Login user (JWT token) |

---

### 📄 Document Processing

| Method | Endpoint              | Description        |
| ------ | --------------------- | ------------------ |
| POST   | `/api/upload/pan`     | Upload PAN card    |
| POST   | `/api/upload/aadhaar` | Upload Aadhaar     |
| POST   | `/api/upload/selfie`  | Upload user selfie |

---

### 🤖 AI Processing

| Method | Endpoint              | Description           |
| ------ | --------------------- | --------------------- |
| POST   | `/api/verify/pan`     | PAN verification      |
| POST   | `/api/verify/aadhaar` | Aadhaar verification  |
| POST   | `/api/verify/face`    | Face matching         |
| POST   | `/api/fraud/check`    | Fraud detection       |
| POST   | `/api/decision`       | Final decision engine |

---

### 📊 Dashboard

| Method | Endpoint          | Description         |
| ------ | ----------------- | ------------------- |
| GET    | `/api/dashboard`  | Get user results    |
| GET    | `/api/report/pdf` | Download PDF report |

---

## 🧠 Tech Stack

### 🎨 Frontend

* React.js (TypeScript)
* Tailwind CSS
* Framer Motion
* Recharts

### ⚙ Backend

* Python (Flask)
* JWT Authentication
* REST APIs

### 🤖 AI / ML

* OpenCV (Face Recognition)
* OCR (Text Extraction)
* Custom Fraud Detection Logic

### 🗄 Database

* MySQL

---

## 📂 Project Structure

```bash
Agentic_AI/
│
├── backend/
│   ├── app/
│   ├── agents/
│   ├── routes/
│   └── ml_training/
│
├── frontend/
│   ├── src/
│   └── components/
│
├── screenshots/
│
└── README.md
```

---

## ⚙️ Setup & Installation

### 1️⃣ Clone Repository

```bash
git clone https://github.com/awaresakshi/Agentic_AI.git
cd Agentic_AI
```

### 2️⃣ Backend Setup

```bash
cd backend
pip install -r requirements.txt
python run.py
```

### 3️⃣ Frontend Setup

```bash
cd frontend
npm install
npm run dev
```

---

## 🔒 Security & Best Practices

* JWT-based authentication
* Secure API handling
* Input validation & sanitization
* Modular AI architecture
* Sensitive data protection

---

## 📊 Output

* Risk score visualization
* AI-based decision results
* Fraud detection alerts
* Downloadable PDF reports

---

## 📌 Future Enhancements

* Government API integration (PAN/Aadhaar)
* Advanced ML fraud detection models
* Cloud deployment (AWS / Azure)
* Docker containerization
* CI/CD pipeline integration

---

## 👩‍💻 Author

**Sakshi Aware**
B.Tech Computer Science

---

## ⭐ Show Your Support

If you like this project, give it a ⭐ on GitHub!
