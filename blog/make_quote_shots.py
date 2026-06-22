"""批量：为每条金句抓「大佬说这句」的真实帧 + 烧字幕条 + 降噪角标 → 成品 PNG。
跑法：cd blog && .venv/bin/python make_quote_shots.py
依赖：grab_quote_frame.py（定位+下载+抽帧）、headless Chrome（合成字幕）。
"""
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
    dict(slug="ilya", key="moving from the age",
         locate="某种意义上我们又回到了研究时代，从规模化的时代进入研究的时代",
         zh="我们正从规模化的时代，<br>进入研究的时代。",
         name="Ilya Sutskever", role="OpenAI 联合创始人", score=93),
    dict(slug="feifei", key="Spatial Intelligence",
         locate="对我而言没有空间智能AGI就不完整，空间智能是通往AGI的关键",
         zh="没有空间智能，<br>AGI 就不完整。",
         name="李飞飞 Fei-Fei Li", role="斯坦福教授 · World Labs", score=91),
    dict(slug="karpathy", key="Deep Dive into LLMs",
         locate="预训练是对互联网的有损压缩，我们得到的是互联网的幽灵",
         zh="我们得到的，<br>是互联网的幽灵。",
         name="Andrej Karpathy", role="OpenAI 创始成员", score=90),
    dict(slug="hinton", key="Godfather of AI",
         locate="就像养了一只很可爱的老虎幼崽，除非你能确定它长大后不会想杀你",
         zh="就像养了一只很可爱的老虎幼崽。<br>除非确定它长大后不会想杀你。",
         name="Geoffrey Hinton", role="诺奖得主 · AI 教父", score=95),
    dict(slug="lecun", key="LeCun",
         locate="我们永远不会仅靠在文本上训练就达到人类级别的人工智能",
         zh="永远不会仅靠文本训练，<br>达到人类级别的 AI。",
         name="Yann LeCun", role="图灵奖得主 · Meta", score=88),
    dict(slug="jensen", key="Jensen",
         locate="推理就是思考，思考比阅读难得多",
         zh="推理就是思考，<br>思考比阅读难得多。",
         name="黄仁勋 Jensen Huang", role="英伟达 CEO", score=90),
    dict(slug="block", key="Owen Jennings",
         locate="公司人数和产出之间的相关性在十二月第一周被打破了",
         zh="人数与产出的相关性，<br>在 12 月第一周被打破了。",
         name="Owen Jennings", role="Block（原 Square）", score=88),
]


def find(key):
    for mp in glob.glob(str(ROOT / "archive" / "*" / "metadata.json")):
        m = json.load(open(mp, encoding="utf-8"))
        t = (m.get("title") or "") + (m.get("chinese_title") or "")
        if key.lower() in t.lower():
            return os.path.dirname(mp), m.get("url")
    return None, None


def overlay_html(img, zh, name, role, score):
    verdict = "必读" if score >= 90 else "强烈推荐"
    return f"""<!doctype html><meta charset=utf-8><style>
html,body{{margin:0}}
.stage{{width:1280px;height:720px;position:relative;overflow:hidden;background:#000 url('file://{img}') center/cover no-repeat;font-family:"PingFang SC","Helvetica Neue",sans-serif}}
.tag{{position:absolute;top:30px;left:30px;display:flex;align-items:center;gap:12px;background:rgba(0,0,0,.42);padding:9px 18px 9px 11px;border-radius:999px}}
.chip{{width:38px;height:38px;border-radius:10px;background:#DD6B33;color:#fff;font-family:"Songti SC",serif;font-weight:700;font-size:24px;display:flex;align-items:center;justify-content:center}}
.tt{{color:#fff;font-size:22px;letter-spacing:1px}}
.cap{{position:absolute;left:0;right:0;bottom:0;padding:150px 70px 58px;background:linear-gradient(180deg,transparent,rgba(0,0,0,.22) 36%,rgba(0,0,0,.92))}}
.q{{color:#fff;font-size:60px;font-weight:600;line-height:1.3;text-shadow:0 2px 14px rgba(0,0,0,.65)}}
.by{{display:flex;align-items:center;justify-content:space-between;margin-top:28px}}
.nm{{color:#EBE3D7;font-size:30px}}
.nm b{{color:#fff;font-weight:600}}
.pill{{background:#DD6B33;color:#fff;font-size:25px;font-weight:600;padding:8px 22px;border-radius:999px;white-space:nowrap}}
</style>
<div class=stage>
  <div class=tag><span class=chip>降</span><span class=tt>降噪 · 本周 AI 必读 #1</span></div>
  <div class=cap>
    <div class=q>「{zh}」</div>
    <div class=by><span class=nm>— <b>{name}</b> · {role}</span><span class=pill>评分 {score} · {verdict}</span></div>
  </div>
</div>"""


def main():
    done = []
    for it in ITEMS:
        d, url = find(it["key"])
        if not d:
            print("SKIP", it["slug"], "未找到"); continue
        raw = IMG / f"raw-{it['slug']}.png"
        if not raw.exists():
            r = subprocess.run(
                [PYBLOG, "grab_quote_frame.py", "--dir", d, "--url", url,
                 "--quote", it["locate"], "--out", str(raw)],
                cwd=str(ROOT / "blog"), capture_output=True, text=True)
            print(f"[{it['slug']}] grab:", (r.stdout or "").strip().splitlines()[-1:] or r.stderr[-150:])
        if not raw.exists():
            print("FRAME FAIL", it["slug"]); continue
        hp = CARDS / f"shot-{it['slug']}.html"
        hp.write_text(overlay_html(str(raw), it["zh"], it["name"], it["role"], it["score"]),
                      encoding="utf-8")
        out = IMG / f"shot-{it['slug']}.png"
        subprocess.run(
            [CHROME, "--headless=new", "--disable-gpu", "--hide-scrollbars",
             "--force-device-scale-factor=1", "--window-size=1280,720",
             "--virtual-time-budget=2500", f"--screenshot={out}", f"file://{hp}"],
            capture_output=True, text=True)
        ok = out.exists()
        print(("OK  " if ok else "RENDER FAIL ") + it["slug"], "->", out.name)
        if ok:
            done.append(it["slug"])
    print("\n完成:", done)


if __name__ == "__main__":
    main()
