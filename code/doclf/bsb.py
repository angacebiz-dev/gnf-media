"""BSB fetch + check (Nov 19, 2026). python3 bsb.py jonah 1 2 3 4  -> bsb/jonah_<ch>.json {verse: text}
check(quote, ref): every '...'-separated piece of the quote must appear in order in the BSB verse text (quotes/apostrophes normalised)."""
import re, html, json, sys, os, urllib.request
D = os.path.join(os.path.dirname(os.path.abspath(__file__)), "bsb")
def fetch(book, ch):
    p = f"{D}/{book}_{ch}.json"
    if os.path.exists(p): return {int(k): v for k, v in json.load(open(p)).items()}
    s = urllib.request.urlopen(urllib.request.Request(f"https://biblehub.com/bsb/{book}/{ch}.htm", headers={"User-Agent": "Mozilla/5.0"}), timeout=30).read().decode("utf-8", "ignore")
    s = s[s.find('class="chap"'):]; s = s[:s.find('<div id="botbox"')] if '<div id="botbox"' in s else s
    s = re.sub(r'<p class="hdg">.*?(?=<p class="reg"|<p class="indent|<span class="reftext")', ' ', s, flags=re.S)
    s = re.sub(r'<span class="fn">.*?</span>', '', s, flags=re.S); s = re.sub(r'<sup.*?</sup>', '', s, flags=re.S)
    parts = re.split(r'<span class="reftext"><a href="[^"]*"><b>(\d+)</b></a></span>', s)
    out = {}
    for i in range(1, len(parts) - 1, 2):
        t = re.sub(r'<[^>]+>', ' ', parts[i + 1]); t = html.unescape(t); t = re.sub(r'\s+', ' ', t).strip()
        out[int(parts[i])] = t.split(" Footnotes:")[0].strip()
    json.dump(out, open(p, "w"), ensure_ascii=False, indent=0); return out
def norm(t): return re.sub(r"\s+", " ", t.replace("’", "'").replace("‘", "'").replace("“", '"').replace("”", '"')).strip()
BOOKS = {"Jonah": "jonah", "Genesis": "genesis", "Ezekiel": "ezekiel", "Job": "job", "Matthew": "matthew", "Luke": "luke", "Psalm": "psalms", "Exodus": "exodus", "Hebrews": "hebrews", "Mark": "mark", "John": "john", "Romans": "romans", "James": "james", "2 Peter": "2_peter", "1 Peter": "1_peter", "Isaiah": "isaiah", "2 Kings": "2_kings", "Nahum": "nahum", "Revelation": "revelation", "Ezra": "ezra"}
def verse_text(ref):
    m = re.match(r"^(\d? ?[A-Za-z]+) (\d+):(\d+)(?:-(\d+))?$", ref.strip())
    book, ch, v0, v1 = m.group(1), int(m.group(2)), int(m.group(3)), int(m.group(4) or m.group(3))
    vs = fetch(BOOKS[book], ch); return " ".join(vs[v] for v in range(v0, v1 + 1))
def check(quote, ref):
    full = norm(verse_text(ref)); q = norm(quote).strip('"')
    pos = 0
    for piece in [x.strip(' "') for x in re.split(r"\.\.\.|…", q) if x.strip(' ".,')]:
        piece = piece.strip(' "')
        j = full.find(piece, pos)
        if j < 0: return False, piece, full
        pos = j + len(piece)
    return True, "", full
if __name__ == "__main__":
    b = sys.argv[1]
    for c in sys.argv[2:]:
        v = fetch(b, int(c)); print(b, c, len(v), "verses")
