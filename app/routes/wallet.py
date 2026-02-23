from fastapi import APIRouter, Body, HTTPException, status, Depends
from database.database import get_session
from models.wallet import Wallet
from services.crud import wallet as WalletService
from decimal import Decimal
from typing import List

wallet_router = APIRouter()

@wallet_router.get("/{user_id}", response_model=Decimal) 
async def retrieve_wallet(user_id : int, session=Depends(get_session)):
  balance = WalletService.get_balance_by_user_id(user_id, session)    
  if balance is None:
      raise HTTPException(
          status_code=status.HTTP_404_NOT_FOUND,
          detail=f"Wallet for user {user_id} not found"
      )
  
  return balance

#@wallet_router.get("/{id}", response_model=Transaction) 
#async def retrieve_wallet(id: int) -> Transaction:
 #   for wallet in transactions: 
   #     if wallet.id == id:
    #        return wallet 
    #raise HTTPException(status_code=status. HTTP_404_NOT_FOUND, 
     #       detail="Transaction with supplied ID does not exist")

#@transaction_router.post("/new")
#async def create_transaction(body: Transaction = Body(...)) -> dict: 
 #   transactions.append(body)
  #  return {"message": "Transaction created successfully"}

#@transaction_router.delete("/{id}")
#async def delete_transaction(id: int) -> dict: 
#    for transaction in tansactions:
#        if transaction.id == id: 
#            transactions.remove(tansaction)
#            return {"message": "Transaction deleted successfully"}
#        raise HTTPException(status_code=status. HTTP_404_NOT_FOUND, 
#        detail="Transaction with supplied ID does not exist")

#@transaction_router.delete("/")
#async def delete_all_transactions() -> dict: 
#    transactions.clear()
#    return {"message": "Transactions deleted successfully"}