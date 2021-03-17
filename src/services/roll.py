import json
import magic
from io import BytesIO
from pandas import read_csv
from fastapi.encoders import jsonable_encoder

from src.models.roll import Roll, collection


class manage():

    def __init__(self):      
        """ Check if collection properly exist """
        pass


    async def validate(self, upload) -> bool:
        """ Verify file (extension) magic numbers """
        extension = magic.from_file(upload)
        pass


    async def read(self) -> str:
        """ Read list from roll collection """
        data = jsonable_encoder([])
        async for roll in Roll.all():
            data.append({
                "id": roll.id,
                "name": roll.name
            })
        data = json.dumps(data)
        return data


    async def write(self, upload) -> bool:
        """ Write new roll based on CSV/XLS file"""
        self.validate(upload)
        contents = read_csv(BytesIO(await upload.read()))
        data = json.loads(contents.to_json(orient='records'))
        insert = await collection.insert_many(data)


    async def clear(self) -> None:
        """ Clear roll collection """
        await collection.delete_many({})