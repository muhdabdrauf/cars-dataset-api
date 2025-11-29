from sqlalchemy.orm import Session, joinedload
from sqlalchemy import asc, desc, func, or_
from app.models import Car, Model, Brand, Color
from app.schemas import CarCreate


def get_all_cars(
    db: Session,
    page: int = 1,
    page_size: int = 25,
    sort: str = "car_id:asc",
    brand_id: int | None = None,
    model_id: int | None = None,
    color_id: int | None = None,
    q: str | None = None,
):
    # Pagination calculations
    offset = (page - 1) * page_size
    query = db.query(Car).join(Model).join(Brand).join(Color)

    #Filtering
    if brand_id:
        query = query.filter(Brand.brand_id == brand_id)
    if brand_id:
        query = query.filter(Model.model_id == model_id)
    if color_id:
        query = query.filter(Color.color_id == color_id)

    #Search
    if q:
        search = f"%{q.lower()}%"
        query = query.filter(
            or_(
                func.lower(Brand.brand_name).like(search),
                func.lower(Model.model_name).like(search)
            )
        )

    # Handle multi-field sorting
    sort_fields = [s.strip() for s in sort.split(",") if s.strip()]
    for field in sort_fields:
        if ":" in field:
            field_name, order = field.split(":")
            order = order.lower()
        else:
            field_name, order = field, "asc"

        # Ensure the field exists in the Car model
        if hasattr(Car, field_name):
            column = getattr(Car, field_name)
            query = query.order_by(desc(column) if order == "desc" else asc(column))

    #get total count before pagination
    total = query.count()

    # Apply pagination
    query = query.offset(offset).limit(page_size)
    items = query.options(joinedload(Car.model).joinedload(Model.brand)).all()
    return {
        "items": items,
        "page": page,
        "page_size": page_size,
        "total": total
    }


def get_car_by_id(db: Session, car_id: int):
    return db.query(Car).filter(Car.car_id == car_id).first()


def create_car(db: Session, car_data: CarCreate):
    car = Car(**car_data.dict())
    db.add(car)
    db.commit()
    db.refresh(car)
    return car


def delete_car(db: Session, car_id: int):
    car = db.query(Car).filter(Car.car_id == car_id).first()
    if car:
        db.delete(car)
        db.commit()
        return True
    return False
