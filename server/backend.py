import firebase_admin
from firebase_admin import credentials, firestore, db
import threading

import asyncio
# from microphone import send_receive

TIMEOUT = 600
doc_id = None

cred = credentials.Certificate("firebaseAdmin.json")
firebase_admin.initialize_app(cred)

db = firestore.client()
# doc_ref = db.collection(u'conversations').document(u'convo_2348wfh')

# doc = doc_ref.get()
# if doc.exists:
#     print(f'Document data: {doc.to_dict()}')
# else:
#     print(u'No such document!')

def update_conversation(doc_id, convo_text, gpt_calls):
    conversation_ref = db.collection(u'conversations').document(doc_id)

    data = {
        u'formatted_transcript': convo_text,
        u'gpt_calls': gpt_calls
        # [{
        #     u'call_text': "",
        #     u'call_type': ""
        # }]
    }

    conversation_ref.update(data)

def check_session_active(doc_id):
    conversation_ref = db.collection(u'conversations').document(doc_id)

    doc = conversation_ref.get()

    if doc.exists and doc.to_dict()["active"] == False:
        return False

    return True

def check_new_document():
    # conversation_ref = db.collection(u'conversations').document(doc_id)
    col_query = db.collection(u'conversations').where(u'active', u'==', True)

    col_snapshot = col_query.get()

    for doc in col_snapshot:
        print(doc)

        if doc.exists and doc.to_dict()["active"] == True:
            return doc.id

    return None

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

#             send_receive(doc.id)
#             callback_done.set()

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


# async def listen_for_new_document():
#     # Create a callback on_snapshot function to capture changes
#     def on_snapshot(col_snapshot, changes, read_time):
#         for doc in col_snapshot:
#             print(f"New Conversation Started! {doc.id}")
#             print(doc.to_dict())
            
#             query_watch.unsubscribe()
#             return doc.id
        
#     col_query = db.collection(u'conversations').where(u'active', u'==', True)

#     # Watch the collection query
#     query_watch = col_query.on_snapshot(on_snapshot)

# listen_for_new_document()

# TODO: Figure out a way to end the conversentation
