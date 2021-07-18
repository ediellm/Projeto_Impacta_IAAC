#
#
# Uma app de envio de mensagens (slack like)
from pymongo import MongoClient
from fastapi import FastAPI, status
from pydantic import BaseModel
from typing import List

DB = "slack"
MSG_COLLECTION = "messages"


# Classe que ira definir o schema do mongodb
class Message(BaseModel):
    channel: str
    author: str
    text: str


# Inicializacao do FastApi
app = FastAPI()


@app.get("/healthcheck")
def get_status():
    """Endpoint para status da aplicacao"""
    return {"status": "running"}


@app.get("/channels", response_model=List[str])
def get_channels():
    """Get all channels in list form."""
    with MongoClient() as client:
        msg_collection = client[DB][MSG_COLLECTION]
        distinct_channel_list = msg_collection.distinct("channel")
        return distinct_channel_list


@app.get("/messages/{channel}", response_model=List[Message])
def get_messages(channel: str):
    """Get all messages for the specified channel."""
    with MongoClient() as client:
        msg_collection = client[DB][MSG_COLLECTION]
        msg_list = msg_collection.find({"channel": channel})
        response_msg_list = []
        for msg in msg_list:
            response_msg_list.append(Message(**msg))
        return response_msg_list


@app.post("/post_message", status_code=status.HTTP_201_CREATED)
def post_message(message: Message):
    """Post a new message to the specified channel."""
    with MongoClient() as client:
        msg_collection = client[DB][MSG_COLLECTION]
        result = msg_collection.insert_one(message.dict())
        ack = result.acknowledged
        return {"insertion": ack}
