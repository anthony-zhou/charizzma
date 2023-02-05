import asyncio
from microphone import send_receive
import asyncio
from backend import check_new_document
import time

def main():
    while True:
        print("Listening for new document")
        doc_id = check_new_document()
        print(f"FOUND DOCUMENT: {doc_id}")
        
        if doc_id is not None:
            asyncio.run(send_receive(doc_id))
            break
        time.sleep(1)

if __name__ == "__main__":
    main()

# import asyncio
# from microphone import send_receive
# import asyncio
# import threading
# import firebase_admin
# from firebase_admin import credentials, firestore, db

# TIMEOUT = 600

# cred = credentials.Certificate("firebaseAdmin.json")
# firebase_admin.initialize_app(cred)

# db = firestore.client()

# async def listen_for_new_document():
#     callback_done = threading.Event()

#     doc_id = None

#     # Create a callback on_snapshot function to capture changes
#     def on_snapshot(col_snapshot, changes, read_time):
#         global doc_id
#         for doc in col_snapshot:
#             print(f"New Conversation Started! {doc.id}")
#             print(doc.to_dict())


#             doc_id = doc.id

#             callback_done.set()

#             # await send_receive(doc.id)
#             asyncio.run(send_receive(doc_id))
#             break

#     col_query = db.collection(u'conversations').where(u'active', u'==', True)

#     # Watch the collection query
#     query_watch = col_query.on_snapshot(on_snapshot)

#     # Wait for the callback.
#     callback_done.wait(timeout=TIMEOUT)
#     query_watch.unsubscribe()

#     print(doc_id)
#     print("unsub")

#     return doc_id

# async def main():
#     doc_id = await listen_for_new_document()

#     print(f"FROM MAIN {doc_id}")

#     # asyncio.run(send_receive(doc_id))
#     # await send_receive(doc_id)

# if __name__ == "__main__":
#     asyncio.run(main())