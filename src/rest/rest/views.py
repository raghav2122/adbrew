from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from pymongo import MongoClient
import os
from bson import ObjectId

# Set up MongoDB connection
mongo_uri = 'mongodb://' + os.environ["MONGO_HOST"] + ':' + os.environ["MONGO_PORT"]
db = MongoClient(mongo_uri)['test_db']

class TodoListView(APIView):
    def get(self, request):
        if db.todos.count_documents({}) == 0:
            db.todos.insert_many(hardcoded_todos)
        todos = list(db.todos.find())
        for todo in todos:
            todo['_id'] = str(todo['_id'])
        return Response(todos, status=status.HTTP_200_OK)

    def post(self, request):
        todo_item = request.data
        result = db.todos.insert_one(todo_item)
        return Response({"inserted_id": str(result.inserted_id)}, status=status.HTTP_201_CREATED)

class TodoDetailView(APIView):
    def patch(self, request, *args, **kwargs):
        todo_id = kwargs.get('id')
        update_data = request.data
        db.todos.update_one({'_id': ObjectId(todo_id)}, {'$set': update_data})
        updated_todo = db.todos.find_one({'_id': ObjectId(todo_id)})
        updated_todo['_id'] = str(updated_todo['_id'])
        return Response(updated_todo, status=status.HTTP_200_OK)

    def delete(self, request, *args, **kwargs):
        todo_id = kwargs.get('id')
        result = db.todos.delete_one({'_id': ObjectId(todo_id)})
        if result.deleted_count > 0:
            return Response(status=status.HTTP_204_NO_CONTENT)
        else:
            return Response({"error": "Todo not found"}, status=status.HTTP_404_NOT_FOUND)
