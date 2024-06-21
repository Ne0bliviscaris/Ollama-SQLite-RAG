import db

# Manual query test
db.sql_query(
    """
SELECT DISTINCT p.name AS witness_name, c.city AS crime_location
    FROM crime_scene_report AS c
    JOIN (SELECT * FROM person WHERE address_street_name = 'Northwestern Dr' AND address_number = (SELECT MAX(address_number) FROM person WHERE address_street_name = 'Northwestern Dr')) AS p1
    ON c.city = p1.city
    JOIN (SELECT * FROM person WHERE name = 'Annabel') AS p2
    ON c.city = p2.city;
"""
)
