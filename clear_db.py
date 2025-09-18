from app import app, db, Click   # import both app and db

with app.app_context():          # now use the Flask app's context
    db.session.query(Click).delete()
    db.session.commit()
    print("✅ All click records deleted!")

