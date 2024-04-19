from fastapi import Request
from app.post.post_model import Post, PostCreateRequest, PostUpdateRequest
from app.user.user_service import get_user_by_id
from app.common.api import success_response
from app.common.jwt import decode_token
from app.common.exception import not_found, invalid_jwt, too_long_title, expired_jwt, undefined_error, not_permitted
from datetime import datetime, timezone


# 게시글 목록 조회
def get_all_posts(db_session):
    posts = db_session.query(Post).all()
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
    if token is None:
        return invalid_jwt()
    if len(post.title) > 100:
        return too_long_title()

    token_data = decode_token(token)
    if type(token_data) is dict:
        new_post = Post(title=post.title, content=post.content, writer=token_data["id"])
        db_session.add(new_post)
        db_session.commit()
        db_session.refresh(new_post)
        return success_response(new_post.to_dict())
    elif type(token_data) is int:
        if token_data == 1:
            return expired_jwt()
        elif token_data == 2:
            return invalid_jwt()
        else:
            return undefined_error()
    else:
        return undefined_error()


# 게시글 수정
def update_post(request: Request, db_session, post_id: int, post: PostUpdateRequest):
    token = request.headers.get("authorized-key")
    if token is None:
        return invalid_jwt()

    token_data = decode_token(token)
    db_data = db_session.query(Post).filter(Post.id == post_id).first()

    if type(token_data) is dict:
        if token_data["id"] == int(db_data.writer):
            if post.title is not None:
                db_data.title = post.title
            if post.content is not None:
                db_data.content = post.content
            db_data.updated_at = datetime.now(timezone.utc)
            db_session.commit()
            db_session.refresh(db_data)
            return success_response({"post_id":db_data.id})
        else:
            return not_permitted()
    elif type(token_data) is int:
        if token_data == 1:
            return expired_jwt()
        elif token_data == 2:
            return invalid_jwt()
        else:
            return undefined_error()
    else:
        return undefined_error()


# 게시글 삭제
def delete_post(request: Request, db_session, post_id: int):
    token = request.headers.get("authorized-key")
    if token is None:
        return invalid_jwt()

    token_data = decode_token(token)
    db_data = db_session.query(Post).filter(Post.id == post_id).first()

    if type(token_data) is dict:
        if token_data["id"] == int(db_data.writer):
            db_session.delete(db_data)
            db_session.commit()
            return success_response({"post_id": db_data.id})
        else:
            return not_permitted()
    elif type(token_data) is int:
        if token_data == 1:
            return expired_jwt()
        elif token_data == 2:
            return invalid_jwt()
        else:
            return undefined_error()
    else:
        return undefined_error()
