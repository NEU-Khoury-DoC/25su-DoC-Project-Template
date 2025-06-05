from flask import Blueprint, jsonify, request, current_app
from backend.db_connection import db
from mysql.connector import Error

# Create a Blueprint for post utils routes
post_utils = Blueprint("post_utils", __name__)

# PUT request to add an upvote to a post
# Handles the case where user has already upvoted by returning a 200 status
# Example: /post_utils/post/193/upvote/456
@post_utils.route("/post/<int:post_id>/upvote/<int:user_id>", methods=["PUT"])
def put_upvote(post_id, user_id):
    try:
        current_app.logger.info(f"Starting put_upvote request for post {post_id} by user {user_id}")
        cursor = db.get_db().cursor()

        # First check if the upvote already exists
        check_query = """
            SELECT COUNT(*) 
            FROM UpvotesUsers 
            WHERE UserID = %s AND PostID = %s
        """
        cursor.execute(check_query, (user_id, post_id))
        exists = cursor.fetchone()['COUNT(*)'] > 0

        if exists: # If the user has already upvoted the post, return a 200 status
            current_app.logger.info(f"User {user_id} has already upvoted post {post_id}")
            return jsonify({"message": "User has already upvoted this post"}), 200

        # If no existing upvote, add the upvote
        insert_query = """
            INSERT INTO UpvotesUsers (UserID, PostID) 
            VALUES (%s, %s)
        """
        cursor.execute(insert_query, (user_id, post_id))

        # Update the post's upvote count
        update_query = """
            UPDATE Posts 
            SET NumUpvotes = (
                SELECT COUNT(*) 
                FROM UpvotesUsers 
                WHERE PostID = %s
            )
            WHERE PostID = %s
        """
        cursor.execute(update_query, (post_id, post_id))
        
        db.get_db().commit()
        cursor.close()

        current_app.logger.info(f"Successfully added upvote for post {post_id} by user {user_id}")
        return jsonify({"message": "Successfully upvoted post"}), 200

    except Error as e:
        current_app.logger.error(f"Database error in put_upvote: {str(e)}")
        return jsonify({"error": str(e)}), 500

# DELETE request to remove an upvote from a post
# Example: /post_utils/post/193/upvote/456
@post_utils.route("/post/<int:post_id>/upvote/<int:user_id>", methods=["DELETE"])
def delete_upvote(post_id, user_id):
    try:
        current_app.logger.info(f"Starting delete_upvote request for post {post_id} by user {user_id}")
        cursor = db.get_db().cursor()

        # Delete the upvote
        delete_query = """
            DELETE FROM UpvotesUsers 
            WHERE UserID = %s AND PostID = %s
        """
        cursor.execute(delete_query, (user_id, post_id))
        
        # Check if any rows were actually deleted
        if cursor.rowcount == 0:
            current_app.logger.info(f"No upvote found to delete for post {post_id} by user {user_id}")
            return jsonify({"message": "No upvote found to delete"}), 404

        # Update the post's upvote count
        update_query = """
            UPDATE Posts 
            SET NumUpvotes = (
                SELECT COUNT(*) 
                FROM UpvotesUsers 
                WHERE PostID = %s
            )
            WHERE PostID = %s
        """
        cursor.execute(update_query, (post_id, post_id))
        
        db.get_db().commit()
        cursor.close()

        current_app.logger.info(f"Successfully removed upvote for post {post_id} by user {user_id}")
        return jsonify({"message": "Successfully removed upvote"}), 200

    except Error as e:
        current_app.logger.error(f"Database error in delete_upvote: {str(e)}")
        return jsonify({"error": str(e)}), 500

# PUT request to add a downvote to a post
# Handles the case where user has already downvoted by returning a 200 status
# Example: /post_utils/post/193/downvote/456
@post_utils.route("/post/<int:post_id>/downvote/<int:user_id>", methods=["PUT"])
def put_downvote(post_id, user_id):
    try:
        current_app.logger.info(f"Starting put_downvote request for post {post_id} by user {user_id}")
        cursor = db.get_db().cursor()

        # First check if the downvote already exists
        check_query = """
            SELECT COUNT(*) 
            FROM DownvotesUsers 
            WHERE UserID = %s AND PostID = %s
        """
        cursor.execute(check_query, (user_id, post_id))
        exists = cursor.fetchone()['COUNT(*)'] > 0

        if exists: # If the user has already downvoted the post, return a 200 status
            current_app.logger.info(f"User {user_id} has already downvoted post {post_id}")
            return jsonify({"message": "User has already downvoted this post"}), 200

        # If no existing downvote, add the downvote
        insert_query = """
            INSERT INTO DownvotesUsers (UserID, PostID) 
            VALUES (%s, %s)
        """
        cursor.execute(insert_query, (user_id, post_id))

        # Update the post's downvote count
        update_query = """
            UPDATE Posts 
            SET NumDownvotes = (
                SELECT COUNT(*) 
                FROM DownvotesUsers 
                WHERE PostID = %s
            )
            WHERE PostID = %s
        """
        cursor.execute(update_query, (post_id, post_id))
        
        db.get_db().commit()
        cursor.close()

        current_app.logger.info(f"Successfully added downvote for post {post_id} by user {user_id}")
        return jsonify({"message": "Successfully downvoted post"}), 200

    except Error as e:
        current_app.logger.error(f"Database error in put_downvote: {str(e)}")
        return jsonify({"error": str(e)}), 500

# DELETE request to remove a downvote from a post
# Example: /post_utils/post/193/downvote/456
@post_utils.route("/post/<int:post_id>/downvote/<int:user_id>", methods=["DELETE"])
def delete_downvote(post_id, user_id):
    try:
        current_app.logger.info(f"Starting delete_downvote request for post {post_id} by user {user_id}")
        cursor = db.get_db().cursor()

        # Delete the downvote
        delete_query = """
            DELETE FROM DownvotesUsers 
            WHERE UserID = %s AND PostID = %s
        """
        cursor.execute(delete_query, (user_id, post_id))
        
        # Check if any rows were actually deleted
        if cursor.rowcount == 0:
            current_app.logger.info(f"No downvote found to delete for post {post_id} by user {user_id}")
            return jsonify({"message": "No downvote found to delete"}), 404

        # Update the post's downvote count
        update_query = """
            UPDATE Posts 
            SET NumDownvotes = (
                SELECT COUNT(*) 
                FROM DownvotesUsers 
                WHERE PostID = %s
            )
            WHERE PostID = %s
        """
        cursor.execute(update_query, (post_id, post_id))
        
        db.get_db().commit()
        cursor.close()

        current_app.logger.info(f"Successfully removed downvote for post {post_id} by user {user_id}")
        return jsonify({"message": "Successfully removed downvote"}), 200

    except Error as e:
        current_app.logger.error(f"Database error in delete_downvote: {str(e)}")
        return jsonify({"error": str(e)}), 500

# PUT request to add an endorsement to a post
# Handles the case where user has already endorsed by returning a 200 status
# Example: /post_utils/post/193/endorsement/456
@post_utils.route("/post/<int:post_id>/endorsement/<int:user_id>", methods=["PUT"])
def put_endorsement(post_id, user_id):
    try:
        current_app.logger.info(f"Starting put_endorsement request for post {post_id} by user {user_id}")
        cursor = db.get_db().cursor()

        # First check if the endorsement already exists
        check_query = """
            SELECT COUNT(*) 
            FROM EndorsementsUsers 
            WHERE UserID = %s AND PostID = %s
        """
        cursor.execute(check_query, (user_id, post_id))
        exists = cursor.fetchone()['COUNT(*)'] > 0

        if exists: # If the user has already endorsed the post, return a 200 status
            current_app.logger.info(f"User {user_id} has already endorsed post {post_id}")
            return jsonify({"message": "User has already endorsed this post"}), 200

        # If no existing endorsement, add the endorsement
        insert_query = """
            INSERT INTO EndorsementsUsers (UserID, PostID) 
            VALUES (%s, %s)
        """
        cursor.execute(insert_query, (user_id, post_id))

        # Update the post's endorsement count
        update_query = """
            UPDATE Posts 
            SET NumEndorsements = (
                SELECT COUNT(*) 
                FROM EndorsementsUsers 
                WHERE PostID = %s
            )
            WHERE PostID = %s
        """
        cursor.execute(update_query, (post_id, post_id))
        
        db.get_db().commit()
        cursor.close()

        current_app.logger.info(f"Successfully added endorsement for post {post_id} by user {user_id}")
        return jsonify({"message": "Successfully endorsed post"}), 200

    except Error as e:
        current_app.logger.error(f"Database error in put_endorsement: {str(e)}")
        return jsonify({"error": str(e)}), 500

# DELETE request to remove an endorsement from a post
# Example: /post_utils/post/193/endorsement/456
@post_utils.route("/post/<int:post_id>/endorsement/<int:user_id>", methods=["DELETE"])
def delete_endorsement(post_id, user_id):
    try:
        current_app.logger.info(f"Starting delete_endorsement request for post {post_id} by user {user_id}")
        cursor = db.get_db().cursor()

        # Delete the endorsement
        delete_query = """
            DELETE FROM EndorsementsUsers 
            WHERE UserID = %s AND PostID = %s
        """
        cursor.execute(delete_query, (user_id, post_id))
        
        # Check if any rows were actually deleted
        if cursor.rowcount == 0:
            current_app.logger.info(f"No endorsement found to delete for post {post_id} by user {user_id}")
            return jsonify({"message": "No endorsement found to delete"}), 404

        # Update the post's endorsement count
        update_query = """
            UPDATE Posts 
            SET NumEndorsements = (
                SELECT COUNT(*) 
                FROM EndorsementsUsers 
                WHERE PostID = %s
            )
            WHERE PostID = %s
        """
        cursor.execute(update_query, (post_id, post_id))
        
        db.get_db().commit()
        cursor.close()

        current_app.logger.info(f"Successfully removed endorsement for post {post_id} by user {user_id}")
        return jsonify({"message": "Successfully removed endorsement"}), 200

    except Error as e:
        current_app.logger.error(f"Database error in delete_endorsement: {str(e)}")
        return jsonify({"error": str(e)}), 500

# PUT request to add a bookmark to a post
# Handles the case where user has already bookmarked by returning a 200 status
# Example: /post_utils/post/193/bookmark/456
@post_utils.route("/post/<int:post_id>/bookmark/<int:user_id>", methods=["PUT"])
def put_bookmark(post_id, user_id):
    try:
        current_app.logger.info(f"Starting put_bookmark request for post {post_id} by user {user_id}")
        cursor = db.get_db().cursor()

        # First check if the bookmark already exists
        check_query = """
            SELECT COUNT(*) 
            FROM BookmarkedUsers 
            WHERE UserID = %s AND PostID = %s
        """
        cursor.execute(check_query, (user_id, post_id))
        exists = cursor.fetchone()["COUNT(*)"] > 0

        if exists: # If the user has already bookmarked the post, return a 200 status
            current_app.logger.info(f"User {user_id} has already bookmarked post {post_id}")
            return jsonify({"message": "User has already bookmarked this post"}), 200

        # If no existing bookmark, add the bookmark
        insert_query = """
            INSERT INTO BookmarkedUsers (UserID, PostID) 
            VALUES (%s, %s)
        """
        cursor.execute(insert_query, (user_id, post_id))
        
        db.get_db().commit()
        cursor.close()

        current_app.logger.info(f"Successfully added bookmark for post {post_id} by user {user_id}")
        return jsonify({"message": "Successfully bookmarked post"}), 200

    except Error as e:
        current_app.logger.error(f"Database error in put_bookmark: {str(e)}")
        return jsonify({"error": str(e)}), 500
    
# DELETE request to remove a bookmark from a post
# Example: /post_utils/post/193/bookmark/456
@post_utils.route("/post/<int:post_id>/bookmark/<int:user_id>", methods=["DELETE"])
def delete_bookmark(post_id, user_id):
    try:
        current_app.logger.info(f"Starting delete_bookmark request for post {post_id} by user {user_id}")
        cursor = db.get_db().cursor()

        # Delete the bookmark
        delete_query = """
            DELETE FROM BookmarkedUsers 
            WHERE UserID = %s AND PostID = %s
        """
        cursor.execute(delete_query, (user_id, post_id))
        
        # Check if any rows were actually deleted
        if cursor.rowcount == 0:
            current_app.logger.info(f"No bookmark found to delete for post {post_id} by user {user_id}")
            return jsonify({"message": "No bookmark found to delete"}), 404
        
        db.get_db().commit()
        cursor.close()

        current_app.logger.info(f"Successfully removed bookmark for post {post_id} by user {user_id}")
        return jsonify({"message": "Successfully removed bookmark"}), 200

    except Error as e:
        current_app.logger.error(f"Database error in delete_bookmark: {str(e)}")
        return jsonify({"error": str(e)}), 500
