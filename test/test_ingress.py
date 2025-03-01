import os
from decimal import Decimal
from unittest.mock import patch

import boto3
import pytest

from src.util.ingress import ingress_handler
from src.util.get_secret import get_secret


@pytest.fixture(scope="function")
def aws_credentials():  # credentials required for testing
    os.environ["AWS_ACCESS_KEY_ID"] = "testing"
    os.environ["AWS_SECRET_ACCESS_KEY"] = "testing"
    os.environ["AWS_SECURITY_TOKEN"] = "testing"
    os.environ["AWS_SESSION_TOKEN"] = "testing"
    os.environ["AWS_DEFAULT_REGION"] = "eu-west-2"


secret_name = "Tote-DB"
region_name = "eu-west-2"

# Create a Secrets Manager client
session = boto3.session.Session()
client = session.client(service_name="secretsmanager", region_name=region_name)
db_details = get_secret(client, "Tote-DB")


@patch("src.util.pg_connection_aws.Connection.run")
def test_currency_data_query_returns_correct_scaffold(mock_query):
    # Arrange
    mock_query.return_value = [[1, "GBP"], [2, "USD"], [3, "EUR"]]
    expected_id_type = int
    expected_code_type = str
    # Act
    results = ingress_handler(db_details)
    # Assert

    for result in results[0]["currency"]:
        assert isinstance(result["currency_id"], expected_id_type)
        assert isinstance(result["currency_code"], expected_code_type)
        assert len(result) == 2
        assert len(result["currency_code"]) == 3


@patch("src.util.pg_connection_aws.Connection.run")
def test_staff_data_query_returns_correct_scaffold(mock_query):
    # Arrange
    mock_query.return_value = [
        [
            1,
            "Jeremie",
            "Franey",
            "Purchasing",
            "Manchester",
            "jeremie.franey@terrifictotes.com",
        ],
        [
            2,
            "Deron",
            "Beier",
            "Facilities",
            "Manchester",
            "deron.beier@terrifictotes.com",
        ],
        [
            3,
            "Jeanette",
            "Erdman",
            "Facilities",
            "Manchester",
            "jeanette.erdman@terrifictotes.com",
        ],
        [
            4,
            "Ana",
            "Glover",
            "Production",
            "Leeds",
            "ana.glover@terrifictotes.com",
        ],
        [
            5,
            "Magdalena",
            "Zieme",
            "HR",
            "Leeds",
            "magdalena.zieme@terrifictotes.com",
        ],
        [
            6,
            "Korey",
            "Kreiger",
            "Production",
            "Leeds",
            "korey.kreiger@terrifictotes.com",
        ],
        [
            7,
            "Raphael",
            "Rippin",
            "Purchasing",
            "Manchester",
            "raphael.rippin@terrifictotes.com",
        ],
        [
            8,
            "Oswaldo",
            "Bergstrom",
            "Communications",
            "Leeds",
            "oswaldo.bergstrom@terrifictotes.com",
        ],
        [
            9,
            "Brody",
            "Ratke",
            "Purchasing",
            "Manchester",
            "brody.ratke@terrifictotes.com",
        ],
        [
            10,
            "Jazmyn",
            "Kuhn",
            "Purchasing",
            "Manchester",
            "jazmyn.kuhn@terrifictotes.com",
        ],
        [
            11,
            "Meda",
            "Cremin",
            "Finance",
            "Manchester",
            "meda.cremin@terrifictotes.com",
        ],
        [
            12,
            "Imani",
            "Walker",
            "Finance",
            "Manchester",
            "imani.walker@terrifictotes.com",
        ],
        [
            13,
            "Stan",
            "Lehner",
            "Dispatch",
            "Leds",
            "stan.lehner@terrifictotes.com",
        ],
        [
            14,
            "Rigoberto",
            "VonRueden",
            "Communications",
            "Leeds",
            "rigoberto.vonrueden@terrifictotes.com",
        ],
        [
            15,
            "Tom",
            "Gutkowski",
            "Production",
            "Leeds",
            "tom.gutkowski@terrifictotes.com",
        ],
        [
            16,
            "Jett",
            "Parisian",
            "Facilities",
            "Manchester",
            "jett.parisian@terrifictotes.com",
        ],
        [
            17,
            "Irving",
            "O'Keefe",
            "Production",
            "Leeds",
            "irving.o'keefe@terrifictotes.com",
        ],
        [
            18,
            "Tomasa",
            "Moore",
            "HR",
            "Leeds",
            "tomasa.moore@terrifictotes.com",
        ],
        [
            19,
            "Pierre",
            "Sauer",
            "Purchasing",
            "Manchester",
            "pierre.sauer@terrifictotes.com",
        ],
        [
            20,
            "Flavio",
            "Kulas",
            "Production",
            "Leeds",
            "flavio.kulas@terrifictotes.com",
        ],
    ]
    expected_id_type = int
    expected_first_name_type = str
    expected_last_name_type = str
    expected_department_name_type = str
    expected_location_type = str
    expected_email_address_type = str
    # Act
    results = ingress_handler(db_details)
    # Assert
    for result in results[1]["staff"]:
        assert isinstance(result["staff_id"], expected_id_type)
        assert isinstance(result["first_name"], expected_first_name_type)
        assert isinstance(result["last_name"], expected_last_name_type)
        assert isinstance(
            result["department_name"], expected_department_name_type
        )
        assert isinstance(result["location"], expected_location_type)
        assert isinstance(result["email_address"], expected_email_address_type)
        assert len(result) == 6
        assert result["email_address"].count("@") == 1


@patch("src.util.pg_connection_aws.Connection.run")
def test_design_data_query_returns_correct_scaffold(mock_query):
    # Arrange
    mock_query.return_value = [
        [501, "Granite", "/boot/defaults", "granite-20240813-sy9h.json"],
        [502, "Soft", "/usr/share", "soft-20240427-lrgo.json"],
        [503, "Wooden", "/Library", "wooden-20230711-g1p6.json"],
        [504, "Rubber", "/net", "rubber-20240421-vwnu.json"],
        [505, "Rubber", "/home/user/dir", "rubber-20230214-lthc.json"],
        [506, "Plastic", "/private", "plastic-20231129-wt29.json"],
        [507, "Steel", "/usr/libexec", "steel-20231208-xd3t.json"],
        [508, "Soft", "/opt/sbin", "soft-20240119-f5pa.json"],
        [509, "Rubber", "/opt/share", "rubber-20240803-8001.json"],
        [510, "Granite", "/net", "granite-20240604-rf40.json"],
        [511, "Cotton", "/var", "cotton-20240908-x14e.json"],
        [512, "Concrete", "/var/log", "concrete-20240529-p6yn.json"],
        [513, "Bronze", "/private/tmp", "bronze-20231215-63zp.json"],
        [491, "Plastic", "/usr/bin", "plastic-20230622-xqn8.json"],
        [514, "Bronze", "/net", "bronze-20241111-n42p.json"],
        [515, "Frozen", "/opt", "frozen-20240526-5760.json"],
        [516, "Wooden", "/usr/X11R6", "wooden-20240310-8g72.json"],
        [517, "Concrete", "/usr/local/src", "concrete-20230215-8r2c.json"],
        [433, "Wooden", "/rescue", "wooden-20231202-ut83.json"],
        [518, "Metal", "/usr/include", "metal-20241223-8n78.json"],
        [519, "Frozen", "/opt/sbin", "frozen-20231001-6ial.json"],
        [520, "Metal", "/Applications", "metal-20230908-y5ik.json"],
        [521, "Rubber", "/usr/local/bin", "rubber-20230707-v6yy.json"],
        [522, "Wooden", "/private/tmp", "wooden-20240430-bbgo.json"],
        [523, "Bronze", "/etc/mail", "bronze-20231114-1j5u.json"],
        [524, "Frozen", "/lib", "frozen-20231128-3j1h.json"],
        [525, "Granite", "/srv", "granite-20241013-2zvo.json"],
        [526, "Cotton", "/home/user", "cotton-20240123-ny4x.json"],
        [527, "Concrete", "/var/mail", "concrete-20230312-eu7f.json"],
        [528, "Frozen", "/usr/ports", "frozen-20230216-praj.json"],
        [529, "Plastic", "/tmp", "plastic-20241201-5yh7.json"],
        [530, "Wooden", "/bin", "wooden-20230817-lnag.json"],
        [531, "Concrete", "/lib", "concrete-20240906-qml0.json"],
        [532, "Fresh", "/usr/local/bin", "fresh-20231112-zwlh.json"],
        [533, "Soft", "/usr/share", "soft-20240215-7glv.json"],
        [534, "Cotton", "/var", "cotton-20240817-jfav.json"],
        [535, "Rubber", "/var/log", "rubber-20240724-nndw.json"],
    ]
    expected_id_type = int
    expected_design_name_type = str
    expected_file_location_type = str
    expected_file_name_type = str
    # Act
    results = ingress_handler(db_details)
    # Assert
    for result in results[2]["design"]:
        assert isinstance(result["design_id"], expected_id_type)
        assert isinstance(result["design_name"], expected_design_name_type)
        assert isinstance(result["file_location"], expected_file_location_type)
        assert isinstance(result["file_name"], expected_file_name_type)
        assert len(result) == 4
        assert result["file_location"][0] == "/"
        assert "." in result["file_name"]


@patch("src.util.pg_connection_aws.Connection.run")
def test_address_data_query_returns_correct_scaffold(mock_query):
    # Arrange
    mock_query.return_value = [
        [
            26,
            "522 Pacocha Branch",
            None,
            "Bedfordshire",
            "Napa",
            "77211-4519",
            "American Samoa",
            "5794 359212",
        ],
        [
            27,
            "7212 Breitenberg View",
            "Nora Bridge",
            "Buckinghamshire",
            "Oakland Park",
            "77499",
            "Guam",
            "2949 665163",
        ],
        [
            28,
            "079 Horacio Landing",
            None,
            None,
            "Utica",
            "93045",
            "Austria",
            "7772 084705",
        ],
        [
            29,
            "37736 Heathcote Lock",
            "Noemy Pines",
            None,
            "Bartellview",
            "42400-5199",
            "Congo",
            "1684 702261",
        ],
        [
            30,
            "0336 Ruthe Heights",
            None,
            "Buckinghamshire",
            "Lake Myrlfurt",
            "94545-4284",
            "Falkland Islands (Malvinas)",
            "1083 286132",
        ],
    ]
    expected_id_type = int
    expected_al1_type = str
    expected_al2_type = str | None
    expected_district_type = str | None
    expected_city_type = str
    expected_postal_code_type = str
    expected_country_type = str
    expected_phone_type = str
    # Act
    results = ingress_handler(db_details)
    # Assert
    for result in results[3]["address"]:
        assert isinstance(result["address_id"], expected_id_type)
        assert isinstance(result["address_line_1"], expected_al1_type)
        assert isinstance(result["address_line_2"], expected_al2_type)
        assert isinstance(result["district"], expected_district_type)
        assert isinstance(result["city"], expected_city_type)
        assert isinstance(result["postal_code"], expected_postal_code_type)
        assert isinstance(result["country"], expected_country_type)
        assert isinstance(result["phone"], expected_phone_type)
        assert len(result) == 8


@patch("src.util.pg_connection_aws.Connection.run")
def test_counterparty_data_query_returns_correct_scaffold(mock_query):
    # Arrange
    mock_query.return_value = [
        [
            16,
            "Hartmann, Franecki and Ratke",
            "84824 Bryce Common",
            "Grady Turnpike",
            None,
            "Maggiofurt",
            "50899-1522",
            "Iraq",
            "3316 955887",
        ],
        [
            17,
            "Kihn Group",
            "962 Koch Drives",
            None,
            None,
            "Hackensack",
            "95316-4738",
            "Indonesia",
            "5507 549583",
        ],
        [
            18,
            "Smith and Sons",
            "962 Koch Drives",
            None,
            None,
            "Hackensack",
            "95316-4738",
            "Indonesia",
            "5507 549583",
        ],
        [
            19,
            "Ondricka, Conroy and Turcotte",
            "58805 Sibyl Cliff",
            "Leuschke Glens",
            "Bedfordshire",
            "Lake Arne",
            "63808",
            "Kiribati",
            "0168 407254",
        ],
        [
            20,
            "Yost, Watsica and Mann",
            "179 Alexie Cliffs",
            None,
            None,
            "Aliso Viejo",
            "99305-7380",
            "San Marino",
            "9621 880720",
        ],
    ]
    expected_id_type = int
    expected_legal_name_type = str
    expected_al1_type = str
    expected_al2_type = str | None
    expected_district_type = str | None
    expected_city_type = str
    expected_postal_code_type = str
    expected_country_type = str
    expected_phone_type = str
    # Act
    results = ingress_handler(db_details)
    # Assert
    for result in results[4]["counterparty"]:
        assert isinstance(result["counterparty_id"], expected_id_type)
        assert isinstance(
            result["counterparty_legal_name"], expected_legal_name_type
        )
        assert isinstance(result["address_line_1"], expected_al1_type)
        assert isinstance(result["address_line_2"], expected_al2_type)
        assert isinstance(result["district"], expected_district_type)
        assert isinstance(result["city"], expected_city_type)
        assert isinstance(result["postal_code"], expected_postal_code_type)
        assert isinstance(result["country"], expected_country_type)
        assert isinstance(result["phone"], expected_phone_type)
        assert len(result) == 9


@patch("src.util.pg_connection_aws.Connection.run")
def test_sales_data_query_returns_correct_scaffold(mock_query):
    # Arrange
    mock_query.return_value = [
        [
            12833,
            13,
            13,
            47241,
            Decimal("3.30"),
            2,
            360,
            "2025-03-02",
            "2025-02-28",
            16,
        ],
        [
            12834,
            20,
            10,
            50975,
            Decimal("2.48"),
            2,
            441,
            "2025-03-02",
            "2025-03-02",
            18,
        ],
        [
            12835,
            16,
            5,
            21962,
            Decimal("3.16"),
            1,
            354,
            "2025-02-27",
            "2025-03-02",
            5,
        ],
        [
            12836,
            20,
            3,
            80088,
            Decimal("3.45"),
            1,
            474,
            "2025-03-02",
            "2025-03-02",
            13,
        ],
        [
            12837,
            17,
            2,
            84063,
            Decimal("3.72"),
            1,
            210,
            "2025-03-02",
            "2025-03-01",
            8,
        ],
    ]
    expected_sales_order_id = int
    expected_staff_id = int
    expected_counterparty_id = int
    expected_units_sold = int
    expected_unit_price = str
    expected_currency_id = int
    expected_design_id = int
    expected_agreed_delivery_date = str
    expected_agreed_payment_date = str
    expected_agreed_delivery_location_id = int
    # Act
    results = ingress_handler(db_details)
    # Assert
    for result in results[5]["sales_order"]:
        assert isinstance(result["sales_order_id"], expected_sales_order_id)
        assert isinstance(result["staff_id"], expected_staff_id)
        assert isinstance(result["counterparty_id"], expected_counterparty_id)
        assert isinstance(result["units_sold"], expected_units_sold)
        assert isinstance(result["unit_price"], expected_unit_price)
        assert isinstance(result["currency_id"], expected_currency_id)
        assert isinstance(result["design_id"], expected_design_id)
        assert isinstance(
            result["agreed_delivery_date"], expected_agreed_delivery_date
        )
        assert isinstance(
            result["agreed_payment_date"], expected_agreed_payment_date
        )
        assert isinstance(
            result["agreed_delivery_location_id"],
            expected_agreed_delivery_location_id,
        )
        assert len(result) == 10
