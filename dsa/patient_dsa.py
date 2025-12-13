# dsa/patient_dsa.py

from datetime import datetime
import heapq
from typing import List, Dict, Tuple, Set, Optional

# Mapping of risk string to numeric priority
RISK_PRIORITY = {
    "HIGH": 3,
    "MEDIUM": 2,
    "LOW": 1,
}


# ---------------- BASIC FILTERING ----------------

def filter_patients(
    patients: List[Dict],
    age_range: Tuple[int, int],
    allowed_risks: Set[str],
    name_query: str = "",
) -> List[Dict]:
    """
    Filter patients by:
      - age range
      - risk levels
      - name substring
    """
    min_age, max_age = age_range
    name_query = (name_query or "").lower().strip()
    allowed_risks = {r.upper() for r in allowed_risks}

    result: List[Dict] = []
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


# ---------------- PRIORITY QUEUE (TRIAGE) ----------------

def order_by_priority(patients: List[Dict]) -> List[Dict]:
    """
    High risk & older patients first using a max-heap.

    Priority:
      1) risk_level (HIGH > MEDIUM > LOW)
      2) age (older first)
      3) created_at (earlier first)
    """
    heap = []

    for p in patients:
        risk_str = str(p.get("risk_level", "LOW")).upper()
        risk_score = RISK_PRIORITY.get(risk_str, 1)
        age = int(p.get("age", 0))

        created_raw = p.get("created_at", "1970-01-01T00:00:00")
        try:
            created = datetime.fromisoformat(created_raw)
        except Exception:
            created = datetime(1970, 1, 1)

        # max-heap behaviour using negative values
        priority = (-risk_score, -age, created)
        heapq.heappush(heap, (priority, p))

    ordered: List[Dict] = []
    while heap:
        _, patient = heapq.heappop(heap)
        ordered.append(patient)

    return ordered


# ---------------- FIFO QUEUE (ARRIVAL ORDER) ----------------

def order_by_fifo(patients: List[Dict]) -> List[Dict]:
    """
    Normal worklist: first predicted, first seen.
    """
    return sorted(
        patients,
        key=lambda p: p.get("created_at", "1970-01-01T00:00:00")
    )


# ---------------- LIFO STACK (RECENTLY ADDED) ----------------

def order_by_lifo(patients: List[Dict]) -> List[Dict]:
    """
    Recently added / predicted patients on top.
    """
    return sorted(
        patients,
        key=lambda p: p.get("created_at", "1970-01-01T00:00:00"),
        reverse=True,
    )


# ---------------- HASH MAP INDEX (O(1) LOOKUP) ----------------

def build_id_index(patients: List[Dict]) -> Dict:
    """
    Build a dict: id -> patient
    for fast lookup by ID.
    """
    index: Dict = {}
    for p in patients:
        pid = p.get("id")
        if pid is not None:
            index[pid] = p
    return index


# ---------------- SIMPLE AGE BST (EXTRA DSA) ----------------

class AgeBSTNode:
    def __init__(self, age: int):
        self.age = age
        self.patients: List[Dict] = []
        self.left: Optional["AgeBSTNode"] = None
        self.right: Optional["AgeBSTNode"] = None


class AgeBST:
    def __init__(self):
        self.root: Optional[AgeBSTNode] = None

    def insert(self, patient: Dict):
        age = int(patient.get("age", 0))

        if self.root is None:
            self.root = AgeBSTNode(age)
            self.root.patients.append(patient)
            return

        node = self.root
        while True:
            if age == node.age:
                node.patients.append(patient)
                return
            elif age < node.age:
                if node.left is None:
                    node.left = AgeBSTNode(age)
                    node.left.patients.append(patient)
                    return
                node = node.left
            else:
                if node.right is None:
                    node.right = AgeBSTNode(age)
                    node.right.patients.append(patient)
                    return
                node = node.right

    def range_query(self, min_age: int, max_age: int) -> List[Dict]:
        """Return all patients with min_age <= age <= max_age."""
        result: List[Dict] = []

        def _dfs(node: Optional[AgeBSTNode]):
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

def build_age_bst(patients: List[Dict]) -> AgeBST:
    bst = AgeBST()
    for p in patients:
        bst.insert(p)
    return bst
