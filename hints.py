from db import db


def get_latest():
    result = db.session.execute("""
        SELECT H.name, H.composer, H.id
        FROM Hint H, Categories C
        WHERE H.id = C.hint_id
        GROUP BY H.id
        ORDER BY H.sent_at DESC LIMIT 10""")
    tuple = [(item["id"], item["name"], item["composer"]) for item in result.fetchall()]
    return tuple

def get_hint(hint_id):
    result = db.session.execute("""
        SELECT composer, name, alternatives, link1, link2, link3, sent_at
        FROM Hint WHERE id=(:hint_id)""", 
        {"hint_id":hint_id})
    hint = result.fetchone()
    return hint

def get_hint_places(hint_id, occasion_id):
    result = db.session.execute("""
        SELECT DISTINCT P.name FROM Place P, Categories C 
        WHERE C.hint_id=(:hint_id) AND P.id=C.place_id AND C.occasion_id=(:occasion_id)""", 
        {"hint_id":hint_id, "occasion_id":occasion_id})
    places = result.fetchall()
    return places

def get_hint_styles(hint_id, occasion_id):
    result = db.session.execute("""
        SELECT DISTINCT S.name FROM Style S, Categories C 
        WHERE C.hint_id=(:hint_id) AND S.id=C.style_id AND C.occasion_id=(:occasion_id)""", 
        {"hint_id":hint_id, "occasion_id":occasion_id})
    styles = result.fetchall()
    return styles

def get_name_place(place_id):
    result = db.session.execute("SELECT name FROM Place WHERE id=(:place_id)", {"place_id":place_id})
    category = result.fetchone()
    return category

def get_name_style(style_id):
    result = db.session.execute("SELECT name FROM Style WHERE id=(:style_id)", {"style_id":style_id})
    category = result.fetchone()
    return category

def get_number_of_suggestions():
    result = db.session.execute("""
        SELECT SUM(c) AS total FROM 
        ((SELECT COUNT(DISTINCT hint_id) AS c FROM New_hint)
        UNION ALL 
        (SELECT COUNT(DISTINCT hint_id) AS c FROM Change_hint) 
        UNION ALL 
        (SELECT COUNT(*) AS c FROM Remove_hint)) 
        tables""")
    number = result.fetchone()[0]
    return number

def get_new():
    result = db.session.execute("""
        SELECT H.name, H.composer, H.id
        FROM Hint H, New_hint NH
        WHERE H.id = NH.hint_id
        GROUP BY H.id
        ORDER BY H.sent_at""")
    tuple = [(item["id"], item["name"], item["composer"]) for item in result.fetchall()]
    return tuple

def get_number_of_new():
    result = db.session.execute("SELECT COUNT(DISTINCT hint_id) FROM New_hint")
    number = result.fetchone()[0]
    return number

def get_new_places(hint_id, occasion_id):
    result = db.session.execute("""
        SELECT DISTINCT P.name FROM Place P, New_hint NH 
        WHERE NH.hint_id=(:hint_id) AND P.id=NH.place_id AND NH.occasion_id=(:occasion_id)""", 
        {"hint_id":hint_id, "occasion_id":occasion_id})
    new_places = result.fetchall()
    return new_places

def get_new_styles(hint_id, occasion_id):
    result = db.session.execute("""
        SELECT DISTINCT S.name FROM Style S, New_hint NH 
        WHERE NH.hint_id=(:hint_id) AND S.id=NH.style_id AND NH.occasion_id=(:occasion_id)""", 
        {"hint_id":hint_id, "occasion_id":occasion_id})
    new_styles = result.fetchall()
    return new_styles

def create_hint(composer, name, alternatives, link1, link2, link3):
    db.session.execute("""
        INSERT INTO Hint (composer, name, alternatives, link1, link2, link3, sent_at) 
        VALUES (:composer, :name, :alternatives, :link1, :link2, :link3, NOW())""",
        {"composer":composer, "name":name, "alternatives":alternatives, "link1":link1, "link2":link2, "link3":link3})
    added = db.session.execute("SELECT currval(pg_get_serial_sequence('Hint', 'id'))")
    hint_id = int(added.fetchone()[0])
    db.session.commit()
    return hint_id

def new_hint_categories(hint_id, occasion_id, place_id, style_id):
    db.session.execute("""
        INSERT INTO New_hint 
        VALUES (:hint_id, :occasion_id, :place_id, :style_id)""",
        {"hint_id":hint_id, "occasion_id":occasion_id, "place_id":place_id, "style_id":style_id})
    db.session.commit()

def set_categories_new(hint_id):
    db.session.execute("""
        INSERT INTO Categories
        SELECT hint_id, occasion_id, place_id, style_id FROM New_hint
        WHERE New_hint.hint_id=(:hint_id)""",
        {"hint_id":hint_id})
    db.session.commit()

def delete_new_hint(hint_id):
    db.session.execute("DELETE FROM New_hint WHERE hint_id=(:hint_id)", {"hint_id":hint_id})
    db.session.commit()

def delete_hint(hint_id):
    db.session.execute("DELETE FROM Hint WHERE id=(:hint_id)", {"hint_id":hint_id})
    db.session.commit()

def get_occasion_latest(occasion_id):
    result = db.session.execute("""
        SELECT H.id, H.name, H.composer 
        FROM Hint H, Categories C 
        WHERE H.id=C.hint_id AND C.occasion_id=(:occasion_id) 
        GROUP BY H.id 
        ORDER BY H.sent_at DESC""",
        {"occasion_id":occasion_id})
    tuple = [(item["id"], item["name"], item["composer"]) for item in result.fetchall()]
    return tuple
