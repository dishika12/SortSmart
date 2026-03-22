# SortSmart

SortSmart is a full-stack web application that helps users determine the correct waste bin for an item using a manually curated UBC-inspired sorting dataset.

The goal of the project is simple: a user types an item, and the app tells them which bin it belongs in, along with a short explanation and any useful disposal notes.

---

## Features

- Search for an item from the frontend UI
- Match against canonical item names stored in PostgreSQL
- Support alternate names through a synonyms table
- Use fuzzy matching for misspelled or approximate searches
- Return the correct waste category
- Show an explanation and additional notes in the UI
- Full-stack architecture with React frontend and FastAPI backend

---

## Current Bin Categories

The current dataset supports these four waste categories which are found in UBC bins:

- Food Scraps
- Containers
- Paper
- Garbage

---

## Tech Stack

### Frontend
- React
- Vite
- CSS

### Backend
- FastAPI
- SQLAlchemy
- Python
- python-dotenv
- RapidFuzz

### Database
- PostgreSQL

### Data Source
- Manually curated CSV files

---

## How It Works

When a user searches for an item, the backend follows this order:

1. Normalize the input by trimming spaces and converting to lowercase
2. Search for an exact match in `items.canonical_name`
3. If not found, search for an exact match in `synonyms.synonym_text`
4. If still not found, perform fuzzy matching using RapidFuzz
5. Return the matched item, bin type, explanation, and notes

This allows the app to handle:

- exact queries
- alternate names
- small spelling mistakes
- approximate user input

---

## Database Design

The backend currently uses three main tables:

### `BinType`
Stores the waste categories.

### `Item`
Stores canonical item names, their associated bin type, explanation, and notes.

### `Synonym`
Stores alternate search terms linked to items.

### Relationships
- one `BinType` has many `Item`s
- one `Item` belongs to one `BinType`
- one `Item` has many `Synonym`s
- one `Synonym` belongs to one `Item`

---

## Dataset

The app uses manually created CSV files inside the `data/` folder:

- `bin_types.csv` → waste categories
- `items.csv` → canonical item names, explanations, notes, and bin assignments
- `synonyms.csv` → alternate names for searchable items

These CSV files are imported into PostgreSQL using the backend import script.

---

## Why This Project Matters

Waste sorting can be confusing, especially when users are unsure whether an item belongs in compost, recycling, paper, or garbage. SortSmart makes that decision faster and easier by combining a searchable interface with a structured waste-sorting dataset.

This project demonstrates:

- full-stack web development
- database design and relational modeling
- API development with FastAPI
- frontend-backend integration
- practical search design with exact, synonym, and fuzzy matching

---

## Future Improvements

Planned improvements include:

- deployment to a public hosting platform
- Docker support for easier setup
- autocomplete suggestions
- search history or recent items
- bookmarked common items
- improved UI polish and responsiveness
- campus-specific bin location support
- analytics for common search queries and failed lookups

---
