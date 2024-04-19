from fastapi import Request
from app.post.post_model import Post, PostCreateRequest, PostUpdateRequest
from app.common.api import success_response
from app.common.jwt import decode_token
from app.common.exception import not_found, invalid_jwt, too_long_title, expired_jwt, undefined_error


# 모든 게시물 조회
def get_all_posts(db_session):
    data = db_session.query(Post).all()
    if len(data) < 1:
        return not_found()
    return success_response({"result": data})


# 게시물 생성
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
            return invalid_jwt()
        elif token_data == 2:
            return expired_jwt()
        else:
            return undefined_error()
    else:
        return undefined_error()


