from fastapi import FastAPI #Импорт FastAPI
from pydantic import BaseModel, Field, validator
from typing import List
from datetime import datetime

ALLOWED_CATEGORIES = ["зарплата", "бонус", "инвестиции", "подарок", "фриланс", "еда", "транспорт", "развлечения", "здоровье", "образование", "доход", "другое"] #Разрешенные категории

# Модель для описания данных транзакции
class Transaction(BaseModel):
    id: int = Field(gt=0, description="ID должжен быть положительным числом")
    amount: float = Field(gt=0, description="Сумма транзакций") #Сумма, только положительные числа
    type: str = Field(description="Тип операции: income(доход) или expense(расход)")
    description: str = Field(min_lenght=2, max_lenght=300, description="Описание операции") #описание
    category: str = Field(description="Категория транзакции")#категория
    date: datetime = datetime.now()  # По умолчанию текущая дата

    @validator('type')
    def validate_type(cls, v);
        if v not in ['income', 'expense']:
            raise ValueError("Тип должен быть income или expense")
        return v

    @validator('amount')
    def amount_cannot_be_zero(cls, v):
        if v == 0:
            raise ValueError("Сумма не может быть нулевой")
        return v
    
    @validator('description')
    def description_cannot_be_empty(cls, v):
        if not v.strip():  # Проверяем что не пустая строка или пробелы
            raise ValueError('Описание не может быть пустым')
        return v.strip()


app = FastAPI(title="Personal Finance Tracker")


transactions_db = {} # Пока что это БД
next_id = 1


@app.get("/")
async def root():
    return {"message": "Добро пожаловать в систему учета финансов!"}

# Возвращаем все транзакции из нашего "хранилища"
@app.get("/transactions") 
async def get_transactions():
    
    return {"transactions": list(transactions_db.values())}

# Добавляем новую транзакцию в наш список
@app.post("/transactions") 
async def create_transaction(transaction_id: Transaction):
    global next_id

    if transaction_id.category not in ALLOWED_CATEGORIES:
        return {"error": f"Категория {transaction_id.category} не существует. Добавленные: {ALLOWED_CATEGORIES}"}

    transaction_id.id = next_id
    transactions_db[next_id] = transaction_id
    next_id += 1

    type_russian = "доход" if transaction_id.type == "income" else "расход"

    return {"message": "{type_russian.capitalize()} добавлен", "transaction": transaction_id}

# Удаляем транзакцию по ее айди
@app.delete("/transactions/{transaction_id}") 
async def delete_transaction(transaction_id: int):
    if transaction_id in transactions_db:
        del transactions_db[transaction_id]
        return {"message": f"Транзакция {transaction_id} удалена"}

    return {"error": f"Транзакция {transaction_id} не найдена"}

# Обновляем транзацию по айди
@app.put("/transactions/{transaction_id}")
async def update_transaction(transaction_id: int, updated_transaction: Transaction):
    if transaction_id in transactions_db:
        updated_transaction.id = transaction_id
        transactions_db[transaction_id] = updated_transaction
        return {"message": f"Транзакция {transaction_id} успешно обновлена", "transaction": updated_transaction}
    return {"error": f"Ошибка, транзакция {transaction_id} не найдена"}
