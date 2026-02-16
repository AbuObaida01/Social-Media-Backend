from fastapi import FastAPI, Response, status, HTTPException, Depends, APIRouter
from .. import models,schemas, utils
from ..database import engine, SessionLocal, get_db
from sqlalchemy import select, func
from sqlalchemy.orm import Session
from typing import Optional, List
from .. import oauth2
router=APIRouter(
    prefix="/posts",
    tags=['Posts']
)

@router.get("/",response_model=List[schemas.ResponsePost])

async def get_posts(db:Session=Depends(get_db), limit: int=20, skip: int=0,
                    search: Optional[str]=""):
    # current_user : int  =Depends(oauth2.get_current_user),(use this to authorize the user)  
    # cursor.execute("""SELECT * from posts""")
    # my_posts = cursor.fetchall()
    # print(my_posts)

    # stmt=select(models.Post).limit(limit).offset(skip).where(models.Post.title.contains(search))  # .where(models.Post.owner_id==current_user.id) we can add this to get post only from my id
    # my_posts=db.execute(stmt).scalars().all()

    votes=select(models.Post, func.count(models.Votes.post_id).label("Votes")).outerjoin(
    models.Votes, models.Votes.post_id==models.Post.id).group_by(models.Post.id).limit(
    limit).offset(skip).where(models.Post.title.ilike(f"%{search}%"))
    total= db.execute(votes).all()
    response=[]
    for post, votes in total:
        response.append({
            "id": post.id,
            "title":post.title,
            "content":post.content,
            "created_at": post.created_at,
            "owner":post.owner,
            "votes":votes
        })
    return response
    # my_posts = db.query(models.Post).all()
    # return my_posts

# To check that is it actually working in postGre
# @router.get("/sqlalchemy")
# def test_post(db:Session=Depends(get_db)):
#     posts = db.query(models.Post).all()
#     return{"data":posts}

# TO create posts
@router.post("/", status_code=status.HTTP_201_CREATED, response_model=schemas.PostResponseCreate)
def create_posts(post: schemas.PostCreate, db:Session=Depends(get_db), current_user : int  =Depends(oauth2.get_current_user)):
    # cursor.execute(f"INSERT INTO posts(title,content,published) VALUES ({post.title}, {post.content}, {post.published})")
    
    # # This is the method to prevent SQL Injection that is caused by the above code
    # cursor.execute("""INSERT INTO posts(title,content,published) VALUES(%s,%s,%s) RETURNING * """, (post.title, post.content, post.published))
    # new_post=cursor.fetchone()
    # conn.commit()

    #Using sqlalchemy
    # new_post = models.Post(title=post.title, content=post.content, published=post.published)
    # db.add(new_post)
    # db.commit()
    # db.refresh(new_post)
    # return{"data":new_post}

    # to make it more efficient
    new_post = models.Post(owner_id=current_user.id, **post.dict())
    db.add(new_post)
    db.commit()
    db.refresh(new_post)
    return new_post

    # post_dict=post.dict()
    # post_dict['id']=randrange(0,10000)
    # my_posts.routerend(post_dict)
    # return post_dict

## to retrive latest post 
# @router.get("/posts/latest")
# async def get_latest():
#     post=my_posts[-1]
#     return post

# To retrive any specific post by id
@router.get("/{id}", response_model=schemas.ResponsePost)
async def get_post(id: int, db:Session=Depends(get_db), current_user :int=Depends(oauth2.get_current_user)):
    # cursor.execute("""SELECT * FROM posts WHERE id=%s """, (str(id),) )
    # post=cursor.fetchone()
   
    # for post in my_posts:
    #     if post['id']==id:
    #         return{"post_detail": post}

    # Using sqlalchemy
    # stmt = select(models.Post).where(models.Post.id == id)
    # post= db.execute(stmt).scalar_one_or_none()

    stmt=select(models.Post, func.count(models.Votes.post_id).label("Votes")).outerjoin(
    models.Votes, models.Votes.post_id==models.Post.id).where(models.Post.id==id).group_by(models.Post.id)
    result= db.execute(stmt).first()
 
    # post=db.query(models.Post).filter(models.Post.id== id).first()


    if not result:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"id={id} not available")
    post, votes = result
    return{
        "id": post.id,
        "title":post.title,
        "content":post.content,
        "created_at": post.created_at,
        "owner":post.owner,
        "votes":votes
    }
    # return response
    # return post


    # # We can also use HTTP Exception
    # raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Post {id} not founnd")

## using here will give wrror because it comes after another posts/{id} which will take latest also as id
# ## to retrive latest post 
# @router.get("/posts/latest")
# async def get_latest():
#     post=my_posts[-1]
#     return post

# to delete a post
@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_post(id:int, db:Session=Depends(get_db), current_user : int  =Depends(oauth2.get_current_user)):
    # cursor.execute("""DELETE FROM posts WHERE id=%s RETURNING *""", (str(id),))
    # del_post=cursor.fetchone()
    # conn.commit()
    # index=del_post(id)
    stmt=select(models.Post).where(models.Post.id == id)
    del_post=db.execute(stmt).scalar_one_or_none()



    if del_post is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Post {id} not found")
    # my_posts.pop(index)
    if del_post.owner_id!= current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Can not delete others post")
    db.delete(del_post)
    db.commit()
    return Response(status_code=status.HTTP_204_NO_CONTENT)

# to update a post
@router.put("/{id}",response_model=schemas.ResponsePost)
async def update_post(id:int, post:schemas.PostCreate, db:Session=Depends(get_db), current_user : int  =Depends(oauth2.get_current_user)):
    # index=del_post(id)
    # cursor.execute("""UPDATE posts SET title=%s, content=%s, published=%s WHERE id=%s RETURNING *""", (post.title, post.content
    # ,post.published, str(id),))
    # updated=cursor.fetchone()
    # conn.commit()
    # stmt=select(models.Post).where(models.Post.id==id)
    # updated=db.execute(stmt).scalar_one_or_none()

    # post_query=db.query(models.Post).filter(models.Post.id==id)
    # updated=post_query.first()

    stmt=select(models.Post).where(models.Post.id == id)
    updated=db.execute(stmt).scalar_one_or_none()
    
    if updated is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Post {id} not found")
    
    if updated.owner_id!= current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Can not update others post")
    # post_dict=post.dict()
    # post_dict['id']=id
    # my_posts[index]=post_dict

    for key, value in post.dict().items():
        setattr(updated, key, value)
    db.commit()
    db.refresh(updated)

    # updated.update(post.dict(),synchronizatio_session=False)
    # db.commit()

    return updated
