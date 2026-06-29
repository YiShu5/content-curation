"""为指定的两句金句各做一张「人物画面 + 烧字幕」图（无品牌标志）。"""
import glob, json, os, subprocess
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
IMG = ROOT / "docs" / "images"
CARDS = ROOT / "docs" / "cards"
CHROME = "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome"
PYBLOG = str(ROOT / "blog" / ".venv" / "bin" / "python")
IMG.mkdir(parents=True, exist_ok=True)
CARDS.mkdir(parents=True, exist_ok=True)

ITEMS = [
    dict(slug="q-langchain", key="Memory for agents",
         locate="we are not bullish on a general-purpose memory abstraction or memory as a service for agents",
         zh="我们并不看好<br>通用记忆抽象或服务的想法", attr="— LangChain 团队"),
    dict(slug="q-letta", key="Letta:",
         locate="agents have a much longer lifespan than models; memory and context are more valuable than the model itself",
         zh="代理的寿命比模型的寿命更长。<br>记忆和上下文比模型本身更有价值。", attr="— Charles · Letta 联合创始人"),
]


def find(key):
    for mp in glob.glob(str(ROOT / "archive" / "*" / "metadata.json")):
        m = json.load(open(mp, encoding="utf-8"))
        t = (m.get("title") or "") + (m.get("chinese_title") or "")
        if key.lower() in t.lower():
            return os.path.dirname(mp), m.get("url")
    return None, None


def overlay(img, zh, attr):
    return f"""<!doctype html><meta charset=utf-8><style>
html,body{{margin:0}}
.stage{{width:1280px;height:720px;position:relative;overflow:hidden;background:#000 url('file://{img}') center/cover no-repeat;font-family:"PingFang SC","Helvetica Neue",sans-serif}}
.cap{{position:absolute;left:0;right:0;bottom:0;padding:150px 70px 58px;background:linear-gradient(180deg,transparent,rgba(0,0,0,.22) 36%,rgba(0,0,0,.92))}}
.q{{color:#fff;font-size:58px;font-weight:600;line-height:1.32;text-shadow:0 2px 14px rgba(0,0,0,.65)}}
.by{{color:#EBE3D7;font-size:30px;margin-top:26px}}
</style><div class=stage><div class=cap><div class=q>「{zh}」</div><div class=by>{attr}</div></div></div>"""


for it in ITEMS:
    d, url = find(it["key"])
    if not d:
        print("SKIP", it["slug"], "未找到 key=", it["key"]); continue
    raw = IMG / f"raw-{it['slug']}.png"
    r = subprocess.run([PYBLOG, "grab_quote_frame.py", "--dir", d, "--url", url,
                        "--quote", it["locate"], "--out", str(raw)],
                       cwd=str(ROOT / "blog"), capture_output=True, text=True)
    for ln in (r.stdout or "").strip().splitlines():
        if "定位" in ln or "OK ->" in ln or "FAIL" in ln:
            print(f"[{it['slug']}]", ln)
    if not raw.exists():
        print("FRAME FAIL", it["slug"], (r.stderr or "")[-150:]); continue
    hp = CARDS / f"shot-{it['slug']}.html"
    hp.write_text(overlay(str(raw), it["zh"], it["attr"]), encoding="utf-8")
    out = IMG / f"shot-{it['slug']}.png"
    subprocess.run([CHROME, "--headless=new", "--disable-gpu", "--hide-scrollbars",
                    "--force-device-scale-factor=1", "--window-size=1280,720",
                    "--virtual-time-budget=2500", f"--screenshot={out}", f"file://{hp}"],
                   capture_output=True, text=True)
    print(("OK   " if out.exists() else "RENDER FAIL ") + it["slug"])
print("done")
