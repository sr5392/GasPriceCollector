
import sqlite3

class Database:
    """Represents a class to interact with the database"""

    def __init__(self, path: str) -> None:
        self._path = path
        self._name = "gas_station_prices.db"
      
        self._connection = sqlite3.connect(self._path + self._name)
        self._cursor = self._connection.cursor()

        self._initialize_database()
     
    def __enter__(self) -> None:
        return self

    def __exit__(self, exception_type, exception_value, exception_traceback) -> None:     
        self._commit()
        self._connection.close()

    def _commit(self) -> None:
        """Save all changes to the database"""
        self._connection.commit()
        
    def _execute(self, sql: str, parameters: tuple=None) -> None:
        """Execute a single SQL statement"""
        self._cursor.execute(sql, parameters or ())

    def _executemany(self, sql: str, parameters: tuple =None) -> None:
        """Execute multiple SQL statements"""
        self._cursor.executemany(sql, parameters or [()])

    def _query(self, sql, parameters: tuple=None) -> list:
        """Execute a single SQL statement and return all rows"""
        self._cursor.execute(sql, parameters or ())
        return self._cursor.fetchall()

    def insert_gas_station(self, station_id: str, station_details: list) -> None:
        """Insert the gas station details into the gas station table of the database"""
        name = station_details["brand"]
        street = station_details["street"]
        house_number = station_details["houseNumber"]
        place = station_details["place"]
        postal_code = station_details["postCode"]

        sql = "INSERT INTO gasstations (id, name, street, housenumber, place, postalcode) VALUES (?, ?, ?, ?, ?, ?);"
        self._execute(sql, (station_id, name, street, house_number, place, postal_code))

    def insert_gas_prices(self, gas_prices: dict, insert_date: str, insert_time: str) -> None:
        """Insert the gas prices into the gasprices table of the database"""
        for station_id in gas_prices:

            status = gas_prices[station_id]["status"]
            if status == "open":
                price_e5 = gas_prices[station_id]["e5"]
                price_e10 = gas_prices[station_id]["e10"]
                price_diesel = gas_prices[station_id]["diesel"]

                sql = "INSERT INTO gasprices (stationid, gastypeid, date, time, price) VALUES (?, ?, ?, ?, ?);"

                if price_e5:
                    self._execute(sql, (station_id, 1, insert_date, insert_time, price_e5))
                if price_e10:
                    self._execute(sql, (station_id, 2, insert_date, insert_time, price_e10))
                if price_diesel:
                    self._execute(sql, (station_id, 3, insert_date, insert_time, price_diesel))
                
                self._commit()

    def _create_tables(self) -> None:
        """Create all needed SQL tables in the database if they do not already exist"""
        self._create_table_gastypes()
        self._create_table_gasstations()
        self._create_table_gasprices()

    def _create_table_gasstations(self) -> None:
        """Create table for gas stations in the database if it does not already exist"""

        sql = """CREATE TABLE IF NOT EXISTS "gasstations" (
            "id" TEXT NOT NULL UNIQUE,
            "name" TEXT,
            "street" TEXT,
            "housenumber" TEXT,
            "place" TEXT,
            "postalcode" TEXT,
            PRIMARY KEY ("id"),
            UNIQUE ("street", "housenumber", "place", "postalcode")
            );"""

        self._execute(sql)

    def _create_table_gastypes(self) -> None:
        """Create table for gas types in the database if it does not already exist"""

        sql = """CREATE TABLE IF NOT EXISTS "gastypes" (
            "id" INTEGER NOT NULL UNIQUE,
            "name" TEXT UNIQUE,
            PRIMARY KEY ("id")
            );"""

        self._execute(sql)

    def _create_table_gasprices(self) -> None:
        """Create table for gas prices in the database if it does not already exist"""

        sql = """CREATE TABLE IF NOT EXISTS "gasprices" (
            "stationid" INTEGER NOT NULL,
            "gastypeid" INTEGER NOT NULL,
            "date" TEXT NOT NULL,
            "time" TEXT NOT NULL,
            "price" REAL,
            PRIMARY KEY ("stationid", "gastypeid", "date", "time"),
            FOREIGN KEY ("stationid") REFERENCES "gasstations" ("id"),
            FOREIGN KEY ("gastypeid") REFERENCES "gastypes" ("id")
            );"""

        self._execute(sql)

    def _insert_gas_types(self) -> None:
        """Insert the different gas types into the gas type table of the database if they do not already exist"""
        gas_types = [
            (1, "e5"),
            (2, "e10"),
            (3, "diesel")
            ]

        sql = "REPLACE INTO gastypes (id, name) VALUES (?, ?);"
        self._executemany(sql, gas_types)

    def _enable_foreign_keys(self) -> None:
        """Enable foreign keys constraints in the database"""
        sql = "PRAGMA foreign_keys = ON;"
        self._execute(sql)

    def _initialize_database(self) -> None:
        """Initialize the database"""
        self._enable_foreign_keys()
        self._create_tables()
        self._insert_gas_types()
        self._commit()

    def gas_station_exists(self, station_id: str) -> bool:
        """Check if the gas station table of the database already contains a gas station"""
        sql = "SELECT EXISTS (SELECT * FROM gasstations WHERE id = ?);"
        return self._query(sql, (station_id,))[0][0]
    

