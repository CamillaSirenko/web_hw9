from pymongo import MongoClient
import json

def replace_special_characters(collection):
    # Find all documents containing the special character sequence
    documents_with_special_characters = collection.find({"text": {"$regex": "вЂњ"}})

    # Update documents to replace the special character sequence with a standard double quotation mark
    for document in documents_with_special_characters:
        updated_text = document['text'].replace('вЂњ', '"')
        collection.update_one({"_id": document["_id"]}, {"$set": {"text": updated_text}})

def load_json_to_db(filename, collection):
    with open(filename, 'r', encoding='utf-8') as f:
        file_data = json.load(f)

    collection.insert_many(file_data)

def main():
    client = MongoClient('mongodb+srv://OlgaSHell:PgkhuKA3k2dqHPE@cluster0.ayzqqtl.mongodb.net/?retryWrites=true&w=majority')
    db = client['web_hw9']
    quotes_collection = db['quotes']
    authors_collection = db['authors']

    load_json_to_db('quotes.json', quotes_collection)
    load_json_to_db('authors.json', authors_collection)

    
    replace_special_characters(quotes_collection)

if __name__ == "__main__":
    main()






