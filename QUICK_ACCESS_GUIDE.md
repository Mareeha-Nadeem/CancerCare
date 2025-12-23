# 🚀 Quick Access to Data Science Scripts

## ❌ Problem
You were trying to run:
```bash
python preprocess.py  # ❌ File not in root directory
```

But the file is actually at: `data_science/model_1/preprocess.py`

---

## ✅ Solution: Python Helper Script

Use the **`run_ds.py`** helper script to run any data science script from the project root:

### **Basic Usage:**
```bash
python run_ds.py preprocess    # Run preprocessing
python run_ds.py train         # Train model
python run_ds.py predict       # Make predictions
python run_ds.py interface     # Interactive interface
```

### **Alternative (Direct Access):**
```bash
python data_science\model_1\preprocess.py
python data_science\model_1\train_model.py
python data_science\model_1\prediction.py
python data_science\model_1\interface.py
```

---

## 📋 Available Scripts

| Script | Command | Description |
|--------|---------|-------------|
| **Preprocess** | `python run_ds.py preprocess` | Clean and prepare data |
| **Train** | `python run_ds.py train` | Train ML model |
| **Predict** | `python run_ds.py predict` | Make predictions |
| **Interface** | `python run_ds.py interface` | Interactive prediction tool |

---

## 🎯 Quick Start

**1. Preprocess Data:**
```bash
python run_ds.py preprocess
```

**2. Train Model:**
```bash
python run_ds.py train
```

**3. Test Predictions:**
```bash
python run_ds.py predict
```

---

## 📁 File Locations

All data science scripts are in: `data_science/model_1/`

```
data_science/
└── model_1/
    ├── preprocess.py       # Data preprocessing
    ├── train_model.py      # Model training
    ├── prediction.py       # Make predictions
    ├── interface.py        # Interactive interface
    ├── feature_engineer.py # Feature engineering
    ├── data/              # Training data
    ├── models/            # Trained models
    └── results/           # Model results
```

---

## ✨ Examples

**Preprocess and Train:**
```bash
python run_ds.py preprocess
python run_ds.py train
```

**Make Single Prediction:**
```bash
python run_ds.py interface
# Then follow interactive prompts
```

---

## 🔧 Troubleshooting

**Error:** `File not in root directory`
**Fix:** Always run from project root
```bash
cd "e:\Project\CancerCare -- Copy"
```

**Error:** `ModuleNotFoundError`
**Fix:** Activate virtual environment first
```bash
.\.venv\Scripts\Activate.ps1
python run_ds.py train
```

---

## 💡 Pro Tips

1. **Always run from project root** - Don't navigate to `data_science/model_1/`
2. **Activate venv first** - Make sure virtual environment is active
3. **Use the helper** - `python run_ds.py` is easier than typing full paths

---

**Now you can access all data science scripts easily!** 🎉
