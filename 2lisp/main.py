import sys
import os
import json
import yaml
import re

def to_sexpr(data, tag="yaml"):
    if isinstance(data, dict):
        return "(" + " ".join(f"({tag}:{key} {to_sexpr(value, tag)})" for key, value in data.items()) + ")"
    elif isinstance(data, list):
        if all(isinstance(i, dict) and 'part_no' in i for i in data):
            return "(" + " ".join(f"({tag}:item {to_sexpr(item, tag)})" for item in data) + ")"
        else:
            return "(" + " ".join(to_sexpr(item, tag) for item in data) + ")"
    elif isinstance(data, str):
        if re.match(r"^\d{4}-\d{2}-\d{2}$", data):
            y, m, d = map(int, data.split("-"))
            return f"(make-date {y} {m} {d})"
        return f"\"{data.replace('\"', '\\\"')}\""
    elif isinstance(data, (int, float)):
        return str(data)
    elif isinstance(data, bool):
        return "true" if data else "false"
    elif data is None:
        return "nil"
    else:
        return f"\"{str(data)}\""

def main():
    if len(sys.argv) != 2:
        print("Usage: yaml2lisp <input.yaml|json>")
        sys.exit(1)

    input_file = sys.argv[1]

    if not os.path.isfile(input_file):
        print(f"Error: file not found — {input_file}")
        sys.exit(1)

    try:
        with open(input_file, 'r', encoding='utf-8') as f:
            if input_file.endswith(".json"):
                data = json.load(f)
            else:
                data = yaml.safe_load(f)

        result = to_sexpr(data)
        
        with open("output.lisp", "w", encoding='utf-8') as out:
            out.write(result + "\n")

        print("S-expression written to output.lisp")

    except Exception as e:
        print(f"Error: {e}")
        sys.exit(1)
