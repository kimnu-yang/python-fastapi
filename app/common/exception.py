from app.common.api import Api


def duplicated_email():
    return Api(status="400", message="Duplicated email", data={})


def password_rule_violation():
    return Api(status="400", message="Password rule violation", data={})


def sign_in_data_not_match():
    return Api(status="401", message="Email or Password not matching", data={})


def invalid_jwt():
    return Api(status="401", message="Invalid token", data={})


def expired_jwt():
    return Api(status="401", message="Token expired", data={})


def jwt_data_not_match():
    return Api(status="401", message="JWT data not matching", data={})


def undefined_error():
    return Api(status="500", message="Undefined error", data={})