"""Model backends.

* ``MockBackend`` is deterministic and needs no model. It exists so that every
  command in this repository runs in seconds on any machine. It is clearly
  labelled as a mock in every record it produces.
* ``OllamaBackend`` calls a local open-weight model through the Ollama HTTP API
  (https://ollama.com), with temperature 0 and a fixed seed.
"""
from __future__ import annotations

import json
import urllib.request


class MockBackend:
    """Keyword classifier standing in for an LLM in the toy analytic example."""

    name = "lem-mock-classifier"
    version = "0.1"
    provider = "local (deterministic mock, not an LLM)"
    open_weights = True

    RULES = [
        ("idea-generation", ("hypothes", "idea", "brainstorm", "theory", "concept")),
        ("drafting", ("draft", "paragraph", "write", "section", "outline")),
        ("editing", ("grammar", "spelling", "typo", "polish", "tone")),
    ]

    def generate(self, prompt: str, text: str, temperature: float = 0.0, seed: int = 0) -> str:
        low = text.lower()
        for label, keys in self.RULES:
            if any(k in low for k in keys):
                return label
        return "none"


class OllamaBackend:
    provider = "ollama (local)"
    open_weights = True

    def __init__(self, model: str = "llama3.2:1b", host: str = "http://localhost:11434"):
        self.name = model
        self.version = model
        self.host = host

    def generate(self, prompt: str, text: str, temperature: float = 0.0, seed: int = 0) -> str:
        payload = {
            "model": self.name,
            "prompt": f"{prompt}\n\nText: {text}\nLabel:",
            "stream": False,
            "options": {"temperature": temperature, "seed": seed},
        }
        req = urllib.request.Request(
            f"{self.host}/api/generate",
            data=json.dumps(payload).encode("utf-8"),
            headers={"Content-Type": "application/json"},
        )
        with urllib.request.urlopen(req, timeout=120) as resp:
            out = json.loads(resp.read().decode("utf-8"))["response"]
        return out.strip().split()[0].strip(".,:;").lower() if out.strip() else ""


def get_backend(spec: str):
    if spec == "mock":
        return MockBackend()
    if spec.startswith("ollama:"):
        return OllamaBackend(spec.split(":", 1)[1])
    raise ValueError(f"Unknown backend '{spec}'. Use 'mock' or 'ollama:<model>'.")
