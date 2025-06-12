from flask import Blueprint, jsonify, request
from backend.db_connection import db
from mysql.connector import Error
from flask import current_app

researcher_api = Blueprint("researcher_api", __name__)
    
@researcher_api.route("/posts", methods=["GET", "POST"])
def handle_posts():
    if request.method == "GET":
        try:
            cursor = db.get_db().cursor()
            query = """
                SELECT 
                    rf.ResearchPostID,
                    rf.Title,
                    rf.PostDate,
                    rf.Research,
                    rf.AuthorID,
                    u.UserName,
                    u.Nationality
                FROM ResearchFindings rf
                LEFT JOIN Users u ON rf.AuthorID = u.UserID
                ORDER BY rf.PostDate DESC
            """
            cursor.execute(query)
            posts = cursor.fetchall()
            cursor.close()
            return jsonify({
                "message": f"Found {len(posts)} posts",
                "posts": posts
            }), 200
        except Error as e:
            return jsonify({"error": str(e)}), 500
    elif request.method == "POST":
        try:
            data = request.get_json()
            required_fields = ["Title", "Research", "AuthorID"]
            cursor = db.get_db().cursor()
            query = """
            INSERT INTO ResearchFindings (Title, Research, AuthorID)
            VALUES (%s, %s, %s)
            """
            cursor.execute(
                query,
                (
                    data["Title"],
                    data["Research"],
                    data["AuthorID"]
                ),
            )
            db.get_db().commit()
            new_research_post_id = cursor.lastrowid
            cursor.close()
            return (
                jsonify({"message": "Post created successfully", "ResearchPostID": new_research_post_id}),
                201,
            )
        except Error as e:
            return jsonify({"error": str(e)}), 500

    

@researcher_api.route("/posts/<int:post_id>/", methods=["GET", "PUT", "DELETE"])
def handle_single_post(post_id):
    ## GET Request
    if request.method == "GET":
        try:
            cursor = db.get_db().cursor()
            query = """
                SELECT 
                    rf.ResearchPostID,
                    rf.Title,
                    rf.PostDate,
                    rf.Research,
                    rf.AuthorID,
                    u.UserName,
                    u.Nationality
                FROM ResearchFindings rf
                LEFT JOIN Users u ON rf.AuthorID = u.UserID
                ORDER BY rf.PostDate DESC
            """
            cursor.execute(query)
            posts = cursor.fetchall()
            cursor.close()
            return jsonify({
                "message": f"Found {len(posts)} posts",
                "posts": posts
            }), 200
        except Error as e:
            return jsonify({"error": str(e)}), 500
    ## DELETE request
    elif request.method == "DELETE":
        try:
            conn = db.get_db()
            cursor = conn.cursor()
            check_query = "SELECT ResearchPostID FROM ResearchFindings WHERE ResearchPostID = %s"
            cursor.execute(check_query, (post_id,))
            post = cursor.fetchone()
            
            if not post:
                cursor.close()
                return jsonify({"error": "Post not found"}), 404
            delete_post_query = "DELETE FROM ResearchFindings WHERE ResearchPostID = %s"
            cursor.execute(delete_post_query, (post_id,))
            conn.commit()
            cursor.close()
            return jsonify({"message": f"Post {post_id} deleted successfully"}), 200
        except Error as e:
            if conn:
                conn.rollback()
            return jsonify({"error": str(e)}), 500
    ##PUT request
    elif request.method == "PUT":
        try:
            data = request.get_json()

            cursor = db.get_db().cursor()
            cursor.execute("SELECT * FROM ResearchFindings WHERE ResearchPostID = %s", (research_post_id,))
            if not cursor.fetchone():
                return jsonify({"error": "Post not found"}), 404
            
            update_fields = []
            params = []
            allowed_fields = ["Title", "Research"]

            for field in allowed_fields:
                if field in data:
                    update_fields.append(f"{field} = %s")
                    params.append(data[field])

            if not update_fields:
                return jsonify({"error": "No valid fields to update"}), 400

            params.append(post_id)
            query = f"UPDATE ResearchFindings SET {', '.join(update_fields)} WHERE ResearchPostID = %s"

            cursor.execute(query, params)
            db.get_db().commit()
            cursor.close()

            return jsonify({"message": "Post updated successfully"}), 200
        except Error as e:
            return jsonify({"error": str(e)}), 500
    

@researcher_api.route("/debug_researchers", methods=["GET"])
def debug_researchers():
    try:
        cursor = db.get_db().cursor()
        cursor.execute("SELECT * FROM Researcher;")
        researchers = cursor.fetchall()
        cursor.close()
        return jsonify({"researchers": researchers})
    except Exception as e:
        return jsonify({"error": str(e)}), 500