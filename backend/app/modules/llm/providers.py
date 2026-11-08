"""Adaptateurs LLM réels (activés par configuration, non requis en DEMO)."""

from abc import ABC, abstractmethod
from typing import Any


class LLMProvider(ABC):
    @abstractmethod
    async def complete_structured(self, *, prompt: str, schema: dict[str, Any]) -> dict[str, Any]:
        ...


class OpenAIAdapter(LLMProvider):
    def __init__(self, api_key: str) -> None:
        self.api_key = api_key

    async def complete_structured(self, *, prompt: str, schema: dict[str, Any]) -> dict[str, Any]:
        if not self.api_key:
            raise RuntimeError("OPENAI_API_KEY manquant")
        raise NotImplementedError("Configurer le client HTTP OpenAI — hors DEMO")


class AnthropicAdapter(LLMProvider):
    def __init__(self, api_key: str) -> None:
        self.api_key = api_key

    async def complete_structured(self, *, prompt: str, schema: dict[str, Any]) -> dict[str, Any]:
        if not self.api_key:
            raise RuntimeError("ANTHROPIC_API_KEY manquant")
        raise NotImplementedError("Configurer le client Anthropic — hors DEMO")
