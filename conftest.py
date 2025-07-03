import os

import pytest
from langchain_openai import ChatOpenAI
from ragas.llms import LangchainLLMWrapper

os.environ[
    "OPENAI_API_KEY"] = "sk-proj-G5-ysceXJFhT1TdeXmBqyvDQugiQTg6taa91lnRNWahjEcL3XT3BlbkFJhJE_y3YTLuYwFQR3qIcl1qsvtv7AQQ4mDmaeHeZoNe795dezsUfbOxPDn-vkCtW1qUNvU8GVkA"


@pytest.fixture
def llm_wrapper():
    llm = ChatOpenAI(model="gpt-4", temperature=0)
    lang_chain_llm = LangchainLLMWrapper(llm)
    return lang_chain_llm
