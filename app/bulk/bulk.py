import pandas as pd
from fastapi import File, HTTPException
from pydantic import BaseModel, ValidationError


async def get_bulk_dict(file: File(...), model: BaseModel) -> list[dict]:
    if not file.filename.endswith(".csv"):
        raise HTTPException(status_code=422, detail="Файл должен быть в формате CSV")

    try:
        records = pd.read_csv(file.file).to_dict(orient="records")

        return [model(**record).dict() for record in records]
    except ValidationError as e:
        raise HTTPException(status_code=422, detail=e.errors())
