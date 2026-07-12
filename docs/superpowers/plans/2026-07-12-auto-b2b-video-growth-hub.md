# 汽车 B 端视频增长中台 MVP Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** 在现有 NoiseFilter Flask 站点中交付一个单抖音账号的 B 端视频增长中台：导入自有账号数据、生成可解释的内容复盘、从上传视频生成一条模板化短视频，并经网易邮箱人工确认后发送给客户。

**Architecture:** 保持 `archive/` 为内容真相源，新增一个仅存放本地运行状态的 `blog/data/growth/` JSON 存储层，而不是引入数据库。抖音第一版采用创作者后台 CSV 导入，设计稳定的适配接口为后续官方授权同步预留入口；视频处理以 Python 任务状态机协调 FFmpeg 与 Remotion，邮件由独立 SMTP 服务执行，所有外发必须经过页面人工确认。

**Tech Stack:** Python 3 / Flask 3 / Jinja2 / 标准库 `csv`、`json`、`smtplib`、`subprocess`，FFmpeg，Node.js / Remotion，现有 `requests` 与 OpenAI-compatible API，现有脚本式 Python 测试。

## Global Constraints

- 仅支持一个抖音账号；不实现多账号、门店矩阵、权限体系或抖音自动发布。
- `archive/` 继续是现有内容库的真相源；`blog/data/` 是忽略的本地运行数据，不能提交。
- Flask 继续使用 `blog/.venv` 并运行在 5055 端口。
- 所有密钥仅在 `config/.env` 中读取；不得提交网易授权码、抖音密钥、API Key、客户邮箱或运行时 JSON。
- 抖音数据主路径是用户导出的自有账号 CSV；官方授权同步只在拿到已审批的应用凭据后启用。
- 不以非官方抓取器作为生产数据的唯一来源；粘贴视频链接只创建素材记录，不宣称获得后台指标。
- AI 只能提供“当前样本趋势”；样本少于 10 条时必须展示 `样本不足，仅供参考`，不得输出确定性增长承诺。
- 粗剪仅支持一个连续片段、30–60 秒、9:16、固定品牌模板；每次最多三个候选片段。
- 正式视频只在用户确认候选片段后渲染；预览和正式渲染都必须保留任务状态与失败原因。
- 邮件为一对一 B 端跟进；发送前必须由用户编辑或确认，禁止自动群发、打开像素与隐蔽追踪。
- 视频附件超过 `NETEASE_MAX_ATTACHMENT_BYTES` 时只发送受控下载链接，不尝试绕过邮件附件限制。
- 沿用项目的可执行脚本测试风格：每个新 `blog/test_*.py` 可由 `blog/.venv/bin/python` 直接运行。
- 工作区已有用户拥有的未跟踪 `.superpowers/` 与 `AGENTS.md`；不暂存、删除、移动或提交它们。

---

## File Structure

### New files

- `blog/growth_store.py` — 原子 JSON 存储、单账号资料、视频、指标快照、客户、邮件和视频任务的 CRUD。
- `blog/test_growth_store.py` — 存储层原子写入、去重、状态约束测试。
- `blog/douyin_import.py` — 创作者后台 CSV 标题映射、行校验与指标标准化。
- `blog/test_douyin_import.py` — 中文/英文标题、缺列、重复视频和非法数值测试。
- `blog/growth_insights.py` — 指标计算、样本置信度、确定性复盘和下一条选题草案。
- `blog/test_growth_insights.py` — 点赞率、快照增速、样本不足和排序测试。
- `blog/growth_ai.py` — 以确定性草案为基础的 OpenAI-compatible 文案润色；API 失败时无损降级。
- `blog/test_growth_ai.py` — 模型响应解析与降级测试。
- `blog/video_jobs.py` — 上传文件校验、短视频任务状态机、后台 worker 启动。
- `blog/video_worker.py` — 转录、候选片段、FFmpeg 粗剪、Remotion 渲染的任务执行器。
- `blog/test_video_jobs.py` — 状态转换、候选确认、二进制失败消息测试。
- `blog/test_video_worker.py` — 模拟 subprocess 的裁切/渲染顺序测试。
- `blog/mail_service.py` — 网易 SMTP 配置校验、邮件组成和发送。
- `blog/test_mail_service.py` — SMTP 成功、鉴权错误、附件阈值与确认前禁止发送测试。
- `blog/templates/growth/index.html` — 中台首页：今日总览、视频表现、AI 结论、待处理任务。
- `blog/templates/growth/video_detail.html` — 单视频复盘与“发给客户”入口。
- `blog/templates/growth/workshop.html` — 上传、粗剪候选、渲染状态与成片预览。
- `blog/templates/growth/customer_send.html` — 客户表单、可编辑邮件、发送确认与历史记录。
- `blog/templates/growth/settings.html` — 单账号、CSV 导入、品牌模板、SMTP 连接状态。
- `blog/templates/growth/_metric_card.html` — 统一指标卡。
- `blog/templates/growth/_video_row.html` — 统一视频表格行。
- `blog/static/css/growth.css` — 仅以 `.growth-*` 为前缀的中台样式。
- `blog/static/js/growth.js` — CSV 提交、任务轮询与发送前确认。
- `blog/test_growth_routes.py` — 中台读写路由、文件上传、确认发送和错误展示测试。
- `scripts/render-short-video.mjs` — Remotion 模板渲染入口，读取已验证的 job JSON。
- `video_templates/short-video/src/Root.jsx` — Remotion 根组合。
- `video_templates/short-video/src/ShortVideo.jsx` — 9:16 字幕、Logo 与标题模板。
- `video_templates/short-video/package.json` — 独立 Remotion 运行依赖和 render 脚本。
- `README-growth-hub.md` — 客户交付运行说明、CSV 格式、授权码设置与人工操作流程。

### Modified files

- `blog/config.py` — 增长中台数据目录、上传阈值、OpenAI-compatible、网易 SMTP 与抖音配置的环境变量读取。
- `blog/app.py` — `/growth` 路由、上传/导入/任务/API/邮件确认端点；保留现有首页、内容库与 `/ingest` 行为。
- `blog/templates/base.html` — 可选导航入口和 `extra_head`/`extra_scripts` 块，不改变已有内容库布局。
- `blog/requirements.txt` — 不增加新依赖；使用现有 Flask、requests、python-dotenv。
- `package.json` — 增加根级别 `video:render` 转发脚本，不把 Remotion 依赖混入现有改写脚本依赖。
- `run.sh` — 增加 `growth-worker <job_id>` 与 `growth-check` 两个安全的本地运维入口。
- `README.md` — 增加“汽车 B 端视频增长中台”链接和非生产性说明。

---

## Task 1: 建立本地增长数据存储与配置边界

**Files:**
- Create: `blog/growth_store.py`
- Create: `blog/test_growth_store.py`
- Modify: `blog/config.py`

**Interfaces:**
- Consumes: `Config.GROWTH_DATA_DIR: str`。
- Produces:
  - `GrowthStore(root: Path)`
  - `GrowthStore.get_account() -> dict`
  - `GrowthStore.save_account(account: dict) -> dict`
  - `GrowthStore.upsert_video(video: dict) -> dict`
  - `GrowthStore.append_snapshot(video_id: str, snapshot: dict) -> dict`
  - `GrowthStore.list_videos() -> list[dict]`
  - `GrowthStore.upsert_customer(customer: dict) -> dict`
  - `GrowthStore.record_mail(record: dict) -> dict`
  - `GrowthStore.create_video_job(job: dict) -> dict`
  - `GrowthStore.update_video_job(job_id: str, **patch: object) -> dict`

- [ ] **Step 1: 写出存储层失败测试**

创建 `blog/test_growth_store.py`：

```python
"""Growth hub local store tests.

Run: blog/.venv/bin/python blog/test_growth_store.py
"""

from pathlib import Path
from tempfile import TemporaryDirectory

from growth_store import GrowthStore


def test_video_upsert_and_metrics_snapshot_are_deduplicated():
    with TemporaryDirectory() as tmp:
        store = GrowthStore(Path(tmp))
        store.upsert_video({"video_id": "dy-1", "title": "电池怎么选", "published_at": "2026-07-01"})
        store.append_snapshot("dy-1", {"captured_at": "2026-07-02", "views": 100, "likes": 8})
        store.append_snapshot("dy-1", {"captured_at": "2026-07-02", "views": 120, "likes": 10})
        video = store.list_videos()[0]
    assert video["video_id"] == "dy-1"
    assert video["snapshots"] == [{"captured_at": "2026-07-02", "views": 120, "likes": 10}]
    print("✓ growth snapshots deduplicate by capture date")


def test_mail_record_requires_confirmed_status():
    with TemporaryDirectory() as tmp:
        store = GrowthStore(Path(tmp))
        try:
            store.record_mail({"mail_id": "mail-1", "status": "draft"})
        except ValueError as exc:
            assert "confirmed" in str(exc)
        else:
            raise AssertionError("unconfirmed mail record was accepted")
    print("✓ unconfirmed mail cannot become a send record")


if __name__ == "__main__":
    test_video_upsert_and_metrics_snapshot_are_deduplicated()
    test_mail_record_requires_confirmed_status()
    print("\\n全部通过 ✅")
```

- [ ] **Step 2: 运行测试，确认失败**

Run: `blog/.venv/bin/python blog/test_growth_store.py`
Expected: `ModuleNotFoundError: No module named 'growth_store'`.

- [ ] **Step 3: 实现原子 JSON store 与配置**

创建 `blog/growth_store.py`，采用临时文件后 `replace()` 的写入方式；所有公开 record 都补足 ISO 时间与稳定 ID：

```python
import json
import time
from pathlib import Path


class GrowthStore:
    def __init__(self, root: Path):
        self.root = Path(root)
        self.path = self.root / "growth_state.json"

    def _load(self):
        if not self.path.exists():
            return {"account": {}, "videos": {}, "customers": {}, "mails": {}, "video_jobs": {}}
        return json.loads(self.path.read_text(encoding="utf-8"))

    def _save(self, state):
        self.root.mkdir(parents=True, exist_ok=True)
        temp = self.path.with_suffix(".tmp")
        temp.write_text(json.dumps(state, ensure_ascii=False, indent=2), encoding="utf-8")
        temp.replace(self.path)

    def upsert_video(self, video):
        video_id = str(video.get("video_id") or "").strip()
        if not video_id:
            raise ValueError("video_id is required")
        state = self._load()
        current = dict(state["videos"].get(video_id) or {"video_id": video_id, "snapshots": []})
        current.update({k: v for k, v in video.items() if k != "snapshots"})
        state["videos"][video_id] = current
        self._save(state)
        return current

    def append_snapshot(self, video_id, snapshot):
        captured_at = str(snapshot.get("captured_at") or "").strip()
        if not captured_at:
            raise ValueError("captured_at is required")
        state = self._load()
        video = state["videos"].get(video_id)
        if not video:
            raise KeyError(video_id)
        snapshots = [item for item in video.get("snapshots", []) if item.get("captured_at") != captured_at]
        snapshots.append(dict(snapshot))
        video["snapshots"] = sorted(snapshots, key=lambda item: item["captured_at"])
        self._save(state)
        return video
```

补全 `get_account`、`save_account`、`list_videos`、`upsert_customer`、`record_mail`、`create_video_job`、`update_video_job`。`record_mail` 必须拒绝 `status != "confirmed"`，并将成功写入的状态固定为 `sent` 或 `failed`。在 `blog/config.py` 添加：

```python
GROWTH_DATA_DIR = os.getenv("GROWTH_DATA_DIR", os.path.join(os.path.dirname(__file__), "data", "growth"))
GROWTH_UPLOAD_MAX_BYTES = int(os.getenv("GROWTH_UPLOAD_MAX_BYTES", str(1024 * 1024 * 1024)))
NETEASE_SMTP_HOST = os.getenv("NETEASE_SMTP_HOST", "smtp.163.com")
NETEASE_SMTP_PORT = int(os.getenv("NETEASE_SMTP_PORT", "465"))
NETEASE_SMTP_USER = os.getenv("NETEASE_SMTP_USER", "")
NETEASE_SMTP_AUTH_CODE = os.getenv("NETEASE_SMTP_AUTH_CODE", "")
NETEASE_MAX_ATTACHMENT_BYTES = int(os.getenv("NETEASE_MAX_ATTACHMENT_BYTES", str(18 * 1024 * 1024)))
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY", "")
OPENAI_BASE_URL = os.getenv("OPENAI_BASE_URL", "https://api.openai.com/v1")
OPENAI_MODEL = os.getenv("OPENAI_MODEL", "gpt-4.1-mini")
```

- [ ] **Step 4: 运行存储测试**

Run: `blog/.venv/bin/python blog/test_growth_store.py`
Expected: both checks print `✓` and final output contains `全部通过 ✅`.

- [ ] **Step 5: Commit**

```bash
git add blog/config.py blog/growth_store.py blog/test_growth_store.py
git commit -m "feat: add local growth hub store"
```

## Task 2: 导入抖音自有账号 CSV 并生成可解释复盘

**Files:**
- Create: `blog/douyin_import.py`
- Create: `blog/test_douyin_import.py`
- Create: `blog/growth_insights.py`
- Create: `blog/test_growth_insights.py`
- Create: `blog/growth_ai.py`
- Create: `blog/test_growth_ai.py`

**Interfaces:**
- Consumes: UTF-8 / UTF-8-SIG CSV 文件、`GrowthStore` 的 `upsert_video`/`append_snapshot`。
- Produces:
  - `parse_douyin_csv(text: str, captured_at: str) -> list[dict]`
  - `import_rows(store: GrowthStore, rows: list[dict]) -> dict`
  - `build_insight_report(videos: list[dict]) -> dict`
  - `refine_report(report: dict, request_fn: Callable) -> dict`

- [ ] **Step 1: 写 CSV 和洞察的失败测试**

创建 `blog/test_douyin_import.py`：

```python
from douyin_import import parse_douyin_csv


def test_parse_chinese_creator_export():
    text = "作品ID,作品标题,发布时间,播放量,点赞数,评论数,分享数\\nabc,电池怎么选,2026-07-01,1200,96,12,6\\n"
    rows = parse_douyin_csv(text, "2026-07-08")
    assert rows == [{"video_id": "abc", "title": "电池怎么选", "published_at": "2026-07-01", "views": 1200, "likes": 96, "comments": 12, "shares": 6, "captured_at": "2026-07-08"}]
    print("✓ Chinese Douyin export parses")


def test_parse_rejects_rows_without_id_or_title():
    rows = parse_douyin_csv("作品ID,作品标题,播放量\\n,,100\\n", "2026-07-08")
    assert rows == []
    print("✓ invalid export row is skipped")


if __name__ == "__main__":
    test_parse_chinese_creator_export()
    test_parse_rejects_rows_without_id_or_title()
    print("\\n全部通过 ✅")
```

创建 `blog/test_growth_insights.py`：

```python
from growth_insights import build_insight_report


def test_small_sample_is_explicitly_not_confident():
    report = build_insight_report([{"video_id": "1", "title": "电池", "snapshots": [{"captured_at": "2026-07-01", "views": 100, "likes": 10}]}])
    assert report["confidence"] == "insufficient"
    assert "样本不足" in report["notice"]
    print("✓ small sample carries an explicit notice")


def test_report_ranks_like_rate_not_only_views():
    videos = [
        {"video_id": "a", "title": "车型介绍", "snapshots": [{"captured_at": "2026-07-01", "views": 1000, "likes": 20}]},
        {"video_id": "b", "title": "电池避坑", "snapshots": [{"captured_at": "2026-07-01", "views": 300, "likes": 30}]},
    ] * 5
    report = build_insight_report(videos)
    assert report["top_videos"][0]["video_id"] == "b"
    print("✓ report prioritizes engagement rate")


if __name__ == "__main__":
    test_small_sample_is_explicitly_not_confident()
    test_report_ranks_like_rate_not_only_views()
    print("\\n全部通过 ✅")
```

- [ ] **Step 2: 运行测试，确认缺失模块失败**

Run: `blog/.venv/bin/python blog/test_douyin_import.py && blog/.venv/bin/python blog/test_growth_insights.py`
Expected: first run fails with `ModuleNotFoundError` for `douyin_import`.

- [ ] **Step 3: 实现导入、确定性洞察和 AI 降级**

在 `blog/douyin_import.py` 固定支持下列列名别名：`作品ID/item_id/video_id`、`作品标题/标题/title`、`发布时间/published_at`、`播放量/播放次数/views`、`点赞数/likes`、`评论数/comments`、`分享数/shares`、`收藏数/favorites`。数值通过以下函数标准化，空值为 0，负数拒绝该行：

```python
def as_nonnegative_int(value):
    raw = str(value or "").replace(",", "").strip()
    if not raw:
        return 0
    number = int(float(raw))
    if number < 0:
        raise ValueError("metric cannot be negative")
    return number
```

在 `blog/growth_insights.py` 使用最后一个快照计算比率，使用最早与最新快照计算增长；报告结构固定为：

```python
{
    "sample_size": 12,
    "confidence": "current_trend",
    "notice": "基于 12 条视频的当前趋势，不构成播放量承诺。",
    "top_videos": [{"video_id": "...", "like_rate": 0.08, "comment_rate": 0.01, "growth_7d": 120}],
    "insights": ["..."],
    "next_video": {"title": "...", "opening": "...", "duration_seconds": 45, "customer_type": "企业采购方"},
}
```

`sample_size < 10` 时固定返回 `confidence="insufficient"` 与 `notice="样本不足，仅供参考；继续积累至少 10 条视频后再比较趋势。"`。`growth_ai.refine_report` 只能润色 `insights` 和 `next_video`，必须在请求失败、空响应或非 JSON 响应时原样返回确定性报告：

```python
def refine_report(report, request_fn):
    try:
        response = request_fn(report)
        candidate = response.get("report") if isinstance(response, dict) else None
        if not isinstance(candidate, dict):
            return report
        return {**report, "insights": candidate.get("insights", report["insights"]), "next_video": candidate.get("next_video", report["next_video"])}
    except Exception:
        return report
```

- [ ] **Step 4: 运行导入、洞察和 AI 测试**

Run: `blog/.venv/bin/python blog/test_douyin_import.py && blog/.venv/bin/python blog/test_growth_insights.py && blog/.venv/bin/python blog/test_growth_ai.py`
Expected: all scripts print `全部通过 ✅`.

- [ ] **Step 5: Commit**

```bash
git add blog/douyin_import.py blog/test_douyin_import.py blog/growth_insights.py blog/test_growth_insights.py blog/growth_ai.py blog/test_growth_ai.py
git commit -m "feat: import Douyin metrics and generate insights"
```

## Task 3: 增加安全的短视频任务队列与 Remotion 模板

**Files:**
- Create: `blog/video_jobs.py`
- Create: `blog/video_worker.py`
- Create: `blog/test_video_jobs.py`
- Create: `blog/test_video_worker.py`
- Create: `scripts/render-short-video.mjs`
- Create: `video_templates/short-video/package.json`
- Create: `video_templates/short-video/src/Root.jsx`
- Create: `video_templates/short-video/src/ShortVideo.jsx`
- Modify: `run.sh`
- Modify: `package.json`

**Interfaces:**
- Consumes: `GrowthStore`、上传的 `.mp4/.mov/.m4v`、FFmpeg 可执行文件、`video_templates/short-video` 的 Node 安装。
- Produces:
  - `create_upload_job(store, filename: str, content: bytes) -> dict`
  - `suggest_clips(transcript: list[dict]) -> list[dict]`
  - `confirm_clip(store, job_id: str, clip_id: str) -> dict`
  - `run_job(job_id: str, runner=subprocess.run) -> dict`

- [ ] **Step 1: 写任务状态和二进制调用的失败测试**

创建 `blog/test_video_jobs.py`：

```python
from pathlib import Path
from tempfile import TemporaryDirectory

from growth_store import GrowthStore
from video_jobs import create_upload_job, confirm_clip


def test_job_has_only_three_continuous_clip_candidates():
    with TemporaryDirectory() as tmp:
        store = GrowthStore(Path(tmp))
        job = create_upload_job(store, "老板讲电池.mp4", b"video-bytes")
        assert job["status"] == "queued"
        assert len(job["clip_candidates"]) <= 3
        assert all(item["end_seconds"] - item["start_seconds"] <= 60 for item in job["clip_candidates"])
    print("✓ clip job starts with bounded candidates")


def test_confirming_unknown_clip_is_rejected():
    with TemporaryDirectory() as tmp:
        store = GrowthStore(Path(tmp))
        job = create_upload_job(store, "老板讲电池.mp4", b"video-bytes")
        try:
            confirm_clip(store, job["job_id"], "not-a-candidate")
        except ValueError:
            pass
        else:
            raise AssertionError("unknown clip was confirmed")
    print("✓ only an offered clip can render")


if __name__ == "__main__":
    test_job_has_only_three_continuous_clip_candidates()
    test_confirming_unknown_clip_is_rejected()
    print("\\n全部通过 ✅")
```

- [ ] **Step 2: 运行失败测试**

Run: `blog/.venv/bin/python blog/test_video_jobs.py`
Expected: `ModuleNotFoundError: No module named 'video_jobs'`.

- [ ] **Step 3: 实现任务状态机与 worker**

`video_jobs.py` 只允许下列状态转换：

```python
VALID_TRANSITIONS = {
    "queued": {"analyzing", "failed"},
    "analyzing": {"awaiting_confirmation", "failed"},
    "awaiting_confirmation": {"rendering", "failed"},
    "rendering": {"done", "failed"},
    "done": set(),
    "failed": set(),
}
```

上传后保存到 `Config.GROWTH_DATA_DIR/uploads/<job_id>.mp4`，文件名只用 UUID，不使用用户提交的文件名作为路径。初版候选可基于已转录的连续语句；无转录时生成三个固定安全候选（`0–30`、`30–60`、`60–90`，视频不足时裁至时长），所有候选必须写明 `clip_id`、`start_seconds`、`end_seconds`、`title`、`customer_type`。

`video_worker.py` 必须先运行 FFprobe 取得时长，再运行下列安全的 FFmpeg 命令列表，不能使用 `shell=True`：

```python
cut_cmd = [
    "ffmpeg", "-y", "-ss", str(start), "-i", str(source), "-t", str(duration),
    "-vf", "scale=720:1280:force_original_aspect_ratio=increase,crop=720:1280",
    "-c:v", "libx264", "-preset", "veryfast", "-c:a", "aac", str(cut_path),
]
render_cmd = [
    "npm", "run", "render", "--prefix", str(template_root), "--", str(job_json), str(output_path),
]
```

任何 `returncode != 0` 必须将最后 500 个字符写入 job 的 `error_message`，并转为 `failed`；成功时只暴露 `/growth/video-output/<job_id>` 路径，不暴露原始磁盘路径。

`video_templates/short-video/src/ShortVideo.jsx` 使用固定 `1080x1920` Composition，输入字段只有 `videoSrc`、`captionLines`、`title`、`logoText`；不接受任意 JSX、HTML 或外部 URL。字幕渲染为白色大字、深色半透明底，Logo 固定在左上角。

- [ ] **Step 4: 补足模拟 worker 测试并运行**

在 `blog/test_video_worker.py` 将 `runner` 注入 `run_job`，断言 FFmpeg 命令位于 Remotion 命令之前，且当模拟 FFmpeg 返回 `returncode=1, stderr="bad input"` 时 job 为 `failed` 并包含 `bad input`。

Run: `blog/.venv/bin/python blog/test_video_jobs.py && blog/.venv/bin/python blog/test_video_worker.py`
Expected: both scripts print `全部通过 ✅` without needing a real FFmpeg or Node installation.

- [ ] **Step 5: 添加本地命令与渲染依赖说明**

在 `run.sh` 增加：

```bash
growth-worker)
  [ $# -eq 1 ] || { echo "[ERROR] 用法: ./run.sh growth-worker <job_id>"; exit 1; }
  blog/.venv/bin/python blog/video_worker.py "$1"
  ;;
growth-check)
  command -v ffmpeg >/dev/null || { echo "[ERROR] 未找到 ffmpeg"; exit 1; }
  test -d video_templates/short-video/node_modules || { echo "[ERROR] 请先在 video_templates/short-video 执行 npm install"; exit 1; }
  echo "增长中台视频环境可用"
  ;;
```

`video_templates/short-video/package.json` 固定 `render` 为 `remotion render src/index.jsx ShortVideo`，并将 `@remotion/cli`、`@remotion/bundler`、`@remotion/renderer`、`react`、`react-dom` 固定为同一 Remotion 主版本。根 `package.json` 只添加 `"video:render": "npm run render --prefix video_templates/short-video"`。

- [ ] **Step 6: Commit**

```bash
git add blog/video_jobs.py blog/video_worker.py blog/test_video_jobs.py blog/test_video_worker.py scripts/render-short-video.mjs video_templates/short-video run.sh package.json
git commit -m "feat: add bounded short video rendering jobs"
```

## Task 4: 实现网易 SMTP 的人工确认发送

**Files:**
- Create: `blog/mail_service.py`
- Create: `blog/test_mail_service.py`

**Interfaces:**
- Consumes: `Config.NETEASE_SMTP_HOST`、`Config.NETEASE_SMTP_PORT`、`Config.NETEASE_SMTP_USER`、`Config.NETEASE_SMTP_AUTH_CODE`、视频公开下载 URL。
- Produces:
  - `validate_draft(draft: dict) -> dict`
  - `compose_message(draft: dict, attachment_path: Path | None, attachment_limit: int) -> EmailMessage`
  - `send_confirmed_mail(draft: dict, config: object, smtp_factory=smtplib.SMTP_SSL) -> dict`

- [ ] **Step 1: 写邮件服务失败测试**

创建 `blog/test_mail_service.py`：

```python
from types import SimpleNamespace

from mail_service import send_confirmed_mail


class FakeSMTP:
    sent = []
    def __init__(self, host, port, timeout):
        self.host, self.port = host, port
    def __enter__(self): return self
    def __exit__(self, *_): return None
    def login(self, user, password): self.user = user
    def send_message(self, message): self.sent.append(message)


def test_confirmed_b2b_mail_sends_once():
    config = SimpleNamespace(NETEASE_SMTP_HOST="smtp.163.com", NETEASE_SMTP_PORT=465, NETEASE_SMTP_USER="seller@163.com", NETEASE_SMTP_AUTH_CODE="code", NETEASE_MAX_ATTACHMENT_BYTES=1)
    result = send_confirmed_mail({"confirmed": True, "to": "buyer@example.com", "subject": "电池方案", "body": "张总您好", "video_url": "https://example.com/video.mp4"}, config, smtp_factory=FakeSMTP)
    assert result["status"] == "sent"
    assert len(FakeSMTP.sent) == 1
    print("✓ confirmed mail sends through SMTP")


def test_unconfirmed_mail_never_opens_smtp_connection():
    config = SimpleNamespace(NETEASE_SMTP_HOST="smtp.163.com", NETEASE_SMTP_PORT=465, NETEASE_SMTP_USER="seller@163.com", NETEASE_SMTP_AUTH_CODE="code", NETEASE_MAX_ATTACHMENT_BYTES=1)
    try:
        send_confirmed_mail({"confirmed": False, "to": "buyer@example.com", "subject": "x", "body": "y"}, config, smtp_factory=FakeSMTP)
    except ValueError as exc:
        assert "confirmed" in str(exc)
    else:
        raise AssertionError("unconfirmed mail sent")
    print("✓ unconfirmed mail is blocked")


if __name__ == "__main__":
    test_confirmed_b2b_mail_sends_once()
    test_unconfirmed_mail_never_opens_smtp_connection()
    print("\\n全部通过 ✅")
```

- [ ] **Step 2: 运行失败测试**

Run: `blog/.venv/bin/python blog/test_mail_service.py`
Expected: `ModuleNotFoundError: No module named 'mail_service'`.

- [ ] **Step 3: 实现邮件校验、组成与发送**

`validate_draft` 必须校验 `confirmed is True`、单个有效收件人、非空 subject/body 和 `customer_type` 属于 `采购方 / 经销商 / 维修厂 / 车队`。消息使用 `EmailMessage`，设置 `From`、`To`、`Subject`、纯文本正文；视频优先以 URL 形式附在正文，只有本地文件存在且尺寸不超过阈值时才调用 `add_attachment`。发送实现固定为：

```python
with smtp_factory(config.NETEASE_SMTP_HOST, config.NETEASE_SMTP_PORT, timeout=20) as smtp:
    smtp.login(config.NETEASE_SMTP_USER, config.NETEASE_SMTP_AUTH_CODE)
    smtp.send_message(message)
return {"status": "sent", "sent_at": time.strftime("%Y-%m-%d %H:%M:%S")}
```

捕获 `smtplib.SMTPException`，返回 `{ "status": "failed", "error": "邮件发送失败：<安全摘要>" }`；不得记录授权码、完整 MIME 内容或客户附件内容。

- [ ] **Step 4: 运行邮件测试**

Run: `blog/.venv/bin/python blog/test_mail_service.py`
Expected: two checks print `✓` and final output contains `全部通过 ✅`.

- [ ] **Step 5: Commit**

```bash
git add blog/mail_service.py blog/test_mail_service.py
git commit -m "feat: add confirmed NetEase SMTP sending"
```

## Task 5: 接入 Flask 中台路由与老板可读的界面

**Files:**
- Create: `blog/templates/growth/index.html`
- Create: `blog/templates/growth/video_detail.html`
- Create: `blog/templates/growth/workshop.html`
- Create: `blog/templates/growth/customer_send.html`
- Create: `blog/templates/growth/settings.html`
- Create: `blog/templates/growth/_metric_card.html`
- Create: `blog/templates/growth/_video_row.html`
- Create: `blog/static/css/growth.css`
- Create: `blog/static/js/growth.js`
- Create: `blog/test_growth_routes.py`
- Modify: `blog/app.py`
- Modify: `blog/templates/base.html`

**Interfaces:**
- Consumes: `GrowthStore`、`parse_douyin_csv`、`import_rows`、`build_insight_report`、视频任务接口与 `send_confirmed_mail`。
- Produces:
  - `GET /growth`
  - `GET /growth/videos/<video_id>`
  - `GET|POST /growth/workshop`
  - `GET|POST /growth/customers/send`
  - `GET|POST /growth/settings`
  - `POST /growth/api/import-csv`
  - `GET /growth/api/video-jobs/<job_id>`
  - `POST /growth/api/video-jobs/<job_id>/confirm`
  - `POST /growth/api/send-mail`
  - `GET /growth/video-output/<job_id>`

- [ ] **Step 1: 写路由失败测试**

创建 `blog/test_growth_routes.py`：

```python
import io
import sys
from pathlib import Path
from tempfile import TemporaryDirectory

sys.path.insert(0, str(Path(__file__).parent))
import app as app_module


def test_growth_dashboard_marks_small_sample_as_reference():
    client = app_module.app.test_client()
    response = client.get("/growth")
    assert response.status_code == 200
    assert "视频增长中台" in response.get_data(as_text=True)
    print("✓ growth dashboard renders")


def test_growth_csv_import_rejects_non_csv():
    client = app_module.app.test_client()
    response = client.post("/growth/api/import-csv", data={"file": (io.BytesIO(b"x"), "metrics.xlsx")})
    assert response.status_code == 400
    assert response.get_json()["status"] == "bad_file"
    print("✓ metrics import rejects non-csv")


if __name__ == "__main__":
    test_growth_dashboard_marks_small_sample_as_reference()
    test_growth_csv_import_rejects_non_csv()
    print("\\n全部通过 ✅")
```

- [ ] **Step 2: 运行失败测试**

Run: `blog/.venv/bin/python blog/test_growth_routes.py`
Expected: first assertion fails with a 404 because `/growth` does not yet exist.

- [ ] **Step 3: 添加中台路由与视图模型**

在 `blog/app.py` 只新增 `growth_store()` 工厂和 `/growth` 路由组，不重写已有首页。工厂必须从 `app.config["GROWTH_DATA_DIR"]` 构造 store，便于测试替换：

```python
def growth_store():
    from growth_store import GrowthStore
    return GrowthStore(Path(app.config["GROWTH_DATA_DIR"]))


@app.get("/growth")
def growth_index():
    from growth_insights import build_insight_report
    videos = growth_store().list_videos()
    return render_template("growth/index.html", videos=videos, report=build_insight_report(videos))
```

`POST /growth/api/import-csv` 只接受 `.csv`，最大 5 MB，使用 `utf-8-sig` 解码。上传失败返回 `{ "status": "bad_file", "message": "请上传抖音创作者后台导出的 CSV 文件。" }` 和 HTTP 400。成功返回 `{ "status": "ok", "imported": N, "skipped": N }`。

`POST /growth/api/send-mail` 必须从 JSON 构建 draft，并且仅在 `confirmed: true` 时调用邮件服务。成功或失败都写入 `GrowthStore.record_mail`，失败记录以 `status="failed"` 存储；未确认请求返回 HTTP 400，不创建邮件记录。

- [ ] **Step 4: 生成中台页面与交互**

`growth/index.html` 必须显示：账号名称、最近同步时间、近 7 天趋势占位卡、本周互动最佳视频、样本提示、最多三条 AI 结论、一个下一条视频建议和“待粗剪/待发送”任务数。视频列表每行展示封面占位、标题、播放、点赞率、7 天变化、`复盘`、`发给客户`。

`growth/workshop.html` 只能呈现上传、三个候选片段、一个模板预览和渲染状态；不绘制自由时间线。`growth/customer_send.html` 必须展示客户公司、联系人、客户类型、业务阶段、邮箱、主题和正文；提交按钮文本固定为 `确认并通过网易邮箱发送`。

`growth.js` 在发送按钮绑定二次浏览器确认：

```javascript
if (!window.confirm('确认向该 B 端客户发送此邮件？发送后将写入跟进记录。')) return;
payload.confirmed = true;
```

`growth.css` 使用深色驾驶舱底色、紧凑指标卡、状态色和较大的中文正文；所有选择器均以 `.growth-` 开头，避免污染既有 `style.css`。

- [ ] **Step 5: 运行路由测试与现有路由回归**

Run: `blog/.venv/bin/python blog/test_growth_routes.py && blog/.venv/bin/python blog/test_app_routes.py`
Expected: both scripts print `全部通过 ✅`; existing `/`、详情页与 `/signal/attention` 保持通过。

- [ ] **Step 6: Commit**

```bash
git add blog/app.py blog/templates/base.html blog/templates/growth blog/static/css/growth.css blog/static/js/growth.js blog/test_growth_routes.py
git commit -m "feat: add automotive video growth hub UI"
```

## Task 6: 写运行说明、执行完整验证并进行视觉 QA

**Files:**
- Create: `README-growth-hub.md`
- Modify: `README.md`
- Modify: `run.sh`

**Interfaces:**
- Consumes: 已实现路由、CSV、FFmpeg、Remotion、网易 SMTP。
- Produces: 可复现的本地运行说明和完整验证命令。

- [ ] **Step 1: 写交付文档**

创建 `README-growth-hub.md`，必须包含以下完整、可复制的配置块，不填入真实密钥：

```dotenv
GROWTH_DATA_DIR=blog/data/growth
NETEASE_SMTP_USER=sales@example.com
NETEASE_SMTP_AUTH_CODE=replace-with-netease-authorization-code
NETEASE_MAX_ATTACHMENT_BYTES=18874368
OPENAI_API_KEY=replace-with-compatible-api-key
OPENAI_BASE_URL=https://api.openai.com/v1
OPENAI_MODEL=gpt-4.1-mini
```

同时写明 CSV 必需的 `作品ID` 与 `作品标题`，可选的播放/点赞/评论/分享列；明确此版本是“导入自己账号数据”，不是竞品抓取或抖音自动发布；列出 `/growth`、`./run.sh growth-check`、`./run.sh growth-worker <job_id>` 的用途。

- [ ] **Step 2: 更新主 README 的入口说明**

在 `README.md` 的博客章节增加一句：`汽车行业 B 端单账号视频增长中台见 README-growth-hub.md；它是本地 MVP，不替代抖音官方后台。` 该链接必须使用相对 Markdown 链接 `[README-growth-hub.md](README-growth-hub.md)`。

- [ ] **Step 3: 执行完整自动化测试**

Run:

```bash
set -e
for f in \
  blog/test_product_schema.py \
  blog/test_user_preferences.py \
  blog/test_embeddings.py \
  blog/test_ingest_jobs.py \
  blog/test_today_signal.py \
  blog/test_app_routes.py \
  blog/test_growth_store.py \
  blog/test_douyin_import.py \
  blog/test_growth_insights.py \
  blog/test_growth_ai.py \
  blog/test_video_jobs.py \
  blog/test_video_worker.py \
  blog/test_mail_service.py \
  blog/test_growth_routes.py
do
  blog/.venv/bin/python "$f"
done
node scripts/test-product-schema.mjs
node scripts/test-rewrite-format.mjs
git diff --check
```

Expected: all Python scripts print their success marker, both Node scripts exit 0, and `git diff --check` prints nothing.

- [ ] **Step 4: 做本地浏览器视觉 QA**

Run: `blog/.venv/bin/python blog/app.py`
Open: `http://127.0.0.1:5055/growth`

Verify manually at desktop width and 390 px width:

1. 首页显示“视频增长中台”、样本提示和最近视频表，而现有 `/` 内容库布局未变化。
2. CSV 导入失败信息为中文且不暴露 Python 栈信息。
3. 视频工坊只出现三个或更少连续候选片段，没有自由时间线。
4. 客户邮件页要求公司、联系人、类型、阶段和邮箱；点击发送出现二次确认。
5. 没有任何真实 SMTP 凭据时，设置页显示“未配置”，不显示密钥内容。

- [ ] **Step 5: Commit**

```bash
git add README-growth-hub.md README.md run.sh
git commit -m "docs: add growth hub operation guide"
```

---

## Spec Coverage Review

| 设计要求 | 覆盖任务 |
|---|---|
| 单账号抖音数据总览与每日快照 | Task 1、Task 2、Task 5 |
| 数据导入优先于未授权抓取 | Task 2、Task 5、Task 6 |
| 人话内容结论、样本不足提示与下一条建议 | Task 2、Task 5 |
| 30–60 秒连续粗剪、FFmpeg、Remotion、确认后正式渲染 | Task 3、Task 5 |
| B 端客户字段、可编辑邮件、网易 SMTP、人工确认与记录 | Task 1、Task 4、Task 5 |
| 5055 Flask 应用、复用 archive、避免重建 SaaS | Task 1、Task 5、Task 6 |
| 数据、密钥、风控与失败处理 | Task 1、Task 3、Task 4、Task 6 |
