# ReceiptIQ - Privacy-First Personal Finance Agent

<div align="center">

![ReceiptIQ](https://img.shields.io/badge/ReceiptIQ-AI%20Expense%20Tracker-10A37F?style=for-the-badge)

**Turn messy paper receipts into clean financial insights using AI.**

[![Kaggle](https://img.shields.io/badge/Kaggle-Notebook-20BEFF?style=flat-square&logo=kaggle)](https://www.kaggle.com/code/mrrogueknight/receiptiq)
[![GitHub](https://img.shields.io/badge/GitHub-Repo-181717?style=flat-square&logo=github)](https://github.com/MrRogueKnight/privacy-first-personal-finance-agent)

Maintained by **Prashant Ranjan** ([@MrRogueKnight](https://github.com/MrRogueKnight))

</div>

---

## Why We Built This

Manual expense tracking is slow, repetitive, and often ignored. Most people don't track spending because it's tedious.

ReceiptIQ was built to automate personal finance tracking using OCR and machine learning while keeping user data completely private. No cloud uploads. No third-party APIs. Just local processing that works.

---

## What It Does

ReceiptIQ extracts receipt data using **OCR**, auto-categorizes expenses with **machine learning**, and delivers **privacy-first analytics dashboards**. Upload receipt images, ask questions in plain English, and get instant spending insights.

**All receipt data is processed locally for maximum privacy.**

---

## Repository Highlights

- Privacy-first AI project
- End-to-end ML application
- Real-world OCR use case
- Multi-member collaboration
- Recruiter-ready engineering project

---

## Key Features

| Feature | Description |
|---------|-------------|
| **Receipt OCR** | Upload photos of receipts, extract store, date, amount |
| **Smart Categorization** | ML automatically categorizes expenses (Food, Transport, Shopping, etc.) |
| **Chat Interface** | Ask "How much did I spend on food?" or "Show me last month" |
| **Spending Analytics** | Category breakdown, monthly trends, average transaction value |
| **Multi-Receipt Upload** | Process dozens of receipts in one go |
| **CSV Export** | Download all transactions for tax or budgeting |

**Advanced Analytics (ReceiptDNA):**
- Spending personas via clustering
- Anomaly detection for unusual transactions
- 7-day spend forecasting
- Interactive visualizations

---

## Engineering Challenges Solved

- Extracting noisy text from low-quality receipt images
- Detecting totals across different receipt formats (currency symbols, positions, spacing)
- Preventing duplicate receipt entries using hash-based indexing
- Building fast local OCR workflows without GPU dependency
- Designing category prediction from sparse, short receipt text
- Handling OCR failures gracefully with fallback logic

---

## Design Decisions

| Decision | Why |
|----------|-----|
| **EasyOCR over Cloud APIs** | Offline processing, no data leaves machine, free |
| **TF-IDF + Classical ML** | Lightweight inference, no GPU needed, fast startup |
| **Privacy-first approach** | No cloud dependency = trust + zero cost |
| **Gradio for UI** | Rapid prototyping, Python-native, easy sharing |
| **Local data storage** | User owns their financial data completely |

---

## Tech Stack

```
Frontend:    Gradio, Plotly, Matplotlib
OCR:         EasyOCR
ML:          scikit-learn (SVM, Random Forest, K-Means, Isolation Forest)
Data:        Pandas, NumPy
Vision:      OpenCV, PIL
```

---

## Core Modules

```
┌─────────────┐     ┌─────────────┐     ┌─────────────┐
│ OCR Engine  │────▶│   Receipt   │────▶│  Expense    │
│  (EasyOCR)  │     │   Parser    │     │ Classifier  │
└─────────────┘     └─────────────┘     └─────────────┘
                                              │
                                              ▼
┌─────────────┐     ┌─────────────┐     ┌─────────────┐
│ Chat Query  │◀────│  Analytics  │◀────│   Export    │
│    Layer    │     │   Engine    │     │   Manager   │
└─────────────┘     └─────────────┘     └─────────────┘
```

---

## Skills Demonstrated

**Python** | **OCR** | **Machine Learning** | **Data Pipelines** | **UI Prototyping** | **Feature Engineering** | **Forecasting** | **Anomaly Detection** | **Clustering** | **Git Collaboration**

---

## Performance Focus

ReceiptIQ is optimized for:

- **Fast local inference** - No API calls, no waiting
- **Low setup complexity** - Run from Kaggle or local in minutes
- **Practical accuracy** - Works reliably on common receipt layouts
- **Expandability** - Easy to add new categories or training data

> *Prototype benchmarking completed on SROIE2019 dataset. Production training underway using larger labeled receipt corpora.*

---

## Key Learnings

This project improved my understanding of:

- **OCR limitations** - Text extraction quality varies dramatically with image quality
- **Feature engineering** - TF-IDF on short receipt text requires careful preprocessing
- **Model selection** - Simple classifiers often beat complex ones for structured text
- **Shipping usable AI** - The UI/chat layer matters as much as the model
- **Tradeoffs** - Privacy vs features, speed vs accuracy, simplicity vs sophistication

---

## Roadmap

- [ ] Multi-language receipt support
- [ ] Better merchant name detection
- [ ] Budget alerts when exceeding category limits
- [ ] PDF monthly reports with spending insights
- [ ] Mobile-first version (React Native wrapper)
- [ ] Email receipt forwarding (Gmail integration)

---

## Team & Roles

| Role | Member | Responsibilities |
|------|--------|------------------|
| **Team Lead** | **Prashant Ranjan** | Project planning, architecture, final integration, repository management |
| **ML Engineer** | **Ritik Prajapati** | Expense classification models, TF-IDF pipeline, model evaluation |
| **Data Engineer** | **Rayapurreadyy Hema Sundhar** | Dataset preparation, preprocessing, OCR data handling |
| **Backend Developer** | **Venkata Nivas Yalla** | Receipt manager logic, storage flow, exports, system backend |
| **Frontend Developer** | **Grihshant Manash Datta** | Gradio UI, interaction flow, usability improvements |
| **Analytics Engineer** | **Chandragiri Navdeep** | Forecasting, anomaly detection, clustering insights |
| **QA & Documentation** | **Baldev Singh Jadon** | Testing, bug validation, documentation quality |

---

## Quick Start

### Run on Kaggle (Recommended)

1. Open the [Kaggle Notebook](https://www.kaggle.com/code/mrrogueknight/receiptiq)
2. Click **Copy and Edit** to create your own copy
3. Run all cells sequentially
4. The Gradio interface will launch with a public URL

### Local Setup

```bash
# Clone the repository
git clone https://github.com/MrRogueKnight/privacy-first-personal-finance-agent.git
cd privacy-first-personal-finance-agent

# Install dependencies
pip install -r requirements.txt

# Run the app
python expense_tracker.py
```

Then open http://127.0.0.1:7860 in your browser.

---

## AI Pipeline

```
Receipt Image
      ↓
   OCR Engine (EasyOCR)
      ↓
   Text Extraction & Cleaning
      ↓
   TF-IDF Feature Extraction
      ↓
   ML Classification (SVM/Random Forest)
      ↓
   Category Prediction
      ↓
   Analytics Engine
      ↓
   Dashboard & Export
```

---

## Documentation

| File | Description |
|------|-------------|
| [TEAM.md](./TEAM.md) | Team members, roles, and responsibilities |
| [RESULTS.md](./RESULTS.md) | Performance metrics, benchmarks, insights |
| [ARCHITECTURE.md](./ARCHITECTURE.md) | System design, data flow, model details |

---

## License

MIT License.  
Dataset subject to original SROIE terms.

---

<div align="center">

Built with Python, OCR, and Machine Learning by Team ReceiptIQ.

[⬆ Back to Top](#receiptiq---privacy-first-personal-finance-agent)

</div>
