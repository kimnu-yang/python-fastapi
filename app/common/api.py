from pydantic import BaseModel


class Api(BaseModel):
    status: str
    message: str
    data: dict


def success_response(data: dict):
    return Api(status="200", message="OK", data=data)
