from typing import TypedDict


class AuthorDto(TypedDict):
    first_name: str
    last_name: str
    birthday: str


class AuthorObjDto(AuthorDto):
    id: int
