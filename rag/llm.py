import os
import sys
import time
from abc import ABC

from langchain_core.callbacks import CallbackManagerForLLMRun
from llama_cpp import Llama
from langchain.llms.base import LLM
from pydantic import Field
from typing import Dict, Any, Mapping, Optional, List

BASE_DIR = os.path.dirname(__file__)
# PRJ_DIR上层目录
# PRJ_DIR = os.path.abspath(os.path.join(BASE_DIR, ".."))
sys.path.append(BASE_DIR)

def get_llm_model(
        prompt: str = None,
        model: str = None,
        temperature: float = 0.0,
        max_token: int = 2048,
        n_ctx: int = 512):
    """
    根据模型名称去加载模型，返回response数据
    :param prompt:
    :param model:
    :param temperature:
    :param max_token:
    :param n_ctx:
    :return:
    """
    if model in ['Qwen_q2']:
        model_path = os.environ[model]
        llm = Llama(model_path=model_path, n_ctx=n_ctx)
        start = time.time()
        response = llm.create_chat_completion(
            messages=[
                {
                    "role": "system",
                    "content": "你是一个智能超级助手，请用专业的词语回答问题，整体上下文带有逻辑性，如果不知道，请不要乱说",
                },
                {
                    "role": "user",
                    "content": "{}".format(prompt)
                },
            ],
            temperature=temperature,
            max_tokens=max_token,
            stream=False
        )
        cost = time.time() - start
        print(f"模型生成时间：{cost}")
        print(f"大模型回复：\n{response}")
        return response['choices'][0]['message']['content']

class QwenLLM(LLM):
    """
    自定义QwenLLM
    """
    model_name: str = "Qwen_q2"
    # 访问时延上限
    request_timeout: float = None
    # 温度系数
    temperature: float = 0.1
    # 窗口大小
    n_ctx = 2048
    # token大小
    max_tokens = 1024
    # 必备的可选参数
    model_kwargs: Dict[str, Any] = Field(default_factory=dict)

    def _call(self, prompt: str, stop: Optional[List[str]] = None,
              run_manager: Optional[CallbackManagerForLLMRun] = None,
              **kwargs: Any):
        qwen_path = os.environ[self.model_name]
        print("qwen_path:", qwen_path)

        llm = Llama(model_path=qwen_path, n_ctx=self.n_ctx)

        response = llm.create_chat_completion(
            messages=[
                {
                    "role": "system",
                    "content": "你是一个智能超级助手，请用[中文]专业的词语回答问题，整体上下文带有逻辑性，并以markdown格式输出",
                },
                {
                    "role": "user",
                    "content": "{}".format(prompt)
                },
            ],
            temperature=self.temperature,
            max_tokens=self.max_tokens,
            stream=False
        )

        # prompt工程提示

        # print(f"Qwen prompt: \n{prompt}")
        # response = lla(
        #     prompt=prompt,
        #     temperature=self.temperature,
        #     max_tokens=self.max_tokens
        # )
        print(f"Qwen response: \n{response}")
        # return response['choices'][0]['text']
        return response['choices'][0]['message']['content']

    @property
    def _llm_type(self) -> str:
        return "Llama3"

        # 定义一个返回默认参数的方法

    @property
    def _default_params(self) -> Dict[str, Any]:
        """获取调用默认参数。"""
        normal_params = {
            "temperature": self.temperature,
            "request_timeout": self.request_timeout,
            "n_ctx": self.n_ctx,
            "max_tokens": self.max_tokens
        }
        # print(type(self.model_kwargs))
        return {**normal_params}

    @property
    def _identifying_params(self) -> Mapping[str, Any]:
        """Get the identifying parameters."""
        return {**{"model_name": self.model_name}, **self._default_params}
