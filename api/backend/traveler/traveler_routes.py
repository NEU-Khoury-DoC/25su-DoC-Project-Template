from flask import Blueprint, jsonify, request
from backend.db_connection import db
from mysql.connector import Error
from flask import current_app

traveler_api = Blueprint("traveler_api", __name__)
