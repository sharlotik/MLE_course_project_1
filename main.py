from database.config import get_settings
from database.database import get_session, init_db, get_database_engine
from services.crud.user import get_all_users, create_user
from services.crud.event import get_all_events, create_event, get_event_by_id
from services.crud.transaction import get_transaction_by_id, get_transaction_by_user_id, get_all_transactions, create_transaction
from services.crud.wallet import get_balance_by_user_id
from sqlmodel import Session
from models.event import Event, EventBase
from models.user import User
from models.wallet import Wallet
from models.model import Model
from models.transaction import Transaction
from decimal import Decimal



if __name__ == "__main__":
    settings = get_settings()
    print(settings.APP_NAME)
    print(settings.API_VERSION)
    print(f'Debug: {settings.DEBUG}')
    
    print(settings.DB_HOST)
    print(settings.DB_NAME)
    print(settings.DB_USER)
    
    init_db(drop_all=True)
    print('Init db has been success')

    ml_model = Model()
    
    test_user = User(email='test1@gmail.com', password='test')
    test_user_2 = User(email='test2@gmail.com', password='test')
    test_user_3 = User(email='test3@gmail.com', password='test')
    
    test_event = EventBase(title='Вызов модели', image='test', description='test')
    test_event_2 = EventBase(title='Вызов модели', image='test', description='test')

  
   # test_user.events.append(test_event)
    #test_user.events.append(test_event_2)
    
    engine = get_database_engine()
    
    with Session(engine, expire_on_commit=False) as session:
        create_user(test_user, session)
        create_user(test_user_2, session)
        create_user(test_user_3, session)
        create_transaction(test_user_2.id, 'Deposit', Decimal("10.00"), session)
        print(f'Баланс {test_user_2.id} пользователя: \
            {get_balance_by_user_id(test_user_2.id, session)}')
        event_2 = create_event(test_event_2, test_user_2.id, ml_model, session)
        test_user_2.events.append(event_2)
        print(f'Баланс {test_user_2.id} пользователя: \
            {get_balance_by_user_id(test_user_2.id, session)}')
        session.expire_all() 
        users = get_all_users(session)
        events = get_all_events(session)
        transactions = get_all_transactions(session)



    print('-------')
    print(f'Id локального пользователя: {id(test_user)}')
    print(f'Id пользователя из БД: {id(users[0])}')
    print(f'Id одинаковые: {id(test_user) == id(users[0])}')


    print('-------')
    print('Пользователи из БД:')        
    for user in users:
        print(user)
        print()
        print('Пользовательские события:')
        if user.event_count == 0:
            print('Пользователь не имеет событий')
        else:
            for evnt in user.events:
                print(evnt)
    
       
    print('-------')
    print('---Events----')
    if not events:
        print("Список пуст в БД")
    else:
        for ev in events:
            print(ev.model_dump())

       
    print('-------')
    print('---Transactions----')
    if not transactions:
        print("Список пуст в БД")
    else:
        for txn in transactions:
            print(txn.model_dump())