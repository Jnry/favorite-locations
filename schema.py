import database
import config

schema = [
    (0, 
     """CREATE TABLE IF NOT EXISTS user (
           id integer primary key auto_increment,
           title varchar(255) null,
           firstname varchar(255) null,
           lastname varchar(255) null)"""),
     (1,
      """CREATE TABLE IF NOT EXISTS location (
           id integer primary key auto_increment,
           name varchar(255) not null,
           address text null,
           lat decimal(6, 3) not null,
           lng decimal(6, 3) not null)""",
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
    
