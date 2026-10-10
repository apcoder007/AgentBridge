"""Create the application's shared chat model from centralized settings."""

from agent_service.config import Settings, get_settings


def create_chat_model(settings: Settings | None = None):
    """Build the configured provider model, or return None for offline mode."""

    settings = settings or get_settings()

    if settings.llm_provider == "openai":
        if not settings.openai_api_key:
            return None

        from langchain_openai import ChatOpenAI

        return ChatOpenAI(
            api_key=settings.openai_api_key,
            model=settings.openai_model,
            temperature=0,
        )

    if settings.llm_provider == "anthropic":
        if not settings.anthropic_api_key:
            return None

        from langchain_anthropic import ChatAnthropic

        return ChatAnthropic(
            api_key=settings.anthropic_api_key,
            model=settings.anthropic_model,
            temperature=0,
        )

    if not settings.groq_api_key:
        return None

    from langchain_openai import ChatOpenAI

    return ChatOpenAI(
        api_key=settings.groq_api_key,
        base_url=settings.groq_base_url,
        model=settings.groq_model,
        temperature=0,
    )
