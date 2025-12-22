from datetime import datetime

from fastapi import APIRouter, Form, Request
from fastapi.responses import HTMLResponse, Response

from src.core import Crud, SessionDep, templates

router = APIRouter(prefix="/items", tags=["Items"])
crud = Crud()


@router.get("/", response_class=HTMLResponse)
def items_table(request: Request, session: SessionDep):
    items = crud.get_item(session)
    return templates.TemplateResponse(
        "components/table.html",
        {"request": request, "items": items},
    )


@router.post("/add")
def add_item(
    session: SessionDep,
    date: datetime = Form(...),
    category_id: int = Form(...),
    name: str = Form(...),
    label_id: int = Form(...),
    total: int = Form(...),
):

    if crud.set_item(session, date, category_id, name, label_id, total):
        items = crud.get_item(session)
        if items:
            return {"Status": "Oks"}


@router.delete("/delete/{id}")
def delete_item(session: SessionDep, id: int):
    if crud.delete_item(session, id):
        return Response(status_code=204, headers={"HX-Refresh": "true"})
    else:
        Response(status_code=404)
