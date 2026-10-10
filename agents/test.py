from pathlib import Path
import sys


PROJECT_ROOT = Path(__file__).resolve().parent
sys.path.insert(0, str(PROJECT_ROOT / "src"))

from agent_service.config import get_settings  # noqa: E402
from agent_service.llm import create_chat_model  # noqa: E402


model = create_chat_model(get_settings())
if model is None:
    raise RuntimeError("Configure an API key for the selected LLM_PROVIDER in .env")

response = model.invoke("Explain the importance of fast language models")
print(response.content)
