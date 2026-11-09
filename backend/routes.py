"""Songs REST API backed by MongoDB."""
import json
import os
from pathlib import Path
from urllib.parse import quote_plus
from flask import jsonify, request, abort
from pymongo import MongoClient
from . import app

host = os.environ.get('MONGODB_SERVICE', 'localhost:27017')
if ':' not in host:
    host += ':' + os.environ.get('MONGODB_PORT', '27017')
username = os.environ.get('MONGODB_USERNAME')
password = os.environ.get('MONGODB_PASSWORD')
auth = f'{quote_plus(username)}:{quote_plus(password)}@' if username and password else ''
client = MongoClient(os.environ.get('MONGODB_URI', f'mongodb://{auth}{host}/?authSource=admin'), serverSelectionTimeoutMS=5000)
db = client.songs
if db.songs.count_documents({}) == 0:
    with (Path(__file__).parent / 'data' / 'songs.json').open(encoding='utf-8') as source:
        db.songs.insert_many(json.load(source))
db.songs.create_index('id', unique=True)

@app.get('/health')
def health():
    client.admin.command('ping')
    return jsonify(status='OK'), 200

@app.get('/count')
def count():
    return jsonify(length=db.songs.count_documents({})), 200

@app.get('/song')
def get_songs():
    return jsonify(list(db.songs.find({}, {'_id': 0}))), 200

@app.get('/song/<int:id>')
def get_song_by_id(id):
    song = db.songs.find_one({'id': id}, {'_id': 0})
    if song is None:
        abort(404)
    return jsonify(song), 200

@app.post('/song')
def create_song():
    song = request.get_json()
    if not isinstance(song, dict) or not isinstance(song.get('id'), int):
        abort(400)
    if db.songs.find_one({'id': song['id']}):
        return jsonify(Message=f"song with id {song['id']} already present"), 302
    db.songs.insert_one(dict(song))
    return jsonify(song), 201

@app.put('/song/<int:id>')
def update_song(id):
    song = request.get_json()
    if not isinstance(song, dict):
        abort(400)
    song.pop('_id', None)
    song['id'] = id
    if not db.songs.update_one({'id': id}, {'$set': song}).matched_count:
        abort(404)
    return jsonify(song), 200

@app.delete('/song/<int:id>')
def delete_song(id):
    if not db.songs.delete_one({'id': id}).deleted_count:
        abort(404)
    return '', 204
