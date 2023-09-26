from typing import Any

import torch
from interfaces import model
from torch import Tensor
from transformers import AutoModelForCausalLM, AutoTokenizer
from utils import model as model_deco

MODEL_NAME = "deepparag/Aeona"


class DaveModel(model.DaveModelInterface):
    """DaveModel is an NLP conversational Model

    This is responsible for providing auto
    generated conversation to users
    """

    def __init__(self) -> None:
        self._tokenizer: Any = AutoTokenizer.from_pretrained(
            MODEL_NAME, padding_side="left"
        )
        self._model: Any = AutoModelForCausalLM.from_pretrained(MODEL_NAME)

    def get_model(self) -> Any:
        """Get the model"""
        return self._model

    @model_deco.model_error_handler
    def reply(self, question: str) -> str:
        """Reply to the user request

        This is responsible for replying
        to the user request or message

        Args:
            question (str): Question you want to ask

        Returns:
            str: Return a reply
        """
        chat_history_ids: Tensor = Tensor()

        for step in range(4):
            user_input_ids = self._tokenizer.encode(
                f">> User: {question}" + self._tokenizer.eos_token,
                return_tensors="pt",
            )

            dave_input_ids = (
                torch.cat([chat_history_ids, user_input_ids], dim=-1)
                if step > 0
                else user_input_ids
            )

            chat_history_ids = self._model.generate(
                dave_input_ids,
                max_length=200,
                pad_token_id=self._tokenizer.eos_token_id,
                no_repeat_ngram_size=4,
                do_sample=True,
                top_k=100,
                top_p=0.7,
                temperature=0.8,
            )

            response: str = "{}".format(
                self._tokenizer.decode(
                    chat_history_ids[:, dave_input_ids.shape[-1] :][  # noqa: E203,E501
                        0
                    ],  # type: ignore
                    skip_special_tokens=True,
                )
            )

            return response
