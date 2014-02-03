def find_one_by(db, **value_pairs):
    condition_str = " AND ".join(["`" + k + "` = '" + v + "'" for (k, v) in value_pairs.iteritems()])
    query = "SELECT id, username FROM user WHERE " + condition_str
    row = db.fetch_one(query)
    if row is None:
        return row
    return {"id": row[0], "username": row[1]}
