# app/Models.py


from sqlalchemy import Column, Integer, String, ForeignKey, DECIMAL, CheckConstraint, DATE, Time, UniqueConstraint

from sqlalchemy.sql.expression import text
from sqlalchemy.sql.sqltypes import TIMESTAMP
from .database import Base
from sqlalchemy.orm import relationship




class Bookings(Base):

    __tablename__ = "bookings"

    __table_args__ = (
        CheckConstraint("char_length(pnr) = 10", name="pnr_length_10"),
        CheckConstraint("pnr ~ '^[0-9]{10}$'", name="pnr_10_digits"),
    )

    id = Column(Integer, primary_key= True)
    pnr = Column (String(10), nullable= False, unique= True, index=True ) 
    user_id = Column(Integer, ForeignKey("users.id", ondelete="RESTRICT", onupdate="CASCADE"), nullable= False, index=True)
    train_id = Column(Integer, ForeignKey("trains.id", ondelete="RESTRICT", onupdate="CASCADE"), nullable= False) 
    source_station_id = Column(Integer, ForeignKey("stations.id", ondelete="RESTRICT", onupdate="CASCADE"), nullable= False)
    destination_station_id = Column(Integer, ForeignKey("stations.id", ondelete="RESTRICT", onupdate="CASCADE"), nullable= False)
    journey_date = Column(DATE, nullable=False, index= True)
    class_id = Column(Integer, ForeignKey("classes.id", ondelete="RESTRICT", onupdate="CASCADE"), nullable= False)
    quota = Column(String, nullable=False)
    total_fare = Column(DECIMAL(10, 2), nullable=False)
    booking_status = Column(String, nullable=False)
    created_at = Column(TIMESTAMP(timezone = True), 
                        nullable = False, server_default=text('now()'))

class Users(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True)
    name = Column(String, nullable= False)
    email = Column(String, nullable= False, unique=True, index=True)
    phone = Column(String(15), nullable= False)
    password_hash = Column(String, nullable=False)
    role = Column(String, nullable=False, default="user")
    created_at = Column(TIMESTAMP(timezone = True), 
                            nullable = False, server_default=text('now()'))


class Stations(Base):
    __tablename__ = "stations"
    id = Column(Integer, primary_key=True)
    station_code = Column(String(10), nullable= False, unique=True, index=True)
    station_name = Column(String, nullable= False)
    city = Column(String, nullable= False)
    state = Column(String, nullable= False)


class Trains(Base):
    __tablename__ = "trains"
    id = Column(Integer, primary_key=True)
    train_number = Column(String(10), nullable=False, unique=True, index=True)
    train_name = Column(String, nullable= False)
    train_type = Column(String, nullable= False)

class Classes(Base):
    __tablename__ = "classes"
    id = Column(Integer, primary_key=True)
    class_code = Column(String(10), nullable= False, unique=True)
    class_name = Column(String, nullable= False)

# class Train_routes(Base):
#     __tablename__ = "train_routes"
#     id = Column(Integer, primary_key=True)
#     train_id = Column(Integer, ForeignKey("trains.id", ondelete="RESTRICT",onupdate="CASCADE"), nullable=False)
#     station_id = Column(Integer, ForeignKey("stations.id", ondelete="RESTRICT",onupdate="CASCADE"), nullable=False)
#     stop_order = Column(Integer, nullable=False)
#     arrival_time = Column(Time)
#     departure_time = Column(Time)
#     distance_km = Column(Integer, nullable= False)
#     day_of_journey = Column(Integer, nullable= False)

class TrainRoute(Base):
    __tablename__ = "train_routes"

    __table_args__ = (
        UniqueConstraint("train_id", "station_id", name="uq_train_station"),
        UniqueConstraint("train_id", "stop_order", name="uq_train_stop_order"),
    )

    id = Column(Integer, primary_key=True)
    train_id = Column(Integer, ForeignKey("trains.id", ondelete="RESTRICT", onupdate="CASCADE"), nullable=False, index=True)
    station_id = Column(Integer, ForeignKey("stations.id", ondelete="RESTRICT", onupdate="CASCADE"), nullable=False, index=True)
    stop_order = Column(Integer, nullable=False)
    arrival_time = Column(Time)
    departure_time = Column(Time)
    distance_km = Column(Integer, nullable=False)
    day_of_journey = Column(Integer, nullable=False)


# class Train_running_days(Base):
#     __tablename__ = "train_running_days"
#     id = Column(Integer, primary_key=True)
#     train_id = Column(Integer, ForeignKey("trains.id", ondelete="RESTRICT",onupdate="CASCADE"), nullable=False)
#     weekday = Column(String, nullable=False)

class TrainRunningDay(Base):
    __tablename__ = "train_running_days"

    __table_args__ = (
        UniqueConstraint("train_id", "weekday", name="uq_train_weekday"),
    )

    id = Column(Integer, primary_key=True)
    train_id = Column(Integer, ForeignKey("trains.id", ondelete="RESTRICT", onupdate="CASCADE"), nullable=False, index=True)
    weekday = Column(String, nullable=False)

# class Coaches(Base):
#     __tablename__ = "coaches"
#     id = Column(Integer, primary_key=True)
#     train_id = Column(Integer, ForeignKey("trains.id", ondelete="RESTRICT",onupdate="CASCADE"), nullable=False)
#     class_id = Column(Integer, ForeignKey("classes.id", ondelete="RESTRICT",onupdate="CASCADE"), nullable=False)
#     coach_number = Column(String, nullable= False)
#     total_seats = Column(Integer, nullable=False)

class Coaches(Base):
    __tablename__ = "coaches"

    __table_args__ = (
        UniqueConstraint("train_id", "coach_number", name="uq_train_coach"),
    )

    id = Column(Integer, primary_key=True)
    train_id = Column(Integer, ForeignKey("trains.id", ondelete="RESTRICT", onupdate="CASCADE"), nullable=False, index=True)
    class_id = Column(Integer, ForeignKey("classes.id", ondelete="RESTRICT", onupdate="CASCADE"), nullable=False, index=True)
    coach_number = Column(String(10), nullable=False)
    total_seats = Column(Integer, nullable=False)


class SeatAvailability(Base):
    __tablename__ = "seat_availability"
    __table_args__ = (
    UniqueConstraint("train_id", "journey_date", "class_id", "quota", name="uq_seat_availability"),
)
    id = Column(Integer, primary_key=True)
    train_id = Column(Integer, ForeignKey("trains.id", ondelete="RESTRICT",onupdate="CASCADE"), nullable=False, index=True)
    journey_date = Column(DATE, nullable=False, index= True)
    class_id = Column(Integer, ForeignKey("classes.id", ondelete="RESTRICT",onupdate="CASCADE"), nullable=False, index=True)
    quota = Column(String, nullable=False)
    total_seats = Column(Integer, nullable=False)
    confirmed_available = Column(Integer, nullable=False)
    rac_available = Column(Integer, nullable=False)
    wl_available = Column(Integer, nullable=False)

# class Fare_rules(Base):
#     __tablename__ = "fare_rules"
#     id = Column(Integer, primary_key=True)
#     class_id = Column(Integer, ForeignKey("classes.id", ondelete="RESTRICT",onupdate="CASCADE"), nullable=False)
#     fare_per_km = Column(DECIMAL(10, 2), nullable=False)
#     reservation_charge = Column(DECIMAL(10, 2), nullable=False)
#     gst_percent = Column(DECIMAL(10, 2), nullable=False)
class FareRule(Base):
    __tablename__ = "fare_rules"
    id = Column(Integer, primary_key=True)
    class_id = Column(Integer, ForeignKey("classes.id", ondelete="RESTRICT", onupdate="CASCADE"), nullable=False, unique=True)
    fare_per_km = Column(DECIMAL(10, 2), nullable=False)
    reservation_charge = Column(DECIMAL(10, 2), nullable=False)
    gst_percent = Column(DECIMAL(10, 2), nullable=False)



class BookedPassengers(Base):
    __tablename__ = "booked_passengers"

    id = Column(Integer, primary_key=True)
    booking_id = Column(
        Integer,
        ForeignKey("bookings.id", ondelete="RESTRICT", onupdate="CASCADE"),
        nullable=False,
        index=True
    )
    passenger_name = Column(String, nullable=False)
    age = Column(Integer, nullable=False)
    gender = Column(String)
    berth_preference = Column(String)
    coach_number = Column(String)
    seat_number = Column(String)
    berth_type = Column(String)
    passenger_status = Column(String, nullable=False)
    wl_number = Column(Integer)


class Cancellations(Base):
    __tablename__ = "cancellations"
    id = Column(Integer, primary_key=True)
    booking_id = Column(Integer, ForeignKey("bookings.id", ondelete="RESTRICT", onupdate="CASCADE"), nullable=False, index=True)
    booked_passenger_id = Column(Integer, ForeignKey("booked_passengers.id", ondelete="RESTRICT", onupdate="CASCADE"), nullable=False, index=True)
    cancellation_time = Column(TIMESTAMP(timezone=True), nullable=False, server_default=text("now()"))
    refund_amount = Column(DECIMAL(10, 2), nullable=False)
    refund_status = Column(String, nullable=False)


# class Payments(Base):
#     __tablename__ = "payments"

#     id = Column(Integer, primary_key=True)
#     booking_id = Column(Integer, ForeignKey("bookings.id", ondelete="RESTRICT", onupdate="CASCADE"), nullable=False, index=True)
#     amount = Column(DECIMAL(10, 2), nullable=False)
#     payment_method = Column(String)
#     payment_status = Column(String, nullable=False)
#     transaction_ref = Column(String)
#     paid_at = Column(TIMESTAMP(timezone=True))
class Payments(Base):
    __tablename__ = "payments"

    id = Column(Integer, primary_key=True)
    booking_id = Column(Integer, ForeignKey("bookings.id", ondelete="RESTRICT", onupdate="CASCADE"), nullable=False, unique=True, index=True)
    amount = Column(DECIMAL(10, 2), nullable=False)
    payment_method = Column(String)
    payment_status = Column(String, nullable=False)
    transaction_ref = Column(String, unique=True)
    paid_at = Column(TIMESTAMP(timezone=True))

