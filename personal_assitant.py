from time import sleep
from openai import OpenAI
from datetime import datetime
from common import get_secret
from dataclasses import dataclass
from typing import Any


@dataclass
class Conversation:

    client: OpenAI
    assistant_id: str
    run: Any = None

    def __init__(self):
        assistant_secrets = get_secret(
            secret_name="personal-ai-assistant", region_name="eu-west-1"
        )
        self.client = OpenAI(
            organization=assistant_secrets["OPENAI_ORGANIZATION"],
            api_key=assistant_secrets["OPENAI_API_KEY"],
        )
        self.assistant_id = assistant_secrets["ASSISTANT_ID"]

    def run_and_retrieve_message(self, prompt: str):
        if not self.run:
            self.run = self.client.beta.threads.create_and_run(
                assistant_id=self.assistant_id,
                thread={
                    "messages": [
                        {
                            "role": "user",
                            "content": f"{prompt}",
                        }
                    ]
                },
            )
        else:
            self.client.beta.threads.messages.create(
                thread_id=self.run.thread_id, role="user", content=f"{prompt}"
            )

            self.run = self.client.beta.threads.runs.create(
                thread_id=self.run.thread_id,
                assistant_id=self.run.assistant_id,
            )
        return self._retrieve_message()

    def _retrieve_message(self):
        while self.run.status not in ["completed", "failed"]:
            sleep(2)
            self.run = self.client.beta.threads.runs.retrieve(
                thread_id=self.run.thread_id, run_id=self.run.id
            )
            print(self.run.status)
        messages = self.client.beta.threads.messages.list(thread_id=self.run.thread_id)
        return messages.data[0].content[0].text.value

    def reset_run(self):
        self.run = None
