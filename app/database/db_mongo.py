import time
import docker
from pymongo import MongoClient

import os
from dotenv import load_dotenv

load_dotenv()

docker_client = docker.from_env()

mongo_container = docker_client.containers.run(
    "mongo:latest",
    name="python_local_mongo",
    ports={"27017/tcp": 27017},  # Map container port 27017 to localhost:27017
    detach=True,  # Run in background
    # remove=True,  # Automatically delete container when stopped
)

time.sleep(3)


class Config:
    MONGO_URI = os.getenv("MONGO_URI")


try:
    client = MongoClient(Config.MONGO_URI)
    db = client["stylesync"]
    produtos = db["produtos"]

    produtos.insert_one(
        {
            "nome": "Placa de Video RTX 9090",
            "preco": 15999.98,
            "descricao": "A placa de video mais potente para jogos",
            "estoque": 50,
        }
    )

    for produto in produtos.find():
        print(produto)

except Exception as e:
    print("Erro ao se conectar ao MongoDB.", e)

finally:
    mongo_container.stop()
