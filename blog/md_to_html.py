"""把周报 md 渲染成自带图片(base64 内嵌)的单文件 HTML，方便复制进公众号/浏览器看。
用法: blog/.venv/bin/python md_to_html.py ../docs/本周AI必读-第1期-draft.md ../docs/本周AI必读-第1期.html
"""
import base64, re, sys, mimetypes
from pathlib import Path
import markdown

src = Path(sys.argv[1]).resolve()
out = Path(sys.argv[2]).resolve()
base = src.parent
raw = src.read_text(encoding="utf-8")

# 去掉给自己看的元信息行（状态/待办/角度/所有引用/标题已定）
keep = []
for ln in raw.splitlines():
    s = ln.lstrip("> ").strip()
    if ln.lstrip().startswith(">") and any(s.startswith(k) for k in
            ("角度:", "角度：", "状态:", "状态：", "所有引用", "待办", "标题已定")):
        continue
    keep.append(ln)
raw = "\n".join(keep)

# 图片相对路径 → base64 data URI
def inline(m):
    alt, rel = m.group(1), m.group(2)
    p = (base / rel)
    if not p.exists():
        return m.group(0)
    mime = mimetypes.guess_type(str(p))[0] or "image/png"
    b64 = base64.b64encode(p.read_bytes()).decode()
    return (f'<img src="data:{mime};base64,{b64}" alt="{alt}" '
            f'style="max-width:100%;border-radius:8px;margin:14px 0;display:block"/>')

raw = re.sub(r'!\[([^\]]*)\]\(([^)]+)\)', inline, raw)

body = markdown.markdown(raw, extensions=["extra"])
html = f"""<!doctype html><html lang=zh><head><meta charset=utf-8>
<meta name=viewport content="width=device-width,initial-scale=1">
<title>{src.stem}</title>
<style>
 body{{max-width:680px;margin:32px auto;padding:0 18px;color:#1f1f1f;line-height:1.85;
   font:17px/1.85 -apple-system,"PingFang SC","Helvetica Neue",sans-serif;background:#fff}}
 h1{{font-size:26px;line-height:1.4}} h2{{font-size:21px;margin-top:34px}}
 blockquote{{margin:14px 0;padding:10px 16px;border-left:3px solid #DD6B33;
   background:#FAF6F0;color:#5a5048}}
 img{{max-width:100%}} hr{{border:none;border-top:1px solid #eee;margin:28px 0}}
 strong{{color:#1f1f1f}}
</style></head><body>
{body}
</body></html>"""
out.write_text(html, encoding="utf-8")
print("OK ->", out)
