from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import String, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship
from typing import List

db = SQLAlchemy()

# Tabla de asociación para User <-> User (followers)
# Ahora Follower será esta tabla de asociación
# class Follower(db.Model): ... (ver más abajo la forma más común)

class User(db.Model):
    _tablename_= "user"
    
    id: Mapped[int] = mapped_column(primary_key=True)
    username: Mapped[str] = mapped_column(String(120), unique=True, nullable=False)
    firstname: Mapped[str] = mapped_column(String(120), nullable=False)
    lastname: Mapped[str] = mapped_column(String(120), nullable=False)
    email: Mapped[str] = mapped_column(String(120), unique=True, nullable=False)

    # Asociacion con tablas
    follower: Mapped[List["Follower"]]= relationship(back_populates = "from_id")
    posts: Mapped[List["Post"]] = relationship(back_populates = "user")
    comentarios: Mapped[List["Comment"]] = relationship(back_populates = "usuario")

    def serialize(self):
        return {
            "id": self.id,
            "email": self.email,
            "username": self.username,
            "firstname": self.firstname,
            "lastname": self.lastname
            # do not serialize the password, its a security breach
        }

# Follower como tabla de asociación para una relación muchos-a-muchos entre Usuarios
class Follower(db.Model):
    __tablename__ = "follower"
    
    user_from_id: Mapped[int] = mapped_column(primary_key=True)
    user_to_id: Mapped[int] = mapped_column(ForeignKey("user.id"))

    # asociacion con tablas
    from_id: Mapped["User"]= relationship(back_populates = "follower")


class Post(db.Model):
    __tablename__ = "post"

    id:Mapped[int]= mapped_column(primary_key = True)
    user_id: Mapped[int] = mapped_column(ForeignKey("user.id"))

    # asociacion con tablas
    user: Mapped["User"]= relationship(back_populates = "posts")
    media: Mapped[List["Media"]] = relationship(back_populates = "type_post")
    comentarios: Mapped[List["Comment"]] = relationship(back_populates = "post")

class Comment(db.Model):
    __tableame__ = "comment"

    id : Mapped[int] = mapped_column(primary_key = True)
    post_id: Mapped[int] = mapped_column(ForeignKey("post.id"))
    comment_text: Mapped[str] = mapped_column(String(250), nullable = False)
    author_id : Mapped[int] = mapped_column(ForeignKey("user.id"))

    # asociacion con tablas
    post: Mapped["Post"] = relationship(back_populates="comentarios")
    usuario: Mapped["User"] = relationship(back_populates = "comentarios")

class Media(db.Model): 
    __tablename__ = "media"

    id : Mapped[int] = mapped_column(primary_key = True)
    type_media: Mapped[enumerate] = mapped_column(String(255), nullable = False)
    url: Mapped[str] = mapped_column(String(255), nullable = False)
    post_id: Mapped[int] = mapped_column(ForeignKey("post.id"))

    # asociacion con tablas
    type_post: Mapped["Post"] = relationship(back_populates = "media")