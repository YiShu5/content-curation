"""外部命令真实探活。

本模块改编自 Agent-Reach 的 ``agent_reach/probe.py``：
https://github.com/Panniantong/Agent-Reach/blob/e825f6740d24c6c315c3b0dc41907e6c87ff39a5/agent_reach/probe.py

原项目采用 MIT License，版权与许可说明见项目根目录 THIRD_PARTY_NOTICES.md。
"""

import os
import shutil
import subprocess
from dataclasses import dataclass
from typing import Optional, Sequence


@dataclass
class ProbeResult:
    status: str  # "ok" | "missing" | "broken" | "timeout" | "error"
    output: str = ""
    hint: str = ""

    @property
    def ok(self) -> bool:
        return self.status == "ok"


def reinstall_hint(package: str) -> str:
    """返回 Python CLI 虚拟环境断链时的修复处方。"""
    return (
        "命令存在但无法执行——通常是系统 Python 升级后 venv 解释器丢失。"
        f"重装即可修复：uv tool install --force {package}"
    )


def probe_command(
    cmd: str,
    args: Sequence[str] = ("--version",),
    timeout: int = 10,
    package: Optional[str] = None,
) -> ProbeResult:
    """真实执行无副作用命令，区分缺失、断链、超时和普通错误。"""
    path = shutil.which(cmd)
    if not path:
        return ProbeResult("missing", hint=f"找不到命令：{cmd}")

    env = os.environ.copy()
    env.update({"PYTHONUTF8": "1", "PYTHONIOENCODING": "utf-8"})
    try:
        result = subprocess.run(
            [path, *args],
            capture_output=True,
            encoding="utf-8",
            errors="replace",
            timeout=timeout,
            env=env,
        )
    except FileNotFoundError:
        return ProbeResult("broken", hint=reinstall_hint(package or cmd))
    except OSError:
        return ProbeResult("broken", hint=reinstall_hint(package or cmd))
    except subprocess.TimeoutExpired:
        return ProbeResult("timeout", hint=f"`{path}` 响应超时（>{timeout}s）")

    output = ((result.stdout or "") + (result.stderr or "")).strip()
    if result.returncode in (126, 127):
        return ProbeResult("broken", output=output, hint=reinstall_hint(package or cmd))
    if result.returncode != 0:
        return ProbeResult("error", output=output)
    return ProbeResult("ok", output=output)
