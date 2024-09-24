from fastapi import FastAPI,Response,status,HTTPException,Depends,APIRouter
from .. import schemas,models
from sqlalchemy.orm import Session
from sqlalchemy import func
from ..database import get_db
from typing import List,Optional
from .. import oauth2
from . import vote

router = APIRouter(prefix="/posts",tags=['Posts'])


# @router.get("/",response_model=List[schemas.Post])
@router.get("/",response_model=List[schemas.PostOut])
def get_posts(db: Session = Depends(get_db),current_user: int = Depends(oauth2.get_current_user),limit: int = 10,skip: int = 0,search: Optional[str] = ""):
    # cursor.execute(""" SELECT * FROM posts""")
    # posts = cursor.fetchall()
    # print(current_user.email)
    # posts = db.query(models.Post).filter(models.Post.owner_id == current_user).all()  ## if we want to get all posts for respective users only
    # posts = db.query(models.Post).filter(models.Post.title.contains(search)).limit(limit=limit).offset(offset=skip).all() # this is not case insensitive

    # posts = db.query(models.Post).filter(models.Post.title.ilike(f"%{search}%")).limit(limit=limit).offset(offset=skip).all() # this is case insensitive 
    # results = db.query(models.Post,func.count(models.Vote.post_id).label("votes")).join(models.Vote,models.Vote.post_id == models.Post.id,isouter=True).group_by(models.Post.id).all()

    results = db.query(models.Post,func.count(models.Vote.post_id).label("votes")).join(models.Vote, models.Vote.post_id == models.Post.id, isouter=True).filter(models.Post.title.ilike(f"%{search}%")).group_by(models.Post.id).limit(limit=limit).offset(skip).all()
    # print(results)

    response = [
        {"Post": post, "votes": votes} for post, votes in results
    ]
    
    return response
    # return results

@router.post("/",status_code=status.HTTP_201_CREATED,response_model=schemas.Post)
def create_posts(post: schemas.PostCreate,db: Session = Depends(get_db),current_user: int = Depends(oauth2.get_current_user)):
    # cursor.execute("""INSERT INTO posts (title,content,published) VALUES (%s,%s,%s) RETURNING * """,
    #                (post.title,post.content,post.published))
    # new_post = cursor.fetchone()
    # conn.commit()
    # print(post.model_dump())
    # if user_id:
    # print(user_id)
    new_post = models.Post(owner_id = current_user.id, **post.model_dump())
    db.add(new_post)
    db.commit()
    db.refresh(new_post)

    return new_post
    # else:
    #     raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,detail=f"unauthorized can't post")
    

@router.get("/{id}",response_model=schemas.PostOut)
def get_post(id: int,response: Response,db: Session = Depends(get_db),current_user: int = Depends(oauth2.get_current_user)):
    # cursor.execute(""" SELECT * FROM posts WHERE id = %s""",(id,))
    # post = cursor.fetchone()

    post = db.query(models.Post).filter(models.Post.id == id).first()
    results = db.query(models.Post,func.count(models.Vote.post_id).label("votes")).join(models.Vote,models.Vote.post_id == models.Post.id,isouter=True).filter(models.Post.id ==id).group_by(models.Post.id).first()

    print(results)
    if not results:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"post with id: {id} was not found")
       
    return results


## deleting a post
@router.delete("/{id}",status_code=status.HTTP_204_NO_CONTENT)
def delete_post(id:int,response:Response,db: Session = Depends(get_db),current_user: int = Depends(oauth2.get_current_user)):
    # cursor.execute(""" DELETE FROM posts WHERE id = %s RETURNING *""",(id,))
    # deleted_post = cursor.fetchone()
    # conn.commit()
    post = db.query(models.Post).filter(models.Post.id == id)



    if post.first() == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail=f"post with id: {id} not found")
    
    if post.first().owner_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,detail=f"Not authorized to perform requested action")

    post.delete(synchronize_session=False)
    db.commit()
    # return {"message":f"Post deleted successfully with id : {id}"}
    return Response(status_code=status.HTTP_204_NO_CONTENT)


## updating a post
@router.put("/{id}",response_model=schemas.Post)
def update_post(id:int,response:Response,post:schemas.PostCreate,db: Session = Depends(get_db),current_user: int = Depends(oauth2.get_current_user)):
    # cursor.execute(""" UPDATE posts SET title= %s, content = %s, published = %s WHERE id = %s RETURNING *""",(post.title,post.content,post.published,id,))
    # updated_post = cursor.fetchone()
    # conn.commit()
    post_query = db.query(models.Post).filter(models.Post.id == id)
    posts = post_query.first()
    if posts == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail=f"post with id: {id} not found")
    
    if posts.owner_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,detail=f'Not authorized to perform requested action')

    post_query.update(post.model_dump(),synchronize_session=False)

    # post_query.update({'title':'this is updated title',
    #                    'content':'this is the updated content'},synchronize_session=False)
    
    db.commit()
    return post_query.first()