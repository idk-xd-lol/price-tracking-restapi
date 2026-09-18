from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates

app = FastAPI()
frontend = Jinja2Templates(directory="frontend")

product_count = 123

@app.get("/", response_class=HTMLResponse)
async def home_page(request: Request):
    return frontend.TemplateResponse(
            request=request,
            name="home.html",
            context={
                "products_count": product_count
                }
            )
