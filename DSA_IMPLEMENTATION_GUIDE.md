# 📚 DSA (Data Structures & Algorithms) Implementation in CancerCare

## 🎯 Overview
The CancerCare project now features a **fully functional Search page** that demonstrates real-world applications of various Data Structures and Algorithms (DSA).

---

## 📍 Where DSA is Used

### **Location:** `frontend/search_page.py`
**Access:** Click "🔍 Search" in the sidebar navigation

This advanced search page implements **8 different DSA algorithms** for efficient patient data management and searching.

---

## 🧮 Implemented DSA Algorithms

### **1. Linear Search** 🔍
- **File:** `dsa/linearsearch.py`
- **Complexity:** O(n)
- **Use Case:** Find patient by name, MRN, or email
- **How to Use:**
  - Go to "Direct Search" tab
  - Select "Linear Search"
  - Choose search field (name/mrn/email)
  - Enter value
  - Click Search

**Code:**
```python
def linear_search(arr, key, value):
    for i, item in enumerate(arr):
        if item.get(key) == value:
            return i, item
    return -1, None
```

---

### **2. Binary Search** 🎯
- **File:** `dsa/linearsearch.py`
- **Complexity:** O(log n)
- **Use Case:** Fast search on sorted patient data
- **Requirement:** Data must be sorted first
- **How to Use:**
  - Go to "Direct Search" tab
  - Select "Binary Search (Sorted)"
  - Choose search field
  - Enter value
  - Click Search

**Code:**
```python
def binary_search(arr, key, value):
    low, high = 0, len(arr) - 1
    while low <= high:
        mid = (low + high) // 2
        mid_val = arr[mid].get(key)
        if mid_val == value:
            return mid, arr[mid]
        elif mid_val < value:
            low = mid + 1
        else:
            high = mid - 1
    return -1, None
```

---

### **3. Merge Sort** 📊
- **File:** `dsa/sorting.py`
- **Complexity:** O(n log n)
- **Use Case:** Sort patients alphabetically or by age
- **How to Use:**
  - Go to "Sort & Order" tab
  - Select "Name (Merge Sort)" or "Age (Merge Sort)"
  - Click Apply Sorting

**Code:**
```python
def merge_sort(arr, key):
    if len(arr) <= 1:
        return arr
    mid = len(arr) // 2
    left = merge_sort(arr[:mid], key)
    right = merge_sort(arr[mid:], key)
    return _merge(left, right, key)
```

---

### **4. Priority Queue (Max-Heap)** 🚨
- **File:** `dsa/patient_dsa.py`
- **Complexity:** O(log n) per operation
- **Use Case:** Triage patients - High risk + older patients first
- **How to Use:**
  - Go to "Sort & Order" tab
  - Select "Priority (High Risk + Older First)"
  - Click Apply Sorting

**Priority Logic:**
```
1. Risk Level (HIGH > MEDIUM > LOW)
2. Age (Older first)
3. Registration date (Earlier first)
```

**Code:**
```python
def order_by_priority(patients):
    heap = []
    for p in patients:
        risk_score = RISK_PRIORITY.get(risk_str, 1)
        age = int(p.get("age", 0))
        priority = (-risk_score, -age, created)
        heapq.heappush(heap, (priority, p))
    
    ordered = []
    while heap:
        _, patient = heapq.heappop(heap)
        ordered.append(patient)
    return ordered
```

---

### **5. FIFO Queue (First In, First Out)** ⏰
- **File:** `dsa/patient_dsa.py`
- **Complexity:** O(n log n) for sorting
- **Use Case:** Process patients in order of registration
- **How to Use:**
  - Go to "Sort & Order" tab
  - Select "FIFO (First In, First Out)"
  - Click Apply Sorting

**Code:**
```python
def order_by_fifo(patients):
    return sorted(
        patients,
        key=lambda p: p.get("created_at", "1970-01-01T00:00:00")
    )
```

---

### **6. LIFO Stack (Last In, First Out)** 🆕
- **File:** `dsa/patient_dsa.py`
- **Complexity:** O(n log n) for sorting
- **Use Case:** View recently registered patients first
- **How to Use:**
  - Go to "Sort & Order" tab
  - Select "LIFO (Last In, First Out)"
  - Click Apply Sorting

**Code:**
```python
def order_by_lifo(patients):
    return sorted(
        patients,
        key=lambda p: p.get("created_at", "1970-01-01T00:00:00"),
        reverse=True
    )
```

---

### **7. Linear Filtering** 🎯
- **File:** `dsa/patient_dsa.py`
- **Complexity:** O(n)
- **Use Case:** Multi-criteria patient filtering
- **Filters:**
  - Age range
  - Risk levels
  - Name substring
  - Gender
- **How to Use:**
  - Go to "Smart Filters" tab
  - Set filters (age, risk, name, gender)
  - Click Apply Filters

**Code:**
```python
def filter_patients(patients, age_range, allowed_risks, name_query):
    min_age, max_age = age_range
    result = []
    for p in patients:
        age = int(p.get("age", 0))
        risk = str(p.get("risk_level", "LOW")).upper()
        name = str(p.get("name", "")).lower()
        
        if not (min_age <= age <= max_age):
            continue
        if allowed_risks and risk not in allowed_risks:
            continue
        if name_query and name_query not in name:
            continue
        
        result.append(p)
    return result
```

---

### **8. Binary Search Tree (BST)** 🌳
- **File:** `dsa/patient_dsa.py`
- **Complexity:** O(log n) average case
- **Use Case:** Efficient age-range queries
- **How to Use:**
  - Go to "Advanced (BST)" tab
  - Set minimum and maximum age
  - Click Search BST

**Features:**
- Efficient range queries
- Self-balancing structure
- Fast age-based lookups

**Code:**
```python
class AgeBST:
    def insert(self, patient):
        # ... BST insertion logic
        
    def range_query(self, min_age, max_age):
        result = []
        def _dfs(node):
            if node is None:
                return
            if node.age > min_age:
                _dfs(node.left)
            if min_age <= node.age <= max_age:
                result.extend(node.patients)
            if node.age < max_age:
                _dfs(node.right)
        
        _dfs(self.root)
        return result
```

---

## 📊 DSA Complexity Comparison

| Algorithm | Time Complexity | Space Complexity | Best For |
|-----------|----------------|------------------|----------|
| Linear Search | O(n) | O(1) | Unsorted small data |
| Binary Search | O(log n) | O(1) | Sorted data |
| Merge Sort | O(n log n) | O(n) | General sorting |
| Priority Queue | O(log n) | O(n) | Triage/prioritization |
| FIFO Queue | O(n log n) | O(n) | Chronological order |
| LIFO Stack | O(n log n) | O(n) | Recent items |
| Linear Filter | O(n) | O(n) | Multi-criteria search |
| BST Range Query | O(log n + k) | O(n) | Range searches |

---

## 🎨 UI Features

### **Visual Indicators:**
- **DSA Badge:** Shows which algorithm is being used
- **Color-coded risk levels:**
  - 🔴 High Risk
  - 🟡 Medium Risk
  - 🟢 Low Risk
  - ⚪ Unknown

### **Statistics Dashboard:**
- Total patients count
- High/Medium/Low risk breakdown
- Real-time updates

### **Tabbed Interface:**
- Smart Filters
- Direct Search
- Sort & Order
- Advanced (BST)

---

## 🚀 How to Access

1. **Start the app:**
   ```bash
   streamlit run app.py
   ```

2. **Navigate to Search:**
   - Look in the sidebar
   - Click "🔍 Search"

3. **Try different algorithms:**
   - Each tab demonstrates a different DSA concept
   - Results show which algorithm was used
   - Performance is visualized

---

## 💡 Real-World Applications

### **Medical Triage:**
- Priority Queue sorts patients by urgency
- High-risk elderly patients seen first

### **Patient Lookup:**
- Binary Search for fast ID/MRN lookups
- Linear Search for flexible name matching

### **Reporting:**
- Merge Sort for alphabetical reports
- Age BST for demographic analysis

### **Queue Management:**
- FIFO for fair scheduling
- LIFO for recent cases

---

## 🎓 Learning Outcomes

Students/developers can learn:
1. **Practical DSA application** in healthcare
2. **Algorithm selection** based on use case
3. **Performance optimization** techniques
4. **Data structure trade-offs**
5. **Real-world problem solving**

---

## 📝 Code Structure

```
dsa/
├── linearsearch.py       # Linear & Binary Search
├── sorting.py            # Merge Sort
├── patient_dsa.py        # Priority Queue, FIFO, LIFO, BST, Filtering
├── bst.py                # Additional BST implementations
├── hashing.py            # Hash-based lookups
├── appointment_queue.py  # Queue for appointments
└── ...

frontend/
└── search_page.py        # UI for all DSA features
```

---

## 🔧 Technical Details

### **Dependencies:**
- Python's `heapq` for priority queue
- Standard library (no external DSA libraries)
- Streamlit for UI

### **Data Flow:**
```
Patient Database
    ↓
Convert to Python dicts
    ↓
Apply DSA algorithm
    ↓
Display results with badges
```

---

## ✅ Summary

The DSA folder is **now fully integrated** into the CancerCare project through the **Search page**, demonstrating:

- ✅ 8 different algorithms
- ✅ Real-world healthcare applications
- ✅ Interactive UI
- ✅ Educational value
- ✅ Production-ready code

**Try it now:** `streamlit run app.py` → Click "🔍 Search" 🚀
