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

transactions_db = [] # Пока что это БД

@app.get("/")
async def root():
    return {"message": "Добро пожаловать в систему учета финансов!"}

@app.get("/transactions") # Метод GET используется для получения данных с сервера
async def get_transactions():
    # Возвращаем все транзакции из нашего "хранилища"
    return {"transactions": transactions_db}

@app.post("/transactions") # Метод POST используется для отправки данных на сервер
async def create_transaction(transaction: Transaction):
    # Добавляем новую транзакцию в наш список
    transactions_db.append(transaction)
    return {"message": "Транзакция добавлена", "transaction": transaction}

@app.delete("/transactions/{transaction_id}") # Удаляем транзакцию по ее айди
async def delete_transaction(transaction_id: int):
    for transaction in transactions_db:
        if transaction_id == transaction.id:
            transactions_db.remove(transaction)
            return {"message": f"Транзакция {transaction_id} удалена"}

    return {"error": f"Транзакция {transaction_id} не найдена"}

@app.put("/transactions/{transaction_id}")
async def update_transaction(transaction_id: int, updated_transaction: Transaction):
    for index, transaction in enumerate(transactions_db):
        if transaction_id == transaction.id:
            transactions_db[index] = updated_transaction
            return {"message": f"Транзакция {transaction_id} обновлена", "transaction": updated_transaction}
    return {"error": f"Транзакция {transaction_id} не найдена"}