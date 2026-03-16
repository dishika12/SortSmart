import pandas as pd

from app.database import SessionLocal
from app.models import BinType, Item, Synonym


def import_bin_types(session):
    df = pd.read_csv("../data/bin_types.csv")

    for _, row in df.iterrows():
        existing = session.query(BinType).filter_by(bin_type_id=row["bin_type_id"]).first()
        if not existing:
            session.add(
                BinType(
                    bin_type_id=int(row["bin_type_id"]),
                    bin_name=row["bin_name"],
                    color=row["color"],
                    description=row["description"],
                )
            )

    session.commit()


def import_items(session):
    df = pd.read_csv("../data/items.csv")

    for _, row in df.iterrows():
        existing = session.query(Item).filter_by(item_id=row["item_id"]).first()
        if not existing:
            notes_value = row["notes"] if pd.notna(row["notes"]) else None

            session.add(
                Item(
                    item_id=int(row["item_id"]),
                    canonical_name=row["canonical_name"],
                    bin_type_id=int(row["bin_type_id"]),
                    explanation=row["explanation"],
                    notes=notes_value,
                )
            )

    session.commit()


def import_synonyms(session):
    df = pd.read_csv("../data/synonyms.csv")

    for _, row in df.iterrows():
        existing = session.query(Synonym).filter_by(synonym_id=row["synonym_id"]).first()
        if not existing:
            session.add(
                Synonym(
                    synonym_id=int(row["synonym_id"]),
                    item_id=int(row["item_id"]),
                    synonym_text=row["synonym_text"],
                )
            )

    session.commit()


def main():
    session = SessionLocal()

    try:
        import_bin_types(session)
        import_items(session)
        import_synonyms(session)
        print("CSV data imported successfully.")
    finally:
        session.close()


if __name__ == "__main__":
    main()