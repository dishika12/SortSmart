from fastapi import Depends, FastAPI, HTTPException, Query
from fastapi.middleware.cors import CORSMiddleware
from rapidfuzz import fuzz, process
from sqlalchemy.orm import Session

from app import models
from app.database import Base, engine, get_db

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173", "http://127.0.0.1:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

Base.metadata.create_all(bind=engine)

FUZZY_THRESHOLD = 75 

@app.get("/")
def root():
    return {"message": "Backend is working"}


@app.get("/search")
def search_item(q: str = Query(..., min_length=1), db: Session = Depends(get_db)):
    search_term = q.strip().lower()

    # Exact canonical name match
    item = (
        db.query(models.Item)
        .filter(models.Item.canonical_name.ilike(search_term))
        .first()
    )

    # Exact synonym match
    if not item:
        synonym = (
            db.query(models.Synonym)
            .filter(models.Synonym.synonym_text.ilike(search_term))
            .first()
        )
        if synonym:
            item = db.query(models.Item).filter(models.Item.item_id == synonym.item_id).first()

    # Fuzzy match against canonical names and synonyms
    fuzzy_used = False
    if not item:
        all_items = db.query(models.Item).all()
        all_synonyms = db.query(models.Synonym).all()

        # Build a lookup: display string -> Item object
        candidates: dict[str, models.Item] = {}
        for i in all_items:
            candidates[i.canonical_name.lower()] = i
        for s in all_synonyms:
            syn_item = db.query(models.Item).filter(models.Item.item_id == s.item_id).first()
            if syn_item:
                candidates[s.synonym_text.lower()] = syn_item

        # Find best fuzzy match
        match = process.extractOne(
            search_term,
            candidates.keys(),
            scorer=fuzz.WRatio,  # handles typos, partial matches, word reordering
            score_cutoff=FUZZY_THRESHOLD,
        )

        if match:
            matched_key, score, _ = match
            item = candidates[matched_key]
            fuzzy_used = True

    if not item:
        raise HTTPException(status_code=404, detail="Item not found")

    bin_type = (
        db.query(models.BinType)
        .filter(models.BinType.bin_type_id == item.bin_type_id)
        .first()
    )

    return {
        "item_id": item.item_id,
        "canonical_name": item.canonical_name,
        "matched_by": "fuzzy" if fuzzy_used else "exact",  # useful for frontend UX
        "bin_type": {
            "bin_type_id": bin_type.bin_type_id,
            "bin_name": bin_type.bin_name,
            "color": bin_type.color,
            "description": bin_type.description,
        },
        "explanation": item.explanation,
        "notes": item.notes,
    }