from sqlalchemy import Column,Integer,String,create_engine,Date
from fastapi import FastAPI,status,HTTPException,Depends
from pydantic import BaseModel
from sqlalchemy.orm import declarative_base,sessionmaker,Session
from datetime import date
from typing import Optional

#create app
app = FastAPI()

engine = create_engine("sqlite:///./service_center.db",echo=True)
Base = declarative_base()
SessionLocal = sessionmaker(autocommit=False,bind=engine)

#create db
class ServiceBooking(Base):
    __tablename__ = "service_booking"
    id = Column(Integer,primary_key=True,index=True)
    customer_name = Column(String,nullable=False)
    vehicle_name = Column(String,nullable=False)
    service_type = Column(String,nullable=False)
    booking_date = Column(Date, nullable=False)

Base.metadata.create_all(bind=engine)

#pydantic model
class ServiceBookingCreate(BaseModel):
    customer_name :str
    vehicle_name : str
    service_type :str
    booking_date :date

class serviceBookingUpdate(BaseModel):
    customer_name : Optional[str] = None
    vehicle_name : Optional[str] = None
    service_type :Optional[str] = None
    booking_date :Optional[date] = None

# class ServiceBookingUpdate(BaseModel):
#     customer_name : 
#     vehicle_name : str
#     service_type :str
#     booking_date :date

class Config:
    orm_mode = True 


#dependency 
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.post("/bookings/")
def create_booking(booking: ServiceBookingCreate, db: Session = Depends(get_db)):
    # Validate booking date
    if booking.booking_date < date.today():
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Booking date cannot be in the past."
        )
    new_booking = ServiceBooking(**booking.dict())
    db.add(new_booking)
    db.commit()
    db.refresh(new_booking)
    return new_booking


@app.get("/bookings/get-all/")
def get_all_bookings(db: Session = Depends(get_db)):
    bookings = db.query(ServiceBooking).all()
    return bookings

@app.get("/bookings/{booking_id}")
def get_booking_by_id(booking_id: int, db: Session = Depends(get_db)):
    booking = db.query(ServiceBooking).filter(ServiceBooking.id == booking_id).first()
    if not booking:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Booking not found."
        )
    return booking

@app.put("/bookings/{booking_id}")
def update_booking(booking_id: int, updated_booking: serviceBookingUpdate, db: Session = Depends(get_db)):
    booking = db.query(ServiceBooking).filter(ServiceBooking.id == booking_id).first()
    if not booking:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Booking not found."
        )
    # Validate booking date
    if updated_booking.booking_date is not None and updated_booking.booking_date < date.today():
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Booking date cannot be in the past."
        )
    if updated_booking.customer_name is not None:
        booking.customer_name = updated_booking.customer_name
    if updated_booking.vehicle_name is not None:
        booking.vehicle_name = updated_booking.vehicle_name 
    if updated_booking.service_type is not None:
        booking.service_type = updated_booking.service_type
    if updated_booking.booking_date is not None:
        booking.booking_date = updated_booking.booking_date

    db.commit()
    db.refresh(booking)
    return booking