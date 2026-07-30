import os
import psycopg2
import base64

from pathlib import Path
from dotenv import load_dotenv


# =====================================================
# LOAD .ENV
# =====================================================

BASE_DIR = Path(__file__).resolve().parent.parent

ENV_FILE = BASE_DIR / ".env"

loaded = load_dotenv(
    dotenv_path=ENV_FILE,
    override=True
)


print("ENV PATH:")
print(ENV_FILE)

print("ENV LOADED:")
print(loaded)

print(
    "PASSWORD CHECK:",
    os.getenv("POSTGRES_PASSWORD_ENCRYPTED")
)


# =====================================================
# PASSWORD DECRYPT
# =====================================================

def decrypt_password(encoded_password):

    if not encoded_password:
        raise Exception(
            "Encrypted password missing"
        )

    decoded = base64.b64decode(
        encoded_password
    )

    return decoded.decode("utf-8")



# =====================================================
# DATABASE CONNECTION
# =====================================================

def get_connection():


    encrypted_password = os.getenv(
        "POSTGRES_PASSWORD_ENCRYPTED"
    )


    if encrypted_password is None:

        raise Exception(
            "POSTGRES_PASSWORD_ENCRYPTED not found in .env"
        )



    password = decrypt_password(
        encrypted_password
    )


    print(
        "Connecting to PostgreSQL..."
    )


    conn = psycopg2.connect(

        host=os.getenv(
            "POSTGRES_HOST"
        ),

        database=os.getenv(
            "POSTGRES_DB"
        ),

        user=os.getenv(
            "POSTGRES_USER"
        ),

        password=password,

        port=os.getenv(
            "POSTGRES_PORT"
        )

    )


    return conn




# =====================================================
# CREATE TABLE
# =====================================================

def create_table():


    conn = get_connection()

    cursor = conn.cursor()


    cursor.execute(
        """
        CREATE TABLE IF NOT EXISTS traffic_data
        (

            id SERIAL PRIMARY KEY,

            date_time TIMESTAMP,

            car_count INTEGER DEFAULT 0,

            scooter_count INTEGER DEFAULT 0,

            bus_count INTEGER DEFAULT 0,

            truck_count INTEGER DEFAULT 0,

            overspeed_count INTEGER DEFAULT 0

        );
        """
    )


    conn.commit()


    cursor.close()

    conn.close()


    print(
        "traffic_data table ready"
    )




# =====================================================
# INSERT DATA
# =====================================================

def save_traffic_data(
        date_time,
        vehicles,
        overspeed_count
):


    conn = get_connection()

    cursor = conn.cursor()


    cursor.execute(

        """
        INSERT INTO traffic_data
        (
            date_time,
            car_count,
            scooter_count,
            bus_count,
            truck_count,
            overspeed_count
        )

        VALUES
        (%s,%s,%s,%s,%s,%s)

        """,

        (

            date_time,

            vehicles.get(
                "Car",
                0
            ),

            vehicles.get(
                "Motorcycle",
                0
            ),

            vehicles.get(
                "Bus",
                0
            ),

            vehicles.get(
                "Truck",
                0
            ),

            overspeed_count

        )

    )


    conn.commit()


    cursor.close()

    conn.close()


    print(
        "Traffic data inserted successfully"
    )