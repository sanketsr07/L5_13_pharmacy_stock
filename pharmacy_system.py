
"""Manage pharmacy stock, patient allergies, and prescriptions."""

import json
import sqlite3
from datetime import datetime

# Global state
conn = sqlite3.connect(":memory:")
stock = {}
prescriptions = []


def setup_database():
    """Create the patient database and insert sample records."""
    cur = conn.cursor()
    cur.execute(
        "CREATE TABLE patients (id TEXT, name TEXT, allergy TEXT)"
    )
    cur.execute(
        "INSERT INTO patients VALUES (?, ?, ?)",
        ("P1", "Kavya", "penicillin"),
    )
    cur.execute(
        "INSERT INTO patients VALUES (?, ?, ?)",
        ("P2", "Arjun", "none"),
    )
    cur.execute(
        "INSERT INTO patients VALUES (?, ?, ?)",
        ("P3", "Meena", "ibuprofen"),
    )
    conn.commit()


def find_patient(name):
    """Return the ID and allergy information for a patient."""
    cur = conn.cursor()
    query = "SELECT id, allergy FROM patients WHERE name = ?"
    return cur.execute(query, (name,)).fetchall()


def add_stock(drug, units, expiry, batch_log=None):
    """Add units of a drug and optionally record the batch."""
    if batch_log is None:
        batch_log = []

    current_units = stock.get(drug, {}).get("units", 0)
    stock[drug] = {
        "units": current_units + units,
        "expiry": expiry,
    }
    batch_log.append((drug, units))
    return len(batch_log)


def dispense(patient_name, drug, units):
    """Dispense medicine if the patient has no matching allergy."""
    try:
        patients = find_patient(patient_name)
        if not patients:
            return False

        patient = patients[0]

        if drug.lower() in patient[1].lower():
            print("Allergy warning for", patient_name)
            return False

        if drug not in stock or stock[drug]["units"] < units:
            return False

        stock[drug]["units"] -= units
        prescriptions.append(
            {
                "patient": patient[0],
                "drug": drug,
                "units": units,
                "time": str(datetime.now()),
            }
        )
        return True
    except (sqlite3.Error, KeyError, TypeError, ValueError):
        return False


def expiring_soon(days=30):
    """Return drugs expiring within the specified number of days."""
    soon = []

    for drug, details in stock.items():
        expiry = datetime.strptime(details["expiry"], "%Y-%m-%d")
        remaining_days = (expiry - datetime.now()).days

        if 0 <= remaining_days < days:
            soon.append(drug)

    return soon


def export_prescriptions(file="prescriptions.json"):
    """Write prescription records to a JSON file."""
    with open(file, "w", encoding="utf-8") as output_file:
        json.dump(prescriptions, output_file, indent=4)


def load_stock(file="stock.json"):
    """Load stock records from a JSON file when available."""

    try:
        with open(file, "r", encoding="utf-8") as input_file:
            loaded_stock = json.load(input_file)

        if isinstance(loaded_stock, dict):
            stock.update(loaded_stock)
    except FileNotFoundError:
        return
    except (json.JSONDecodeError, OSError, TypeError):
        return


def print_stock():
    """Print the current pharmacy stock."""
    print("Pharmacy Stock")

    for drug, details in stock.items():
        print(
            drug,
            "->",
            details["units"],
            "units, expires",
            details["expiry"],
        )


def main():
    """Run the pharmacy demonstration."""
    setup_database()
    load_stock()

    add_stock("Paracetamol", 100, "2027-03-01")
    add_stock("Amoxicillin", 20, "2025-12-31")
    add_stock("Penicillin", 50, "2027-01-15")
    add_stock("Ibuprofen", -15, "2026-11-30")

    print(
        "Arjun gets Amoxicillin:",
        dispense("Arjun", "Amoxicillin", 30),
    )
    print(
        "Kavya gets Penicillin:",
        dispense("Kavya", "Penicillin", 10),
    )
    print(
        "Meena gets ibuprofen:",
        dispense("Meena", "ibuprofen", 2),
    )
    print("Unknown patient:", dispense("Ghost", "Paracetamol", 5))

    name = input(
        "Patient name to look up (Enter for Arjun): "
    ) or "Arjun"

    print("Lookup result:", find_patient(name))
    print("Expiring within 30 days:", expiring_soon())
    export_prescriptions()
    print_stock()


if __name__ == "__main__":
    main()
