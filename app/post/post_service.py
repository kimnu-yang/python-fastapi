from fastapi import Request
from app.models.post_model import Post, PostCreateRequest, PostUpdateRequest
from app.user.user_service import get_user_by_id
from app.common.api import success_response
from app.common.jwt import decode_token
from app.common.exception import not_found, too_long_title, not_permitted
from datetime import datetime, timezone


# 게시글 목록 조회
def get_all_posts(db_session, sort, page, size):
    offset = (page - 1) * size
    posts = db_session.query(Post)
    if sort:
        if ',' in sort:
            sort_data = sort.split(',')
        else:
            sort_data = [sort]

        if sort_data[0] in ['hits', 'created_at']:
            if len(sort_data) > 1 and sort_data[1].upper() == "DESC":
                posts = posts.order_by(getattr(Post, sort_data[0]).desc())
            else:
                posts = posts.order_by(getattr(Post, sort_data[0]))

    posts = posts.offset(offset).limit(size).all()

    if len(posts) < 1:
        return not_found()
    else:
        data = {}
        cnt = 0
        for post in posts:
            writer = get_user_by_id(db_session, post.writer)
            data[cnt] = {
                "title": post.title,
                "writer": writer["username"],
                "hits": post.hits
            }
            cnt += 1
    return success_response(data)


# 게시글 조회
def get_post(db_session, post_id: int):
    post = db_session.query(Post).filter(Post.id == post_id).first()
    if post:
        writer = get_user_by_id(db_session, post.writer)
        return success_response({
            "title": post.title,
            "writer": writer["username"],
            "content": post.content,
            "created_at": post.created_at,
            "updated_at": "" if post.updated_at is None else post.updated_at
        })
    else:
        return not_found()


# 게시글 생성
def create_post(request: Request, db_session, post: PostCreateRequest):
    token = request.headers.get("authorized-key")
    if len(post.title) > 100:
        return too_long_title()

    token_data = decode_token(token)
    new_post = Post(title=post.title, content=post.content, writer=token_data["id"])
    db_session.add(new_post)
    db_session.commit()
    db_session.refresh(new_post)
    return success_response(new_post.to_dict())


# 게시글 수정
def update_post(request: Request, db_session, post_id: int, post: PostUpdateRequest):
    token = request.headers.get("authorized-key")
    token_data = decode_token(token)
    db_data = db_session.query(Post).filter(Post.id == post_id).first()

    if token_data["id"] == int(db_data.writer):
        if post.title is not None:
            db_data.title = post.title
        if post.content is not None:
            db_data.content = post.content
        db_data.updated_at = datetime.now(timezone.utc)
        db_session.commit()
        db_session.refresh(db_data)
        return success_response({"updated_post_id": db_data.id})
    else:
        return not_permitted()


# 게시글 삭제
def delete_post(request: Request, db_session, post_id: int):
    token = request.headers.get("authorized-key")
    token_data = decode_token(token)
    db_data = db_session.query(Post).filter(Post.id == post_id).first()

    if token_data["id"] == int(db_data.writer):
        db_session.delete(db_data)
        db_session.commit()
        return success_response({"deleted_post_id": db_data.id})
    else:
        return not_permitted()