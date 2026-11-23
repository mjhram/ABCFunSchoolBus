import json

with open(r"C:\Users\hp2\.gemini\antigravity\brain\9c880cfa-c73a-4633-929f-9c2dbdfe7dfd\.system_generated\steps\189\output.txt", "r", encoding="utf-8") as f:
    models = json.load(f)

free_models = []
for m in models:
    pricing = m.get("pricing", {})
    cit = pricing.get("completionImageTokens", None)
    if cit == "0" or cit == 0:
        free_models.append(m.get("name"))

print("Free image models:", free_models)
