from pathlib import Path
from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates

from sqlalchemy import text
from data.database import engine

PROJECT_DIR = Path(__file__).resolve().parent.parent
FRONTEND_DIR = PROJECT_DIR / "frontend"

app = FastAPI()
frontend = Jinja2Templates(directory=str(FRONTEND_DIR))
app.mount("/static", StaticFiles(directory=str(FRONTEND_DIR)), name="static")

def get_products_count():
    with engine.connect() as connection:
        count = connection.execute(text("SELECT COUNT(*) FROM items")).scalar_one()
    return count

def get_products():
    with engine.connect() as connection:
        products = connection.execute(text("SELECT * FROM items"))
        products = products.fetchall()
    return products


#main page
@app.get("/", response_class=HTMLResponse)
async def home_page(request: Request):
    products_count = get_products_count()
    products = get_products()
    return frontend.TemplateResponse(
            request=request,
            name="index.html",
            context={
                "products_count": products_count,
                "products": products
                }
            )

@app.get("/products/{products_url}_{products_id}")
async def read_item(products_url, products_id):
    return {"products_id": products_id, "products_url": products_url}
