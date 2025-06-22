from bson import ObjectId
from conections.mongo import conection_mongo

def delete_publication(publication_id):
    try:
        db = conection_mongo()
        publications_collection = db["Publications"]

        try:
            obj_id = ObjectId(publication_id)
        except Exception:
            return {"error": "Invalid ObjectId format"}, 400

        result = publications_collection.update_one(
            {"_id": obj_id},
            {"$set": {"Status": 0}}
        )

        if result.matched_count == 0:
            return {"error": "Publication not found"}, 404

        return {"message": "Publication deleted successfully"}, 200

    except Exception as e:
        return {"error": f"Internal server error: {str(e)}"}, 500
