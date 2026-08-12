"""
One-time bootstrap script to promote a user to admin.

Use this to create the very first admin account -- there's no other way in,
since every admin-management endpoint (PATCH /api/v1/admin/users/{id}/role)
requires you to already be an admin. Run this once, directly against
Firestore, then use the app's admin endpoints/UI from then on.

Usage:
    python scripts/bootstrap_admin.py --email you@example.com --project hive-investor --database hiveinvestor
"""
import argparse
from google.cloud import firestore


def main():
    parser = argparse.ArgumentParser(description="Promote a user to admin.")
    parser.add_argument("--email", required=True, help="Email of the user to promote")
    parser.add_argument("--project", required=True, help="GCP project ID")
    parser.add_argument("--database", default="hiveinvestor", help="Firestore database name")
    args = parser.parse_args()

    db = firestore.Client(project=args.project, database=args.database)

    normalized_email = args.email.strip().lower()
    users_ref = db.collection("users")
    matches = list(users_ref.where("email", "==", args.email).stream())

    if not matches:
        print(f"No user found with email {args.email}. They must register first.")
        return

    if len(matches) > 1:
        print(f"WARNING: multiple users found with email {args.email}, promoting all of them.")

    for doc in matches:
        doc.reference.update({"role": "admin"})
        print(f"Promoted {args.email} (user_id={doc.id}) to admin.")


if __name__ == "__main__":
    main()
