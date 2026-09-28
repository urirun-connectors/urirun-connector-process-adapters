"""urirun connector for Process URI adapters: sandbox://, pypi://, and browser://."""

from __future__ import annotations

import subprocess
from dataclasses import dataclass
from pathlib import Path
from typing import Any
from urllib.parse import parse_qsl, urlsplit


@dataclass
class SandboxConfig:
    image: str = "python:3.11-slim"
    max_memory: str = "512m"
    max_cpus: float = 1.0
    timeout_sec: int = 60
    network: str = "none"


class DockerSandboxRunner:
    """Executes commands in an isolated Docker container."""

    def __init__(self, config: SandboxConfig | None = None) -> None:
        self.config = config or SandboxConfig()

    def build_docker_cmd(
        self,
        command: str,
        *,
        workspace_mount: Path | None = None,
        env_vars: dict[str, str] | None = None,
    ) -> list[str]:
        cmd = [
            "docker",
            "run",
            "--rm",
            f"--memory={self.config.max_memory}",
            f"--cpus={self.config.max_cpus}",
            f"--network={self.config.network}",
        ]
        if workspace_mount:
            cmd.extend(["-v", f"{workspace_mount.resolve()}:/workspace:rw", "-w", "/workspace"])
        if env_vars:
            for k, v in env_vars.items():
                cmd.extend(["-e", f"{k}={v}"])
        cmd.extend([self.config.image, "sh", "-c", command])
        return cmd


class CdpBrowserController:
    """Translates browser:// Process URIs into CDP commands."""

    def __init__(self, endpoint_url: str = "http://127.0.0.1:9222") -> None:
        self.endpoint_url = endpoint_url
        self._message_id = 0

    def next_id(self) -> int:
        self._message_id += 1
        return self._message_id

    def build_cdp_frame(self, method: str, params: dict[str, Any] | None = None) -> dict[str, Any]:
        return {
            "id": self.next_id(),
            "method": method,
            "params": params or {},
        }


def sandbox_bindings() -> dict[str, Any]:
    return {"scheme": "sandbox", "runner": DockerSandboxRunner}


def browser_bindings() -> dict[str, Any]:
    return {"scheme": "browser", "controller": CdpBrowserController}
