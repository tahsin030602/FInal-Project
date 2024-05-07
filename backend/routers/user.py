from fastapi import APIRouter, Depends,status,HTTPException,Response
from typing import List
from passlib.context import CryptContext
from sqlalchemy import desc
from respository import user
from sqlalchemy.orm import Session
import schemas,database,models
import oauth2
from hashing import Hash

router = APIRouter(
    prefix='/user',
    tags=['user']
)

@router.post('/create',status_code=status.HTTP_201_CREATED)
def create_user(request : schemas.User,db: Session = Depends(database.get_db)):
    new_user =  user.create_user(request,db)
    if not new_user:
        raise HTTPException(status_code=status.HTTP_204_NO_CONTENT,detail=f'User not created')
    else:
        return 'created'

@router.post('/list_add',status_code=status.HTTP_201_CREATED)
def create_user(request : schemas.Address,db: Session = Depends(database.get_db),current_user = Depends(oauth2.getCurrentUser)):
    new_add =  user.list_add(request,db,current_user.user_id)
    if not new_add:
        raise HTTPException(status_code=status.HTTP_204_NO_CONTENT,detail=f'User not created')
    else:
        return 'listed'
    
@router.get('/items',response_model=List[schemas.itemShow],status_code=status.HTTP_302_FOUND)
def my_item(db: Session = Depends(database.get_db),current_user = Depends(oauth2.getCurrentUser)):
   items = db.query(models.Item)\
              .filter(models.Item.seller_id == current_user.user_id)\
              .order_by(desc(models.Item.auction_end_date))\
              .all()
   if items:
       return items
   else:
       raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail='You have listed no item yet')


