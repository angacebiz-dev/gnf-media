# Documentary long-form pipeline (Nov 19, 2026 — Jonah, Noah, Ezekiel, Job)
1. `python3 bsb.py <book> <ch>...` caches BSB text; `bsb.check(quote, ref)` verifies every quoted verse word for word.
2. `python3 doc_fetch.py <dir> aic:name=id cma:name=id met:name=id` → public-domain / CC0 museum images (+ meta.json for labels).
3. `python3 doc_crop.py <dir> key=auto|x0,y0,x1,y1|keep` (and `blake_crop.py` for Blake's Job plates) → `<dir>/p/`.
4. `<dir>/script.md`: `## Section` headings, plain lines = narration beats, `"verse" — Ref` = verse cards, `@key fx,fy` = image for the following beats.
5. `python3 doc_voice.py <dir>` (Kokoro am_michael) → voice.wav + beats.json.
6. `<dir>/conf.json` (hook title, next card, labels, gold words); `DOC=<dir> python3 doc_story.py --frames t1,t2` to check stills, then `--chunk 0 2` and `--chunk 1 2`.
7. `bash longform_finish.sh <dir> <name>_master.mp4 <seed>` (piano bed, -15 LUFS) → `enc95.sh` (two-pass, under 95 MB) → `doc_thumb.py` (3 thumbnails) → `post_lf.sh` (push + verify raw URLs) → schedule in Metricool.
