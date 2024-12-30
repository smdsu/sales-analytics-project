from fastapi import APIRouter, HTTPException, status, Response, Depends

from app.users.auth import get_password_hash, authenticate_user, create_access_token, get_current_user
from app.users.dao import UsersDAO
from app.users.schemas import SUserRegister, SUserAuth, SUserData
from app.users.models import User
from app.users.dependencies import is_current_user_admin, is_current_user_superadmin

router = APIRouter(prefix="/auth", tags=["Auth"])

@router.get("/")
def auth_page():
    return {"message": "Привет мир аутентификации!"}

@router.post("/register")
async def register_user(user_data: SUserRegister) -> dict:
    user = await UsersDAO.find_one_or_none_by_filter(email=user_data.email)
    if user:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail='Пользователь уже существует')
    user_dict = user_data.dict()
    user_dict['password'] = get_password_hash(user_data.password)
    await UsersDAO.add(**user_dict)
    return {"message": "Пользователь зарегестрирован"}

@router.post("/login")
async def login_user(response: Response, user_data: SUserAuth):
    check = await authenticate_user(email=user_data.email, password=user_data.password)
    if check is None:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Неверное имя пользователя или пароль")
    access_token = create_access_token({"sub": str(check.id)})
    response.set_cookie(key="users_access_token", value=access_token, httponly=True)
    return {'access_token': access_token, 'refresh_token': None}

@router.post("/logout/")
async def logout_user(response: Response):
    response.delete_cookie(key="users_access_token")
    return {'message': 'Пользователь успешно вышел из системы'}

@router.get("/me", response_model=SUserData)
async def get_me(user_data: User = Depends(get_current_user)):
    return user_data

@router.get("/all_users/", response_model=list[SUserData])
async def get_all_users(user_data: User = Depends(is_current_user_admin)):
    return await UsersDAO.find_all()

# Костыль для суперадмина
''' 
@router.put("/set_me_founder")
async def set_me_founder(user_data: User = Depends(get_current_user)):
    check = await UsersDAO.update(filter_by={'id': user_data.id}, is_super_admin=True)
    if check:
        return {"message": f"Пользователь {id} успешно обновлен!"}
    else:
        return {"message": "Ошибка при обновлении покупателя!"}
'''