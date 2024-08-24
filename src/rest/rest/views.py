from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from pymongo import MongoClient
import os
from bson import ObjectId
from pymongo.errors import PyMongoError
from django.core.exceptions import ValidationError

# Set up MongoDB connection
mongo_uri = 'mongodb://' + os.environ["MONGO_HOST"] + ':' + os.environ["MONGO_PORT"]
db = MongoClient(mongo_uri)['test_db']

# Hardcoded todos (optional, for initialization)
hardcoded_todos = [
    {"title": "Study DSA", "completed": False},
    {"title": "Hire Raghav", "completed": False},
    {"title": "Check the todo app", "completed": True}
]

def validate_todo_item(todo_item):
    """ Basic validation function """
    if not isinstance(todo_item.get('title'), str) or len(todo_item['title']) == 0:
        return False, "Title must be a non-empty string."
    if not isinstance(todo_item.get('completed'), bool):
        return False, "Completed must be a boolean value."
    return True, None

class TodoListView(APIView):
    def get(self, request):
        try:
            if db.todos.count_documents({}) == 0:
                db.todos.insert_many(hardcoded_todos)
            todos = list(db.todos.find())
            for todo in todos:
                todo['_id'] = str(todo['_id'])
            return Response(todos, status=status.HTTP_200_OK)
        except PyMongoError as e:
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def post(self, request):
        todo_item = request.data
        is_valid, error_message = validate_todo_item(todo_item)
        if not is_valid:
            return Response({"error": error_message}, status=status.HTTP_400_BAD_REQUEST)
        
        try:
            result = db.todos.insert_one(todo_item)
            return Response({"inserted_id": str(result.inserted_id)}, status=status.HTTP_201_CREATED)
        except PyMongoError as e:
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

class TodoDetailView(APIView):
    def patch(self, request, *args, **kwargs):
        todo_id = kwargs.get('id')
        update_data = request.data
        is_valid, error_message = validate_todo_item(update_data)
        if not is_valid:
            return Response({"error": error_message}, status=status.HTTP_400_BAD_REQUEST)
        
        try:
            result = db.todos.update_one({'_id': ObjectId(todo_id)}, {'$set': update_data})
            if result.matched_count == 0:
                return Response({"error": "Todo not found"}, status=status.HTTP_404_NOT_FOUND)
            updated_todo = db.todos.find_one({'_id': ObjectId(todo_id)})
            if updated_todo:
                updated_todo['_id'] = str(updated_todo['_id'])
                return Response(updated_todo, status=status.HTTP_200_OK)
            else:
                return Response({"error": "Todo not found"}, status=status.HTTP_404_NOT_FOUND)
        except (PyMongoError, ValidationError) as e:
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def delete(self, request, *args, **kwargs):
        todo_id = kwargs.get('id')
        try:
            result = db.todos.delete_one({'_id': ObjectId(todo_id)})
            if result.deleted_count > 0:
                return Response(status=status.HTTP_204_NO_CONTENT)
            else:
                return Response({"error": "Todo not found"}, status=status.HTTP_404_NOT_FOUND)
        except PyMongoError as e:
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
