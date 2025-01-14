#!/usr/bin/python3
""" Place Module for HBNB project """
import os
from sqlalchemy import Column, String, Integer, Float, Table, ForeignKey
from sqlalchemy.orm import relationship
from models.base_model import BaseModel, Base

place_amenity = Table(
    'place_amenity',
    Base.metadata,
    Column(
        'place_id', String(60), ForeignKey('places.id'), primary_key=True
        ),
    Column(
        'amenity_id', String(60), ForeignKey('amenities.id'), primary_key=True
        ),
    extend_existing=True
)


class Place(BaseModel, Base):
    """Class representing the Place table"""
    __tablename__ = 'places'

    city_id = Column(String(60), ForeignKey('cities.id'), nullable=False)
    user_id = Column(String(60), ForeignKey('users.id'), nullable=False)
    amenity_id = []
    name = Column(String(128), nullable=False)
    description = Column(String(1024))
    number_rooms = Column(Integer, nullable=False, default=0)
    number_bathrooms = Column(Integer, nullable=False, default=0)
    max_guest = Column(Integer, nullable=False, default=0)
    price_by_night = Column(Integer, nullable=False, default=0)
    latitude = Column(Float)
    longitude = Column(Float)

    if os.getenv('HBNB_TYPE_STORAGE') == 'db':
        reviews = relationship("Review",
                               backref="place",
                               cascade="all, delete")
        amenities = relationship(
            "Amenity",
            secondary=place_amenity,
            back_populates="places_amenities",
            viewonly=False
            )
    else:
        @property
        def reviews(self):
            from models import storage
            from models.review import Review
            review_list = []
            for review in storage.all(Review).values():
                if review.place_id == self.id:
                    review_list.append(review)
            return review_list

        @property
        def amenities(self):
            from models import storage
            from models.amenity import Amenity
            amenity_list = []
            for amenity_id in self.amenity_id:
                amenity = storage.get(Amenity, amenity_id)
                if amenity:
                    amenity_list.append(amenity)
            return amenity_list

        @amenities.setter
        def amenities(self, obj):
            from models.amenity import Amenity
            if isinstance(obj, Amenity):
                self.amenity_ids.append(obj.id)
