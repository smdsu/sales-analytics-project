from fastapi import APIRouter, HTTPException, status, Response, Depends

from app.users.auth import get_password_hash, authenticate_user, create_access_token, get_current_user
from app.users.dao import UsersDAO
from app.users.schemas import SUserRegister, SUserAuth, SUserData, SUserUpd
from app.users.models import User
from app.users.dependencies import is_current_user_admin, is_current_user_superadmin

router_auth = APIRouter(prefix="/auth", tags=["Auth"])
router_users = APIRouter(prefix="/users", tags=["Работа с пользователями"])

@router_auth.get("/")
def auth_page():
    return {"message": "Привет мир аутентификации!"}

@router_auth.post("/register")
async def register_user(user_data: SUserRegister) -> dict:
    user = await UsersDAO.find_one_or_none_by_filter(email=user_data.email)
    if user:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail='Пользователь уже существует')
    user_dict = user_data.dict()
    user_dict['password'] = get_password_hash(user_data.password)
    await UsersDAO.add(**user_dict)
    return {"message": "Пользователь зарегестрирован"}

@router_auth.post("/login")
async def login_user(response: Response, user_data: SUserAuth):
    check = await authenticate_user(email=user_data.email, password=user_data.password)
    if check is None:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Неверное имя пользователя или пароль")
    access_token = create_access_token({"sub": str(check.id)})
    response.set_cookie(key="users_access_token", value=access_token, httponly=True)
    return {'access_token': access_token, 'refresh_token': None}

@router_auth.post("/logout/")
async def logout_user(response: Response):
    response.delete_cookie(key="users_access_token")
    return {'message': 'Пользователь успешно вышел из системы'}

@router_users.get("/", response_model=list[SUserData])
async def get_all_users(user_data: User = Depends(is_current_user_admin)):
    return await UsersDAO.find_all()

@router_users.get("/me", response_model=SUserData)
async def get_me(user_data: User = Depends(get_current_user)):
    return user_data

# Костыль для суперадмина
''' 
@router_users.put("/set_me_founder")
async def set_me_founder(user_data: User = Depends(get_current_user)):
    check = await UsersDAO.update(filter_by={'id': user_data.id}, is_super_admin=True)
    if check:
        return {"message": f"Пользователь {id} успешно обновлен!"}
    else:
        return {"message": "Ошибка при обновлении покупателя!"}
'''

@router_users.get("/{id}", response_model=SUserData, summary="Получить данные пользователя по ID")
async def get_user_by_id(id: int, user_data: User = Depends(is_current_user_admin)) -> SUserData | None:
    rez = await UsersDAO.find_one_or_none_by_id(id)
    if not rez:
        raise HTTPException(status_code=404, detail=f'Пользователь с id={id} не найден')
    return rez

@router_users.post("/add/")
async def add_user(user: SUserRegister, user_data: User = Depends(is_current_user_superadmin)) -> dict:
    check = await UsersDAO.add(**user.dict())
    if check:
        return {"message": "Пользователь успешно добавлен!", "user": user}
    else:
        return {"message": "Ошибка при добавлении пользователя!"}
        
@router_users.put("/update_by_id/{id}")
async def upd_user_by_id(id: int, new_user: SUserUpd = Depends(), user_data: User = Depends(is_current_user_superadmin)) -> dict:
    check = await UsersDAO.update(filter_by={"id": id}, **new_user.to_new_data_dict())
    if check:
        return {"message": f"Пользователь {id} успешно обновлен!", "rows": new_user.to_new_data_dict()}
    else:
        return {"message": "Ошибка при обновлении пользователя!"}
    
@router_users.put("/update_by_filter/")
async def upd_user_by_filter(new_user: SUserUpd = Depends(), user_data: User = Depends(is_current_user_superadmin)) -> dict:
    check = await UsersDAO.update(filter_by=new_user.to_filter_dict(), **new_user.to_new_data_dict())
    if check:
        return {"message": f"Пользователи успешно обновлены!", "rows_updated": check, "data": new_user.to_new_data_dict()}
    else:
        return {"message": "Ошибка при обновлении пользователя!"}

@router_users.delete("/delete/{id}")
async def delete_user_by_id(id: int, user_data: User = Depends(is_current_user_superadmin)) -> dict:
    check = await UsersDAO.delete(id = id)
    if check:
        return {"message": f"Пользователь с {id} удалён!"}
    else:
        return {"message": "Произошла ошибка при удалении пользователя!"}