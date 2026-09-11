import sys
sys.stdout.reconfigure(encoding='utf-8')
from backend.ai_engine.myth_checker import check_myth

tests = [
    "is modi giving 50000 to all farmers?",
    "50000 farmers scheme",
    "free laptop registration link",
    "free 2 lakh insurance whatsapp",
    "modi laptop yojana",
    "8000 monthly pension scheme"
]

print("=" * 55)
print("MYTH CHECKER — FULL KEYWORD MATCH TEST")
print("=" * 55)
for q in tests:
    r = check_myth(q)
    status = "PASS" if r["verdict"] != "UNVERIFIED" else "CHECK"
    print(f"[{status}] Query  : {q}")
    print(f"       Verdict: {r['verdict']} | Scheme: {r['real_scheme']}")
    print()
