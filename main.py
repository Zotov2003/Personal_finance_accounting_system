from fastapi import FastAPI #Импорт FastAPI
from pydantic import BaseModel
from typing import Optional
from datetime import datetime

# Модель для описания данных транзакции
class Transaction(BaseModel):
    id: int
    amount: float #Сумма
    description: str  #описание
    category: str #категория
    date: datetime = datetime.now()  # По умолчанию текущая дата

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

    transaction_id.id = next_id
    transactions_db[next_id] = transaction_id
    next_id += 1
    
    return {"message": "Транзакция добавлена", "transaction": transaction_id}

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
        transactions_db[transaction_id] = updated_transaction
        return {"message": f"Транзакция {transaction_id} успешно обновлена", "transaction": updated_transaction}
    return {"error": f"Ошибка, транзакция {transaction_id} не найдена"}
