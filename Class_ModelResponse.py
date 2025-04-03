from typing import List, Optional
# https://docs.python.org/3/library/typing.html
# https://docs-python.ru/standart-library/modul-typing-python/

class UsageResponse:
    prompt_tokens: int
    completion_tokens: int
    total_tokens: int

class MessageResponse:
    role: str
    content: str

class ChoiceResponse:
    index: int
    message: MessageResponse
    logprobs: Optional[str]
    finish_reason: str

class ModelResponse:
    id: str
    object: str
    created: int
    model: str
    choices: List[ChoiceResponse]
    usage: UsageResponse
    system_fingerprint: str
