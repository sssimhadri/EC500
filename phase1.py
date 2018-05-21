import json
import os
from pymongo import MongoClient

def CreateDataBase():
	try:
		f = open("airports.json", 'r')
		data = json.loads(f.read())
		client = MongoClient('localhost:27017')
		db = client.Airports
		db.Airports.insert_many(data)
	except Exception,e:
		print(e)


def Search(field, keyword):
	client = MongoClient()
	db = client.Airports
	request = db.Airports.find_one({field:keyword})
	print("Found result in data base: ")
	for item in request:
		print(item),
		print(':'),
		print(request[item])

def Update(field, keyword):
	client = MongoClient()
	db = client.Airports
	request = db.Airports.find_one({field:keyword})
	for item in request:
		print(item),
		print(':'),
		print(request[item])
	new_field = raw_input("Enter what you would like to update: ")
	new_keyword = raw_input("Enter what you would like to update it to: ")
	db.Airports.update_one({field:keyword},{"$set": {new_field:new_keyword}}, upsert=False)


def main():
	if __name__ == '__main__':
		CreateDataBase()
		print("Do you want to search or update...")
		option = raw_input("Enter 'search' or 'update': ")
		if option == 'search':
			field = raw_input("Enter the field you are searching for: ")
			value = raw_input("Enter the value for that field: ")
			Search(field,value)
		elif option == 'update':
			field = raw_input("Enter the field you are searching for: ")
			value = raw_input("Enter the value for that field: ")
			Update(field, value)
		


main()

