# 🏆 Privacy-First Personal Finance Agent

### Edge AI • Document Intelligence • Fully Local Inference

<p align="center">
  <b>Turn raw receipts into structured financial insights — without sending data to the cloud.</b>
</p>

<p align="center">
  <a href="https://www.python.org/downloads/"><img src="https://img.shields.io/badge/python-3.9+-blue.svg"/></a>
  <a href="https://pytorch.org/"><img src="https://img.shields.io/badge/PyTorch-2.0+-red.svg"/></a>
  <a href="LICENSE"><img src="https://img.shields.io/badge/license-MIT-green.svg"/></a>
  <a href="https://www.kaggle.com/"><img src="https://img.shields.io/badge/Kaggle-GPU%20Ready-blue.svg"/></a>
  <a href="CONTRIBUTING.md"><img src="https://img.shields.io/badge/PRs-welcome-brightgreen.svg"/></a>
</p>

---

## 🔗 Project Links

* 📘 **Kaggle Notebook**
  https://www.kaggle.com/code/mrrogueknight/privacy-first-personal-finance-agent

* 💻 **GitHub Repository**
  https://github.com/MrRogueKnight/privacy-first-personal-finance-agent

---

## 🚀 What This Project Does

This system converts **unstructured receipt images → structured financial data → actionable insights**, using a **Vision-Language Model (VLM)** — all while keeping data **100% private and local**.

> No APIs. No cloud calls. No data leakage.

---

## 🎯 Why This Project Stands Out

* 🔒 **Privacy-First AI** → Fully offline inference
* ⚡ **Efficient LLM Usage** → 2B model with 4-bit quantization
* 🧠 **Real-World Engineering** → Handles messy outputs & memory limits
* 📊 **End-to-End System** → Not just ML — full pipeline + analytics
* 🏗️ **Production-Oriented Design** → Stable, scalable, modular

---

## 🧠 System Overview

```
Receipts → Preprocessing → VLM Extraction → JSON Cleaning
        → Categorization → Analytics → Export
```

### 🔹 Pipeline Breakdown

| Stage           | Description                            |
| --------------- | -------------------------------------- |
| Data Loader     | Discovers and loads receipt images     |
| Preprocessing   | Resize, orientation fix, normalization |
| VLM Extraction  | Qwen2-VL-2B extracts structured data   |
| Post-processing | Cleans malformed JSON outputs          |
| Categorization  | Classifies expenses into categories    |
| Analytics       | Generates financial insights           |
| Export          | CSV, JSON, TXT, visualizations         |

---

## 📊 Performance Snapshot

| Metric         | Value                   |
| -------------- | ----------------------- |
| Dataset        | SROIE (973 receipts)    |
| Model          | Qwen2-VL-2B (2B params) |
| GPU            | Tesla P100 (16GB)       |
| Avg Time       | ~12.65 sec/receipt      |
| Success Rate   | 93%                     |
| Total Accuracy | ~80–87%                 |
| VRAM Usage     | ~6.7 GB                 |

---

## ⚙️ Key Engineering Decisions

### 🔹 Model Selection

* Chose **Qwen2-VL-2B** over larger models
* Better stability + no Flash Attention dependency

### 🔹 Quantization Strategy

* **4-bit NF4** → ~50% memory reduction
* Minimal accuracy loss

### 🔹 Memory Management

* Explicit cleanup (`gc.collect()`, `empty_cache()`)
* Prevents long-run GPU crashes

### 🔹 Robust Output Handling

* Regex-based JSON repair
* Handles noisy LLM outputs reliably

---

## 📈 Example Outputs

* Structured receipt data (store, total, items)
* Category-wise expense breakdown
* Store frequency analysis
* Financial summaries

---

## 📁 Project Structure

```
├── notebooks/
│   └── kaggle_pipeline.ipynb
├── outputs/
│   ├── extracted_receipts.csv
│   ├── receipt_insights.json
│   ├── extraction_summary.txt
│   └── receipt_visualizations.png
├── src/
│   ├── data_loader.py
│   ├── extractor.py
│   ├── pipeline.py
│   └── analyzer.py
├── README.md
└── requirements.txt
```

---

## ▶️ Getting Started

### 1. Clone the Repository

```bash
git clone https://github.com/MrRogueKnight/privacy-first-personal-finance-agent.git
cd privacy-first-personal-finance-agent
```

### 2. Install Dependencies

```bash
pip install -r requirements.txt
```

### 3. Run Pipeline

```bash
python main.py
```

Or use the Kaggle notebook (recommended for GPU):

👉 https://www.kaggle.com/code/mrrogueknight/privacy-first-personal-finance-agent

---

## 🚧 Challenges Solved

| Problem               | Solution                       |
| --------------------- | ------------------------------ |
| GPU memory crashes    | Aggressive cleanup strategy    |
| Model incompatibility | Switched to stable VLM         |
| Broken JSON outputs   | Multi-stage sanitization       |
| Fake “local” models   | Ensured true offline execution |

---

## 🔄 Future Improvements

### 🔥 High Impact

* Replace keyword categorization with **zero-shot classification**
* Add **confidence scoring system**
* Introduce **evaluation metrics (Precision / Recall / F1)**
* Implement **micro-batching for speed optimization**

### 🚀 Roadmap

* Fine-tuning on receipts
* Multi-language support
* Streamlit / FastAPI UI
* ONNX / TensorRT acceleration
* Edge/mobile deployment

---

## 👥 Team

| Role         | Name                       | Contribution                           |
| ------------ | -------------------------- | -------------------------------------- |
| Team Lead    | Prashant Ranjan            | System design, integration, deployment |
| Developer    | Ritik Prajapati            | Pipeline, GPU optimization, VLM        |
| ML Engineer  | Rayapurreadyy Hema Sundhar | Model optimization, quantization       |
| Data Analyst | Grihshant Manas Datta      | Categorization, analytics              |

---

## 💡 Key Takeaways

* Small models + smart engineering > large models alone
* Privacy-first AI is achievable today
* Post-processing is critical in LLM systems
* Memory management is essential for production ML

---

## ⭐ Support & Contribution

If you find this project useful:

* ⭐ Star the repo
* 🔁 Share with others
* 🤝 Open a pull request

---

## 📜 License

MIT License
