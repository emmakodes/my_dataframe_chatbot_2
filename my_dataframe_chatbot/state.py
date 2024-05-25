import os
import reflex as rx

from langchain_experimental.agents.agent_toolkits import create_pandas_dataframe_agent
from langchain.chat_models import ChatOpenAI
from langchain.agents.agent_types import AgentType

import pandas as pd


class State(rx.State):

    # The current question being asked.
    question: str

    error_message: str 

    chat_history: list[tuple[str, str]]

    openai_api_key: str

    # The files to show.
    csv_file: list[str]

    upload_confirmation: str = ""

    file_path: str

    is_skeleton_loaded: bool = True

    show: bool = False
            

    async def handle_upload(self, files: list[rx.UploadFile]):
        for file in files:
            upload_data = await file.read()
            outfile = rx.get_upload_dir() / file.filename
            self.file_path = str(outfile)
            with outfile.open("wb") as file_object:
                file_object.write(upload_data)
        self.upload_confirmation = "csv file uploaded successfully, you can now interact with your data"



    async def answer(self):
        yield rx.call_script(f"document.getElementById('downloadbutton').scrollIntoView();")

        self.upload_confirmation = ""

        # check if openai_api_key is empty to return an error
        if self.openai_api_key == "":
            self.error_message = "enter your openai api"
            return

        if os.path.exists(self.file_path):
            df = pd.read_csv(self.file_path)
        else:
            self.error_message = "ensure you upload a csv file"
            return
        
        # turn loading state of the skeleton component to False
        self.is_skeleton_loaded = False
        yield

        # initializes an agent for working with a chatbot and integrates it with a Pandas DataFrame
        agent = create_pandas_dataframe_agent(
                    ChatOpenAI(temperature=0, model="gpt-3.5-turbo-0613", openai_api_key=self.openai_api_key),
                    df,
                    agent_type=AgentType.OPENAI_FUNCTIONS,
                )

        # Add to the answer as the chatbot responds.
        answer = ""
        self.chat_history.append((self.question, answer))
        yield

        # run the agent against a question
        output = agent.run(self.question)

        self.is_skeleton_loaded = True

        # Clear the question input.
        self.question = ""

        # Yield here to clear the frontend input before continuing.
        yield

        # update answer from output
        for item in output:
            answer += item
            self.chat_history[-1] = (
                self.chat_history[-1][0],
                answer,
            )
            yield


    def change(self):
        self.show = not (self.show)
