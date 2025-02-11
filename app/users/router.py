from fastapi import APIRouter, HTTPException, status, Depends, Response
from app.users.models import User
from app.users.dao import UsersDAO
from app.users.dependencies import get_current_user, get_current_admin_user
from app.users.schemas import SUserRegister, SUserAuth
from app.users.auth import get_password_hash, authenticate_user, create_access_token

router = APIRouter(prefix='/auth', tags=['Auth'])


@router.post('/register/')
async def register_user(user_data: SUserRegister) -> dict:
    user = await UsersDAO.find_one_or_none(email=user_data.email)
    if user:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail='User exists!')

    user_dict = user_data.model_dump()
    user_dict['password'] = get_password_hash(user_data.password)
    await UsersDAO.add(**user_dict)
    return {"message": "You are registered successfully!"}


@router.post('/login/')
async def auth_user(response: Response, user_data: SUserAuth) -> dict:
    check = await authenticate_user(email=user_data.email, password=user_data.password)
    if check is None:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail='Incorrect email or password')
    access_token = create_access_token({'sub': str(check.id)})
    response.set_cookie(key='users_access_token', value=access_token, httponly=True)
    return {'access_token': access_token, 'refresh_token': None}


@router.get('/me/')
async def get_me(user_data: User = Depends(get_current_user)):
    return user_data


@router.post('/logout/')
async def logout_user(response: Response):
    response.delete_cookie(key='users_access_token')
    return {'message': 'You have been logged out!'}


@router.get('/all_users/')
async def get_all_users(user_data: User = Depends(get_current_admin_user)):
    return await UsersDAO.find_all()
