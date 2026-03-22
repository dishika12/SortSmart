from sqlalchemy import Column, ForeignKey, Integer, String, Text
from sqlalchemy.orm import relationship

from app.database import Base

class BinType(Base):
    __tablename__ = "bin_types"

    bin_type_id = Column(Integer, primary_key=True, index=True)
    bin_name = Column(String, nullable=False, unique=True)
    color = Column(String, nullable=False)
    description = Column(Text)

    items = relationship("Item", back_populates="bin_type")


class Item(Base):
    __tablename__ = "items"

    item_id = Column(Integer, primary_key=True, index=True)
    canonical_name = Column(String, nullable=False, unique=True, index=True)
    bin_type_id = Column(Integer, ForeignKey("bin_types.bin_type_id"), nullable=False)
    explanation = Column(Text, nullable=False)
    notes = Column(Text)

    bin_type = relationship("BinType", back_populates="items")
    synonyms = relationship("Synonym", back_populates="item")


class Synonym(Base):
    __tablename__ = "synonyms"

    synonym_id = Column(Integer, primary_key=True, index=True)
    item_id = Column(Integer, ForeignKey("items.item_id"), nullable=False)
    synonym_text = Column(String, nullable=False, index=True)

    item = relationship("Item", back_populates="synonyms")