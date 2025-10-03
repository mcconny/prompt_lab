import json
from pathlib import Path
from datetime import datetime

ROOT = Path(__file__).resolve().parent
IN_PATH = ROOT / "input.json"
OUT_DIR = ROOT / "out"
OUT_DIR.mkdir(parents=True, exist_ok=True)
OUT_PATH = OUT_DIR / "tasks.json"

def load_input(path: Path) -> dict:
    if not path.exists():
        raise FileNotFoundError(f"Missing input file: {path}")
    with path.open("r", encoding="utf-8") as f:
        return json.load(f)

def generate_placeholder_tasks(data: dict) -> dict:
    """
    V0 stub: returns a fixed structure based on minimal input fields.
    No AI calls. Deterministic output for reproducibility.
    """
    circuit = data.get("circuit", "UNKNOWN")
    level = data.get("level", "B")
    n = int(data.get("num_tasks", 6))

    tasks = []
    for i in range(1, n + 1):
        tasks.append({
            "id": f"{circuit}-{level}-{i}",
            "type": "placeholder",
            "prompt": f"[V0] Create a task for {circuit} at level {level} (item {i}). No solutions.",
            "constraints": [
                "exactly one task per type (placeholder)",
                "no solutions",
                "units must be specified when applicable"
            ]
        })

    return {
        "meta": {
            "version": "v0",
            "generated_at": datetime.utcnow().isoformat(timespec="seconds") + "Z",
            "source": "apps/task-generator/main.py"
        },
        "input_echo": data,
        "tasks": tasks
    }

def write_output(path: Path, payload: dict) -> None:
    with path.open("w", encoding="utf-8") as f:
        json.dump(payload, f, indent=2, ensure_ascii=False)

def main():
    data = load_input(IN_PATH)
    payload = generate_placeholder_tasks(data)
    write_output(OUT_PATH, payload)
    print(f"OK -> {OUT_PATH.relative_to(ROOT)}")

if __name__ == "__main__":
    main()
