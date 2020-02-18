from app import db, models, system
from werkzeug import generate_password_hash
from firebase_admin import firestore
import os, config, csv

def upsert(model, item):
    existing_item = model.query.get(item.id)
    if existing_item:
        existing_item = item
    else:
        db.session.add(item)

def create_admins():
    admin_user = models.User(
        id="9001",
        password=generate_password_hash("admin"),
        role="admin"
    )
    student_user = models.User(
        id="9003",
        password=generate_password_hash("student"),
        role="student"
    )

    upsert(models.User, admin_user)
    upsert(models.User, student_user)
    db.session.commit()

    system.create_admin_documents("9001")
    system.create_admin_documents("9003")
    

if __name__ == "__main__":
    create_admins()
    print("done")
