# 📘 PROJECT SUMMARY  
## 🧾 ReceiptIQ – AI Powered Receipt Expense Tracker

A complete AI-based system that transforms paper receipts into structured digital insights using **OCR, Machine Learning, Forecasting, Analytics, and Interactive Dashboards**.

---

## 📂 1. SROIE2019 Dataset Analyzer

This Python script analyzes the **SROIE2019 receipt dataset** in Kaggle to understand its structure and verify that all important files are present before training any AI model. It uses `Path()` from `pathlib` because it provides cleaner and more reliable file path handling than traditional `os` methods. Helper functions like `count_files()` count all files recursively, `folder_size_mb()` calculates storage usage, and `sample_files()` previews filenames for quick inspection. Then it creates a `pandas DataFrame` because tabular output is easier to read and compare than plain text printing. After that, it prints detailed folder contents such as subfolders and files. Finally, it checks important paths like `test/box` for annotation `.txt` files and the pretrained `LayoutLM` model directory used for document understanding tasks. In short, it is a dataset validation script to confirm the data is complete, organized, and ready for machine learning workflows.

🔧 **Tools Used:** `pandas`, `pathlib`, `os`  
🎯 **Purpose:** Dataset inspection and preprocessing readiness

---

## 🤖 2. AI Concepts in Receipt Expense Tracker

This Python script demonstrates the **core AI concepts used in a Receipt Expense Tracker** by simulating receipt data and applying machine learning models. It first creates a dataset using `pandas DataFrame`, which is ideal for structured data handling. Using `re.search()`, it extracts total amounts from receipt text because regular expressions are effective for pattern-based text detection. Then `TfidfVectorizer()` converts receipt text into numerical vectors by measuring word importance, which is necessary because machine learning models cannot directly process raw text. After splitting data using `train_test_split()`, it trains three models: `MultinomialNB()` for fast text classification, `SVC()` for accurate category separation, and `MLPClassifier()` as a neural network for learning complex patterns. Their performance is measured using `accuracy_score()`, while Matplotlib is used to compare results visually through charts. It also uses `LinearRegression()` because it is simple and effective for predicting future expenses based on trends. Finally, it predicts categories for new receipts and uses `groupby()` for spending summaries. In short, this script explains how text AI + ML + forecasting can power expense tracking.

🔧 **Tools Used:** `scikit-learn`, `pandas`, `matplotlib`, `regex`  
🎯 **Purpose:** Expense classification and prediction

---

## 📊 3. Advanced AI Based Receipt Expense Tracker

This Python script builds an **AI Based Receipt Expense Tracker** with analytics for multiple users. It stores person names, receipt text, categories, and amounts inside a `pandas DataFrame`, which makes grouping and statistical analysis easier. `re.search()` is used again to detect totals directly from receipt text. `TfidfVectorizer()` converts receipt descriptions into feature vectors so that machine learning models can classify expenses. It trains `MultinomialNB()` because Naive Bayes works well for text data, `SVC()` because Support Vector Machines often give strong accuracy for classification, and `MLPClassifier()` because neural networks can learn more hidden relationships in text. Their scores are compared using `accuracy_score()` and visualized with Matplotlib charts.

The script also uses `groupby()` for person-wise totals, category-wise summaries, and favorite spending categories because aggregation is one of pandas’ strongest features. Pie charts and heatmaps help compare spending visually. `LinearRegression()` is used to forecast next month’s expenses using historical data trends. It also predicts categories for new receipts in real time. Finally, it generates insights such as highest spender, lowest spender, and average bill value. In short, this script expands the basic tracker into a multi-user analytics system.

🔧 **Tools Used:** `pandas`, `matplotlib`, `scikit-learn`  
🎯 **Purpose:** Multi-user financial analytics

---

## 🧠 4. ReceiptDNA – Visual Intelligence Edition

This Python script builds **ReceiptDNA – Visual Intelligence Edition**, an enterprise-grade expense intelligence platform. It uses `pandas` and `numpy` for data cleaning and numerical analysis, while Matplotlib, Seaborn, and Plotly are used because they provide static charts, statistical visuals, and interactive dashboards respectively. If real receipt files are unavailable, it generates synthetic data so the system can still demonstrate full analytics. Additional features like date, time, confidence score, weekday, and month are created because richer features improve analysis quality.

The script performs summaries using `groupby()` and advanced segmentation using `KMeans()`, which groups similar spending behaviors automatically. `PCA()` reduces multiple features into two dimensions so clusters can be visualized clearly. Users are labeled into profiles such as High Spender or Conscious Saver. For forecasting, it combines `LinearRegression()`, `Ridge()`, and `RandomForestRegressor()` because ensemble approaches often improve prediction reliability. `IsolationForest()` is used for anomaly detection because it efficiently finds unusual spending patterns without needing labeled data. Correlation matrices, treemaps, scatter plots, and heatmaps help decision-making. Finally, it outputs recommendations and executive summaries. In short, this script is a professional BI + AI solution for expense intelligence.

🔧 **Tools Used:** `Plotly`, `Seaborn`, `KMeans`, `PCA`, `IsolationForest`  
🎯 **Purpose:** Business intelligence and smart analytics

---

## 🌐 5. Final Expense Tracker Web App

This Python script builds a complete **AI-powered Receipt Expense Tracker Web App** with a chat-style interface using Gradio. Gradio is used because it quickly converts Python projects into interactive web applications without needing full frontend frameworks. It imports `easyocr`, `opencv (cv2)`, `pandas`, and `numpy` to process images and manage receipt data. The `ReceiptManager` class stores receipts, prevents duplicates, calculates totals, averages, monthly spending, category totals, and recent uploads. This class-based design keeps data organized and scalable.

The `OCRProcessor` class uses EasyOCR because it can detect printed text directly from images without needing custom OCR training. `cv2` converts images to grayscale first, which improves OCR accuracy. `re.findall()` is used to detect amounts like `123.45`, and keyword matching assigns categories such as Groceries, Food, Shopping, Bills, or Healthcare.

The app includes chatbot commands like **summary**, **recent**, **categories**, **this month**, and **advice**, making it easier for users to query expenses naturally. Multiple receipts can be uploaded together, processed instantly, and stored in memory. It supports CSV export using `pandas.DataFrame.to_csv()` so users can download records. Custom HTML/CSS inside `gr.Blocks()` is used to design a professional dashboard with sidebar metrics, recent receipts, and spending insights. In short, this final project combines OCR + AI categorization + analytics + chatbot UI into a smart personal finance assistant ready for real users.

🔧 **Tools Used:** `Gradio`, `EasyOCR`, `OpenCV`, `pandas`  
🎯 **Purpose:** Real-world AI finance assistant

---

## 🔁 End-to-End Workflow

```text
Receipt Image
   ↓
OCR Text Extraction
   ↓
Store / Date / Amount Detection
   ↓
Feature Engineering
   ↓
Expense Classification
   ↓
Analytics Dashboard
   ↓
Forecasting & Recommendations
