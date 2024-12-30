from pydantic import Field, EmailStr, BaseModel

class SUserRegister(BaseModel):
    phone_number: str = Field(..., description="Номер телефона, начинающийся с +")
    email: EmailStr = Field(..., description="Электронная почта")
    first_name: str = Field(..., description="Имя")
    last_name: str = Field(..., description="Фамилия")
    password: str = Field(..., min_length=5, max_length=50, description="Пароль от 5 до 50 знаков") #Сделать проверку пароля на стойкость

class SUserAuth(BaseModel):
    email: EmailStr = Field(..., description="Электронная почта")
    password: str = Field(..., min_length=5, max_length=50, description="Пароль от 5 до 50 знаков")

class SUserData(BaseModel):
    id: int = Field(..., description="ID пользователя")
    first_name: str = Field(..., description="Имя")
    last_name: str = Field(..., description="Фамилия")

    phone_number: str = Field(..., description="Номер телефона, начинающийся с +")
    email: EmailStr = Field(..., description="Электронная почта")

    password: str = Field(..., description="Хэш пароля'}")

    is_user: bool
    is_vendor: bool
    is_analyst: bool
    is_admin: bool
    is_super_admin: bool