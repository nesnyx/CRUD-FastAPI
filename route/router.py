from fastapi import APIRouter, Path, HTTPException, status,Request,Depends,Form
from config.database import  db
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
from fastapi.responses import HTMLResponse,RedirectResponse
from sqlalchemy.orm import Session
from models import models
from schemas.plants import Plant
from config.database import SessionLocal,engine

# Get Database
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

router = APIRouter()
templates = Jinja2Templates(directory='./templates/')

@router.get('/')
async def home(request : Request):
    return templates.TemplateResponse('index.html',{'request': request})

@router.get('/crud')
async def crud_system(request: Request, db:Session=Depends(get_db)):
    data = db.query(models.Plant).all()
    return templates.TemplateResponse('crud.html', {'request': request, 'data':data})

@router.get('/add')
async def add_data(request: Request):
    return templates.TemplateResponse('add.html', {'request' : request})

# crud 
@router.post('/addData')
async def add(request: Request, name:str=Form(...), family_name:str=Form(...), science_name:str = Form(...),db: Session=Depends(get_db)):
    new_data = models.Plant(name=name, family_name=family_name, science_name=science_name)
    db.add(new_data)
    db.commit()
    db.refresh(new_data)
    url = router.url_path_for('crud_system')
    return RedirectResponse(url=url,status_code=status.HTTP_303_SEE_OTHER )

@router.get('/edit/{id}')
async def edit(request:Request,id:int, db:Session=Depends(get_db)):
    plant = db.query(models.Plant).filter(models.Plant.id == id).first()
    return templates.TemplateResponse('edit.html', {'request':request, 'data':plant})

@router.post('/update/{id}')
async def update(request:Request, id:int, name:str=Form(...), family_name:str=Form(...), science_name:str = Form(...),db: Session=Depends(get_db)):
    plants=db.query(models.Plant).filter(models.Plant.id == id).first()
    plants.name = name
    plants.family_name = family_name
    plants.science_name = science_name
    db.commit()
    url = router.url_path_for('crud_system')
    return RedirectResponse(url=url,status_code=status.HTTP_303_SEE_OTHER )

@router.get('/delete/{id}')
async def delete(request:Request,id:int, db:Session=Depends(get_db)):
    plants = db.query(models.Plant).filter(models.Plant.id == id).first()
    db.delete(plants)
    db.commit()
    url = router.url_path_for('crud_system')
    return RedirectResponse(url=url,status_code=status.HTTP_303_SEE_OTHER )