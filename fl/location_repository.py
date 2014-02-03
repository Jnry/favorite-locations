def find_one_by(db, **values):
    condition_str = " AND ".join(["`" + k + "` = '" + str(v) + "'" for (k, v) in values.iteritems()])
    query = "SELECT id, name, address, lat, lng FROM location WHERE " + condition_str

    row = db.fetch_one(query)
    if row is None:
        return row
    return {"id": row[0], "name": row[1], "address": row[2], "lat": row[3], "lng": row[4]}

def find_by_user_id(db, user_id):
    query = """SELECT l.id, l.name, l.address, l.lat, l.lng
               FROM location l
               INNER JOIN user_location ul ON ul.location_id = l.id
               WHERE ul.user_id = %s"""
    rows = db.fetch_all(query, (user_id,))
    if rows is None:
        return rows
    return [{"id": row[0], "name": row[1], "address": row[2], "lat": row[3], "lng": row[4]} for row in rows]

def find_all(db):
    query = "SELECT id, name, address, lat, lng FROM location"

    rows = db.fetch_all(query)
    if rows is None:
        return rows
    return [{"id": row[0], "name": row[1], "address": row[2], "lat": row[3], "lng": row[4]} for row in rows]

def delete_by_id(db, id):
    db.delete("location", "id = " + id)
