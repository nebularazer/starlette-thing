import os
from datetime import datetime
from typing import List

from databases import Database
from starlette.applications import Starlette
from starlette.responses import Response, JSONResponse
from starlette.routing import Route
from pydantic import BaseModel

import sqlalchemy as sa

metadata = sa.MetaData()

notes = sa.Table(
    "notes",
    metadata,
    sa.Column("id", sa.Integer, primary_key=True),
    sa.Column("text", sa.String(length=100)),
    sa.Column("date", sa.DateTime(timezone=True)),
)

class Note(BaseModel):
    id: int
    text: str
    date: datetime

class NotesResponse(BaseModel):
    notes: List[Note]

database = Database(os.getenv('DATABASE_URL'))

async def homepage(request):
    query = notes.select()
    results = await database.fetch_all(query)
    content = NotesResponse(
        notes=[
            Note(**result)
            for result in results
        ]
    )
    return Response(content.json(), media_type='application/json')


app = Starlette(
    debug=True,
    routes=[
        Route('/', homepage),
    ],
    on_startup=[database.connect],
    on_shutdown=[database.disconnect],
)