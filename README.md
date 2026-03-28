# Content Monitoring & Flagging System

A Django REST Framework project for monitoring content and flagging keywords with scoring and suppression logic.

## Setup Instructions

1.  **Clone the repository** (or navigate to the project folder).
2.  **Create a virtual environment**:
    ```bash
    python -m venv venv
    source venv/bin/activate  # On Windows: .\venv\Scripts\activate
    ```
3.  **Install dependencies**:
    ```bash
    pip install django djangorestframework django-filter
    ```
4.  **Run migrations**:
    ```bash
    python manage.py migrate
    ```
5.  **Seed sample data**:
    ```bash
    python manage.py seed_data
    ```
6.  **Run the development server**:
    ```bash
    python manage.py runserver
    ```

## API Endpoints

### Keywords
- `POST /api/keywords/`: Create a new keyword.
  ```json
  { "name": "Django" }
  ```
- `GET /api/keywords/`: List all keywords.

### Content Items (Use Django Admin to add more)
- `GET /admin/`: Manage content items at `http://127.0.0.1:8000/admin/` (Create a superuser first).

### Flags
- `GET /api/flags/`: List all flags.
  - Optional filter: `GET /api/flags/?status=pending`
- `PATCH /api/flags/{id}/`: Update flag status and review date.
  ```json
  {
    "status": "irrelevant",
    "last_reviewed_at": "2026-03-28T20:00:00Z"
  }
  ```

### Scan
- `POST /api/scan/`: Trigger a scan of all content items against all keywords.

## Logic Implementation

### Scoring
- **100**: Exact keyword match in `ContentItem.title`.
- **70**: Partial keyword match in `ContentItem.title`.
- **40**: Keyword found in `ContentItem.body`.
- All matches are case-insensitive.

### Suppression
- If a flag is marked **"irrelevant"**, it is NOT updated/recreated during a scan.
- **Exception**: If the `ContentItem.last_updated` is newer than the `Flag.last_reviewed_at`, the flag will be re-evaluated and reset to "pending".

## Bonus Features
- **Logging**: Scan results are logged to the console.
- **Filtering**: Flags can be filtered by status via API.
- **Admin**: Full Django Admin support for Keywords, ContentItems, and Flags.
