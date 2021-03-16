import json
import magic
from io import BytesIO
from pandas import read_csv
from fastapi.encoders import jsonable_encoder

from src.models.roll import Item, collection


class manage():

    def __init__(self):      
        """ Check if collection properly exist """


    async def validate(self, upload) -> bool:
        """ Verify file (extension) magic numbers """


    async def read(self) -> str:
        """ Read list from roll collection """
        data = jsonable_encoder([])
        for row in await collection.find().to_list(length=5):
            row.pop("_id")
            data.append(row)
        return data


    async def write(self, upload) -> bool:
        """ Write new roll based on CSV/XLS file"""
        self.validate(upload)
        contents = read_csv(BytesIO(await upload.read()))
        data = json.loads(contents.to_json(orient='records'))
        insert = await collection.insert_many(data)
