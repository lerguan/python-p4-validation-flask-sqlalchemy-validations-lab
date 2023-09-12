from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import validates

db = SQLAlchemy()


class Author(db.Model):
    __tablename__ = "authors"

    # Add validations and constraints
    @validates("name")
    def validate_name(self, key, name):
        names = db.session.query(Author.name).all()
        if not name:
            raise ValueError("Invalid name value")
        elif len(names) != len(set(names)):
            raise ValueError("Name must be unique.")
        return name

    @validates("phone_number")
    def validate_phone_number(self, key, phone_number):
        if len(phone_number) != 10:
            raise ValueError("Phone number must be 10 digits.")
        return phone_number

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, unique=True, nullable=False)
    phone_number = db.Column(db.String)
    created_at = db.Column(db.DateTime, server_default=db.func.now())
    updated_at = db.Column(db.DateTime, onupdate=db.func.now())

    def __repr__(self):
        return f"Author(id={self.id}, name={self.name})"


class Post(db.Model):
    __tablename__ = "posts"

    # Add validations and constraints
    @validates("content")
    def validate_content(self, key, content):
        if len(content) < 250:
            raise ValueError("content must have at least 250 characters")
        return content

    @validates("summary")
    def validate_summary(self, key, summary):
        if len(summary) >= 250:
            raise ValueError("Summary must not be more than 250 characters")
        return summary

    @validates("category")
    def validate_category(self, key, category):
        if (category != "Fiction") and (category != "Non-Fiction"):
            raise ValueError("category must be either 'Fiction' or 'Non-Fiction'")
        return category

    @validates("title")
    def validate_title_clickbait(self, key, title):
        clickbait_list = ["Won't Believe", "Secret", "Top", "Guess"]
        for item in clickbait_list:
            if item not in title:
                raise ValueError("Title should be clickbaity")
        return title

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String, nullable=False)
    content = db.Column(db.String)
    category = db.Column(db.String)
    summary = db.Column(db.String)
    created_at = db.Column(db.DateTime, server_default=db.func.now())
    updated_at = db.Column(db.DateTime, onupdate=db.func.now())

    def __repr__(self):
        return f"Post(id={self.id}, title={self.title} content={self.content}, summary={self.summary})"
