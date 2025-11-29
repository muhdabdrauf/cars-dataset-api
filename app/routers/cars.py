from fastapi import APIRouter, Depends, HTTPException, Query, Request
from sqlalchemy.orm import Session
from app.database import get_db
from app.schemas import CarCreate, CarResponse, PaginatedCarResponse
from app import crud
from app.auth import verify_api_key
from app.limits import limiter

router = APIRouter(prefix="/cars", tags=["Cars"])

@router.get("/", response_model=PaginatedCarResponse)
@limiter.limit("20/minute")
def get_all_cars(
    request: Request,
    db: Session = Depends(get_db),
    page: int = Query(1, ge=1),
    page_size: int = Query(25, ge=1, le=100),
    sort: str = Query("car_id:asc", description="e.g. 'purchased_date:desc,car_id:asc'"),
    brand_id: int | None = Query(None),
    model_id: int | None = Query(None),
    color_id: int | None = Query(None),
    q: str | None = Query(None, description="Text search across brand/model names")
):
    result = crud.get_all_cars(
        db,
        page=page,
        page_size=page_size,
        sort=sort,
        brand_id=brand_id,
        model_id=model_id,
        color_id=color_id,
        q=q
    )
    return result


@router.get("/{car_id}", response_model=CarResponse)
def get_car(car_id: int, db: Session = Depends(get_db)):
    car = crud.get_car_by_id(db, car_id)
    if not car:
        raise HTTPException(status_code=404, detail="Car not found")
    return car

@router.post("/", response_model=CarResponse, dependencies=[Depends(verify_api_key)])
def create_car(car: CarCreate, db: Session = Depends(get_db)):
    return crud.create_car(db, car)

@router.delete("/{car_id}", dependencies=[Depends(verify_api_key)])
def delete_car(car_id: int, db: Session = Depends(get_db)):
    deleted = crud.delete_car(db, car_id)
    if not deleted:
        raise HTTPException(status_code=404, detail="Car not found")
    return {"message": "Car deleted successfully"}
