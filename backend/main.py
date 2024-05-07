from fastapi import FastAPI, Depends
import models
from database import engine, get_db
from routers import user,item,category,auth,qa,user_rating

app = FastAPI()

models.Base.metadata.create_all(engine)

app.include_router(user.router)
app.include_router(item.router)
app.include_router(category.router)
app.include_router(auth.router)
app.include_router(qa.router)
app.include_router(user_rating.router)