import database
import config

schema = [
    (0, 
     """CREATE TABLE IF NOT EXISTS user (
           id int primary key auto_increment,
           username varchar(255) not null,
           password varchar(255) not null)"""),
     (1,
      """CREATE TABLE IF NOT EXISTS location (
           id int primary key auto_increment,
           name varchar(255) not null,
           address text null,
           lat double not null,
           lng double not null)""",
    ),
    (2,
     """CREATE TABLE IF NOT EXISTS user_location (
          user_id int not null,
          location_id int not null,
          key(user_id),
          key(location_id),
          primary key(user_id, location_id))"""
    ),
]

def create_schema_table(db):
    db.query("""CREATE TABLE IF NOT EXISTS schema_version (current_version int not null)""")

def get_current_version(db):
    create_schema_table(db)
    version = db.fetch_one("SELECT current_version FROM schema_version")
    if version is None:
        db.insert("schema_version", current_version=0)
        return 0
    return version[0]

def update_schema(db):
    current_version = get_current_version(db)
    schema_len = len(schema)
    for i in range(current_version, schema_len):
        db.query(schema[i][1])
        db.update("schema_version", None, current_version=i)

    if current_version != schema_len:
        db.update("schema_version", None, current_version=schema_len)
        

if __name__ == "__main__":
    db = database.MySQL()
    db.connect(config.production_db)
    update_schema(db)
    print "Schema has been updated!\n"
    
