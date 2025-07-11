import difflib

def get_metrics(answer):
    return {
        "Length": len(answer.split()),
        "Chars": len(answer),
    }

def get_similarity(a, b):
    return difflib.SequenceMatcher(None, a, b).ratio()

def get_diff_html(a, b):
    diff = difflib.ndiff(a.split(), b.split())
    html = "<div style='font-family:monospace; line-height:1.8;'>"
    for word in diff:
        if word.startswith("- "):
            html += f"<span style='background:#ffcccc; padding:2px 4px; border-radius:4px;'>{word[2:]} </span>"
        elif word.startswith("+ "):
            html += f"<span style='background:#ccffcc; padding:2px 4px; border-radius:4px;'>{word[2:]} </span>"
        elif word.startswith("? "):
            continue
        else:
            html += f"{word[2:]} "
    html += "</div>"
    return html
