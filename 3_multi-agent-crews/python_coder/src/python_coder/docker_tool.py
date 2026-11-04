import subprocess
from typing import Type

from crewai.tools import BaseTool
from pydantic import BaseModel, Field


class RunPythonInput(BaseModel):
    code: str = Field(..., description="Complete Python 3 source code to execute. It must print its results.")


class RunPythonInDocker(BaseTool):
    name: str = "run_python_in_docker"
    description: str = (
        "Runs Python code in an isolated Docker container (no network, 256 MB RAM, 60 s limit) "
        "and returns the exit code, stdout and stderr. Use it to really execute code and see its output."
    )
    args_schema: Type[BaseModel] = RunPythonInput

    def _run(self, code: str) -> str:
        cmd = [
            "docker", "run", "--rm", "-i",
            "--network", "none",
            "--memory", "256m",
            "--cpus", "1",
            "python:3.12-slim",
            "python", "-",
        ]
        try:
            result = subprocess.run(
                cmd, input=code, capture_output=True,
                text=True, encoding="utf-8", errors="replace", timeout=60,
            )
        except subprocess.TimeoutExpired:
            return "ERROR: execution timed out after 60 seconds."
        return (
            f"exit code: {result.returncode}\n"
            f"--- stdout ---\n{result.stdout}\n"
            f"--- stderr ---\n{result.stderr}"
        )