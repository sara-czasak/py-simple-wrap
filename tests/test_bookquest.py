
from bookquest import (
    get_month_labels,
    get_monthly_totals,
    load_data,
    save_data,
)


def test_monthly_totals():
    """Count completed books by month and exclude unfinished books."""
    data = {
        "books": [
            {"title": "Book A", "status": "completed", "finish_date": "2026-10-05"},
            {"title": "Book B", "status": "completed", "finish_date": "2026-10-18"},
            {"title": "Book C", "status": "completed", "finish_date": "2026-09-20"},
            {"title": "Book D", "status": "reading", "finish_date": None},
        ]
    }

    result = get_monthly_totals(data)

    assert result == {"2026-10": 2, "2026-09": 1}


def test_monthly_totals_with_no_books():
    """Return an empty dictionary when there are no books."""
    assert get_monthly_totals({"books": []}) == {}


def test_monthly_totals_with_no_completed_books():
    """Return no monthly totals when no books have finish dates."""
    data = {
        "books": [
            {"title": "Book A", "status": "reading", "finish_date": None},
            {"title": "Book B", "status": "reading", "finish_date": None},
        ]
    }

    assert get_monthly_totals(data) == {}


def test_monthly_totals_counts_multiple_books_in_same_month():
    """Combine all completed books finished in the same month."""
    data = {
        "books": [
            {"title": "Book A", "finish_date": "2026-10-01"},
            {"title": "Book B", "finish_date": "2026-10-15"},
            {"title": "Book C", "finish_date": "2026-10-30"},
        ]
    }

    assert get_monthly_totals(data) == {"2026-10": 3}


def test_save_and_load_books(tmp_path, monkeypatch):
    """Preserve book records and the monthly goal across a save/load cycle."""
    monkeypatch.chdir(tmp_path)

    data = load_data()
    data["monthly_goal"] = 5
    data["books"].append(
        {
            "title": "Learning Python",
            "author": "Example Author",
            "start_date": "2026-10-01",
            "finish_date": None,
            "status": "reading",
        }
    )

    save_data(data)
    loaded_data = load_data()

    assert loaded_data["monthly_goal"] == 5
    assert len(loaded_data["books"]) == 1
    assert loaded_data["books"][0]["title"] == "Learning Python"
    assert loaded_data["books"][0]["author"] == "Example Author"
    assert loaded_data["books"][0]["status"] == "reading"


def test_load_data_creates_default_data(tmp_path, monkeypatch):
    """Create default data when books.json does not exist."""
    monkeypatch.chdir(tmp_path)

    data = load_data()

    assert data == {"monthly_goal": 4, "books": []}
    assert (tmp_path / "books.json").exists()


def test_get_month_labels_across_year_boundary():
    """Generate consecutive month labels across December and January."""
    result = get_month_labels("2026-11", "2027-02")

    assert result == [
        "2026-11",
        "2026-12",
        "2027-01",
        "2027-02",
    ]


def test_get_month_labels_for_one_month():
    """Return one label when the start and end months are identical."""
    assert get_month_labels("2026-10", "2026-10") == ["2026-10"]
