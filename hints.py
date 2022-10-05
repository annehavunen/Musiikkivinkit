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

def get_places(hint_id, occasion_id):
    result = db.session.execute("""
        SELECT DISTINCT place_id FROM Categories WHERE hint_id=(:hint_id) AND occasion_id=(:occasion_id)""",
        {"hint_id":hint_id, "occasion_id":occasion_id})
    selected = result.fetchall()
    return selected

def get_styles(hint_id, occasion_id):
    result = db.session.execute("""
        SELECT DISTINCT style_id FROM Categories WHERE hint_id = (:hint_id) AND occasion_id=(:occasion_id)""",
        {"hint_id":hint_id, "occasion_id":occasion_id})    
    selected = result.fetchall()
    return selected

def get_number_of_suggestions():
    result = db.session.execute("""
        SELECT SUM(c) AS total FROM 
        ((SELECT COUNT(DISTINCT hint_id) AS c FROM New_suggestion)
        UNION ALL 
        (SELECT COUNT(DISTINCT hint_id) AS c FROM Change_suggestion) 
        UNION ALL 
        (SELECT COUNT(*) AS c FROM Remove_suggestion)) 
        tables""")
    number = result.fetchone()[0]
    return number

def get_number_of_new():
    result = db.session.execute("SELECT COUNT(DISTINCT hint_id) FROM New_suggestion")
    number = result.fetchone()[0]
    return number

def get_number_of_changed():
    result = db.session.execute("SELECT COUNT(DISTINCT hint_id) FROM Change_suggestion")
    number = result.fetchone()[0]
    return number

def get_number_of_removed():
    result = db.session.execute("SELECT COUNT(DISTINCT hint_id) FROM Remove_suggestion")
    number = result.fetchone()[0]
    return number

def get_new_suggestions():
    result = db.session.execute("""
        SELECT H.name, H.composer, H.id
        FROM Hint H, New_suggestion NS
        WHERE H.id = NS.hint_id
        GROUP BY H.id
        ORDER BY H.sent_at""")
    tuple = [(item["id"], item["name"], item["composer"]) for item in result.fetchall()]
    return tuple

def get_change_suggestions():
    result = db.session.execute("""
        SELECT H.name, H.composer, H.id
        FROM Hint H, Change_suggestion CS
        WHERE H.id = CS.hint_id
        GROUP BY H.id
        ORDER BY H.sent_at""")
    tuple = [(item["id"], item["name"], item["composer"]) for item in result.fetchall()]
    return tuple

def get_remove_suggestions():
    result = db.session.execute("""
        SELECT H.name, H.composer, RS.id
        FROM Hint H, Remove_suggestion RS
        WHERE H.id = RS.hint_id
        ORDER BY H.sent_at""")
    tuple = [(item["id"], item["name"], item["composer"]) for item in result.fetchall()]
    return tuple

def get_previous_id(hint_id):
    result = db.session.execute("SELECT DISTINCT old_id FROM Change_suggestion WHERE hint_id=(:hint_id)", {"hint_id":hint_id})
    old_id = result.fetchone()[0]
    return old_id

def get_changed_places(hint_id, occasion_id):
    result = db.session.execute("""
        SELECT DISTINCT P.name FROM Place P, Change_suggestion CS 
        WHERE CS.hint_id=(:hint_id) AND P.id=CS.place_id AND CS.occasion_id=(:occasion_id)""", 
        {"hint_id":hint_id, "occasion_id":occasion_id})
    changed_places = result.fetchall()
    return changed_places

def get_changed_styles(hint_id, occasion_id):
    result = db.session.execute("""
        SELECT DISTINCT S.name FROM Style S, Change_suggestion CS 
        WHERE CS.hint_id=(:hint_id) AND S.id=CS.style_id AND CS.occasion_id=(:occasion_id)""", 
        {"hint_id":hint_id, "occasion_id":occasion_id})
    changed_styles = result.fetchall()
    return changed_styles

def get_new_places(hint_id, occasion_id):
    result = db.session.execute("""
        SELECT DISTINCT P.name FROM Place P, New_suggestion NS 
        WHERE NS.hint_id=(:hint_id) AND P.id=NS.place_id AND NS.occasion_id=(:occasion_id)""", 
        {"hint_id":hint_id, "occasion_id":occasion_id})
    new_places = result.fetchall()
    return new_places

def get_new_styles(hint_id, occasion_id):
    result = db.session.execute("""
        SELECT DISTINCT S.name FROM Style S, New_suggestion NS 
        WHERE NS.hint_id=(:hint_id) AND S.id=NS.style_id AND NS.occasion_id=(:occasion_id)""", 
        {"hint_id":hint_id, "occasion_id":occasion_id})
    new_styles = result.fetchall()
    return new_styles

def get_place_names(hint_id, occasion_id):
    result = db.session.execute("""
        SELECT DISTINCT P.name FROM Place P, Categories C 
        WHERE C.hint_id=(:hint_id) AND P.id=C.place_id AND C.occasion_id=(:occasion_id)""", 
        {"hint_id":hint_id, "occasion_id":occasion_id})
    places = result.fetchall()
    return places

def get_style_names(hint_id, occasion_id):
    result = db.session.execute("""
        SELECT DISTINCT S.name FROM Style S, Categories C 
        WHERE C.hint_id=(:hint_id) AND S.id=C.style_id AND C.occasion_id=(:occasion_id)""", 
        {"hint_id":hint_id, "occasion_id":occasion_id})
    styles = result.fetchall()
    return styles

def create_hint(composer, name, alternatives, link1, link2, link3):
    db.session.execute("""
        INSERT INTO Hint (composer, name, alternatives, link1, link2, link3, sent_at) 
        VALUES (:composer, :name, :alternatives, :link1, :link2, :link3, NOW())""",
        {"composer":composer, "name":name, "alternatives":alternatives, "link1":link1, "link2":link2, "link3":link3})
    added = db.session.execute("SELECT currval(pg_get_serial_sequence('Hint', 'id'))")
    hint_id = int(added.fetchone()[0])
    db.session.commit()
    return hint_id

def create_new_suggestion(hint_id, occasion_id, place_id, style_id):
    db.session.execute("""
        INSERT INTO New_suggestion 
        VALUES (:hint_id, :occasion_id, :place_id, :style_id)""",
        {"hint_id":hint_id, "occasion_id":occasion_id, "place_id":place_id, "style_id":style_id})
    db.session.commit()

def create_remove_suggestion(hint_id, reason):
    db.session.execute("""
        INSERT INTO Remove_suggestion (hint_id, reason) 
        VALUES (:hint_id, :reason)""",
        {"hint_id":hint_id, "reason":reason})
    db.session.commit()

def set_categories_new(hint_id):
    db.session.execute("""
        INSERT INTO Categories
        SELECT hint_id, occasion_id, place_id, style_id FROM New_suggestion
        WHERE New_suggestion.hint_id=(:hint_id)""",
        {"hint_id":hint_id})
    db.session.commit()

def delete_new_suggestion(hint_id):
    db.session.execute("DELETE FROM New_suggestion WHERE hint_id=(:hint_id)", {"hint_id":hint_id})
    db.session.commit()

def delete_hint(hint_id):
    db.session.execute("DELETE FROM Hint WHERE id=(:hint_id)", {"hint_id":hint_id})
    db.session.commit()

def create_change_suggestion(old_id, new_id, occasion_id, place_id, style_id):
    db.session.execute("""
        INSERT INTO Change_suggestion VALUES (:old_id, :hint_id, :occasion_id, :place_id, :style_id)""",
        {"old_id":old_id, "hint_id":new_id, "occasion_id":occasion_id, "place_id":place_id, "style_id":style_id})
    db.session.commit()

def get_old_id(hint_id):
    result = db.session.execute("SELECT DISTINCT old_id FROM Change_suggestion WHERE hint_id=(:hint_id)", {"hint_id":hint_id})
    old_id = result.fetchone()[0]
    return old_id

def set_categories_changed(hint_id):
    db.session.execute("""
        INSERT INTO Categories (hint_id, occasion_id, place_id, style_id)
        SELECT hint_id, occasion_id, place_id, style_id
        FROM Change_suggestion
        WHERE Change_suggestion.hint_id=(:hint_id)""",
        {"hint_id":hint_id})
    db.session.commit()

def delete_change_suggestion(hint_id):
    db.session.execute("DELETE FROM Change_suggestion WHERE hint_id=(:hint_id)", {"hint_id":hint_id})
    db.session.commit()

def update_change_suggestions(hint_id, old_id):
    db.session.execute("""
        UPDATE Change_suggestion
        SET old_id=(:hint_id)
        WHERE old_id=(:old_id)""",
        {"hint_id":hint_id, "old_id":old_id})
    db.session.commit()

def delete_categories(id):
    db.session.execute("DELETE FROM Categories WHERE hint_id=(:hint_id)", {"hint_id":id})
    db.session.commit()

def update_remove_suggestions(hint_id, old_id):
    db.session.execute("UPDATE Remove_suggestion SET hint_id=(:hint_id) WHERE hint_id=(:old_id)", {"hint_id":hint_id, "old_id":old_id})
    db.session.commit()

def get_removed_hint(remove_id):
    result = db.session.execute("SELECT hint_id, reason FROM Remove_suggestion WHERE id=(:remove_id)", {"remove_id":remove_id})
    remove = result.fetchall()
    hint_id = remove[0][0]
    reason = remove[0][1]
    return hint_id, reason

def delete_remove_suggestion(hint_id):
    db.session.execute("DELETE FROM Remove_suggestion WHERE hint_id=(:hint_id)", {"hint_id":hint_id})
    db.session.commit()

def get_change_suggestions_by_id(hint_id):
    result = db.session.execute("SELECT DISTINCT hint_id FROM Change_suggestion WHERE old_id=(:hint_id)", {"hint_id":hint_id})
    suggestions = result.fetchall()
    return suggestions

def search(query):
    result = db.session.execute("""
        SELECT H.name, H.composer, H.id
        FROM Hint H, Categories C
        WHERE H.id = C.hint_id
        AND (LOWER(name) LIKE LOWER(:query) 
        OR LOWER(composer) LIKE LOWER(:query) 
        OR LOWER(alternatives) LIKE LOWER(:query))
        GROUP BY H.id""",
        {"query":"%"+query+"%"})
    tuple = [(item["id"], item["name"], item["composer"]) for item in result.fetchall()]
    return tuple

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

def get_occasion_oldest(occasion_id):
    result = db.session.execute("""
        SELECT H.id, H.name, H.composer 
        FROM Hint H, Categories C 
        WHERE H.id=C.hint_id AND C.occasion_id=(:occasion_id) 
        GROUP BY H.id 
        ORDER BY H.sent_at""",
        {"occasion_id":occasion_id})
    tuple = [(item["id"], item["name"], item["composer"]) for item in result.fetchall()]
    return tuple

def get_occasion_composer(occasion_id):
    result = db.session.execute("""
        SELECT H.id, H.name, H.composer 
        FROM Hint H, Categories C 
        WHERE H.id=C.hint_id AND C.occasion_id=(:occasion_id) 
        GROUP BY H.id 
        ORDER BY H.composer""",
        {"occasion_id":occasion_id})
    tuple = [(item["id"], item["name"], item["composer"]) for item in result.fetchall()]
    return tuple

def get_occasion_composer_reversed(occasion_id):
    result = db.session.execute("""
        SELECT H.id, H.name, H.composer 
        FROM Hint H, Categories C 
        WHERE H.id=C.hint_id AND C.occasion_id=(:occasion_id) 
        GROUP BY H.id 
        ORDER BY H.composer DESC""",
        {"occasion_id":occasion_id})    
    tuple = [(item["id"], item["name"], item["composer"]) for item in result.fetchall()]
    return tuple

def get_occasion_name(occasion_id):
    result = db.session.execute("""
        SELECT H.id, H.name, H.composer 
        FROM Hint H, Categories C 
        WHERE H.id=C.hint_id AND C.occasion_id=(:occasion_id) 
        GROUP BY H.id 
        ORDER BY H.name""",
        {"occasion_id":occasion_id})
    tuple = [(item["id"], item["name"], item["composer"]) for item in result.fetchall()]
    return tuple

def get_occasion_name_reversed(occasion_id):
    result = db.session.execute("""
        SELECT H.id, H.name, H.composer 
        FROM Hint H, Categories C 
        WHERE H.id=C.hint_id AND C.occasion_id=(:occasion_id)
        GROUP BY H.id 
        ORDER BY H.name DESC""",
        {"occasion_id":occasion_id})
    tuple = [(item["id"], item["name"], item["composer"]) for item in result.fetchall()]
    return tuple

def get_style_latest(occasion_id, style_id):
    result = db.session.execute("""
        SELECT H.id, H.name, H.composer 
        FROM Hint H, Categories C 
        WHERE H.id=C.hint_id AND C.occasion_id=(:occasion_id) AND C.style_id=(:style_id) 
        GROUP BY H.id 
        ORDER BY H.sent_at DESC""",
        {"style_id":style_id, "occasion_id":occasion_id})
    tuple = [(item["id"], item["name"], item["composer"]) for item in result.fetchall()]
    return tuple

def get_style_oldest(occasion_id, style_id):
    result = db.session.execute("""
        SELECT H.id, H.name, H.composer 
        FROM Hint H, Categories C 
        WHERE H.id=C.hint_id AND C.occasion_id=(:occasion_id) AND C.style_id=(:style_id) 
        GROUP BY H.id 
        ORDER BY H.sent_at""",
        {"style_id":style_id, "occasion_id":occasion_id})
    tuple = [(item["id"], item["name"], item["composer"]) for item in result.fetchall()]
    return tuple

def get_style_composer(occasion_id, style_id):
    result = db.session.execute("""
        SELECT H.id, H.name, H.composer 
        FROM Hint H, Categories C 
        WHERE H.id=C.hint_id AND C.occasion_id=(:occasion_id) AND C.style_id=(:style_id) 
        GROUP BY H.id 
        ORDER BY H.composer""",
        {"style_id":style_id, "occasion_id":occasion_id})
    tuple = [(item["id"], item["name"], item["composer"]) for item in result.fetchall()]
    return tuple

def get_style_composer_reversed(occasion_id, style_id):
    result = db.session.execute("""
        SELECT H.id, H.name, H.composer 
        FROM Hint H, Categories C 
        WHERE H.id=C.hint_id AND C.occasion_id=(:occasion_id) AND C.style_id=(:style_id) 
        GROUP BY H.id 
        ORDER BY H.composer DESC""",
        {"style_id":style_id, "occasion_id":occasion_id})
    tuple = [(item["id"], item["name"], item["composer"]) for item in result.fetchall()]
    return tuple

def get_style_name(occasion_id, style_id):
    result = db.session.execute("""
        SELECT H.id, H.name, H.composer 
        FROM Hint H, Categories C 
        WHERE H.id=C.hint_id AND C.occasion_id=(:occasion_id) AND C.style_id=(:style_id) 
        GROUP BY H.id 
        ORDER BY H.name""",
        {"style_id":style_id, "occasion_id":occasion_id})
    tuple = [(item["id"], item["name"], item["composer"]) for item in result.fetchall()]
    return tuple

def get_style_name_reversed(occasion_id, style_id):
    result = db.session.execute("""
        SELECT H.id, H.name, H.composer 
        FROM Hint H, Categories C 
        WHERE H.id=C.hint_id AND C.occasion_id=(:occasion_id) AND C.style_id=(:style_id) 
        GROUP BY H.id 
        ORDER BY H.name DESC""",
        {"style_id":style_id, "occasion_id":occasion_id})
    tuple = [(item["id"], item["name"], item["composer"]) for item in result.fetchall()]
    return tuple

def get_place_latest(occasion_id, place_id):
    result = db.session.execute("""
        SELECT H.id, H.name, H.composer 
        FROM Hint H, Categories C 
        WHERE H.id=C.hint_id AND C.occasion_id=(:occasion_id) AND C.place_id=(:place_id)
        GROUP BY H.id
        ORDER BY H.sent_at DESC""", 
        {"place_id":place_id, "occasion_id":occasion_id}) 
    tuple = [(item["id"], item["name"], item["composer"]) for item in result.fetchall()]
    return tuple

def get_place_oldest(occasion_id, place_id):
    result = db.session.execute("""
        SELECT H.id, H.name, H.composer 
        FROM Hint H, Categories C 
        WHERE H.id=C.hint_id AND C.occasion_id=(:occasion_id) AND C.place_id=(:place_id)
        GROUP BY H.id
        ORDER BY H.sent_at""", 
        {"place_id":place_id, "occasion_id":occasion_id})
    tuple = [(item["id"], item["name"], item["composer"]) for item in result.fetchall()]
    return tuple

def get_place_composer(occasion_id, place_id):
    result = db.session.execute("""
        SELECT H.id, H.name, H.composer 
        FROM Hint H, Categories C 
        WHERE H.id=C.hint_id AND C.occasion_id=(:occasion_id) AND C.place_id=(:place_id)
        GROUP BY H.id
        ORDER BY H.composer""", 
        {"place_id":place_id, "occasion_id":occasion_id})
    tuple = [(item["id"], item["name"], item["composer"]) for item in result.fetchall()]
    return tuple

def get_place_composer_reversed(occasion_id, place_id):
    result = db.session.execute("""
        SELECT H.id, H.name, H.composer 
        FROM Hint H, Categories C 
        WHERE H.id=C.hint_id AND C.occasion_id=(:occasion_id) AND C.place_id=(:place_id)
        GROUP BY H.id
        ORDER BY H.composer DESC""", 
        {"place_id":place_id, "occasion_id":occasion_id}) 
    tuple = [(item["id"], item["name"], item["composer"]) for item in result.fetchall()]
    return tuple

def get_place_name(occasion_id, place_id):
    result = db.session.execute("""
        SELECT H.id, H.name, H.composer 
        FROM Hint H, Categories C 
        WHERE H.id=C.hint_id AND C.occasion_id=(:occasion_id) AND C.place_id=(:place_id)
        GROUP BY H.id
        ORDER BY H.name""", 
        {"place_id":place_id, "occasion_id":occasion_id})
    tuple = [(item["id"], item["name"], item["composer"]) for item in result.fetchall()]
    return tuple

def get_place_name_reversed(occasion_id, place_id):
    result = db.session.execute("""
        SELECT H.id, H.name, H.composer 
        FROM Hint H, Categories C 
        WHERE H.id=C.hint_id AND C.occasion_id=(:occasion_id) AND C.place_id=(:place_id)
        GROUP BY H.id)
        ORDER BY H.name DESC""", 
        {"place_id":place_id, "occasion_id":occasion_id})
    tuple = [(item["id"], item["name"], item["composer"]) for item in result.fetchall()]
    return tuple

def get_place_style_latest(occasion_id, place_id, style_id):
    result = db.session.execute("""
        SELECT H.id, H.name, H.composer 
        FROM Hint H, Categories C 
        WHERE H.id=C.hint_id AND C.occasion_id=(:occasion_id) AND C.place_id=(:place_id) AND C.style_id=(:style_id)
        GROUP BY H.id
        ORDER BY H.sent_at DESC""", 
        {"place_id":place_id, "style_id":style_id, "occasion_id":occasion_id})
    tuple = [(item["id"], item["name"], item["composer"]) for item in result.fetchall()]
    return tuple

def get_place_style_oldest(occasion_id, place_id, style_id):
    result = db.session.execute("""
        SELECT H.id, H.name, H.composer 
        FROM Hint H, Categories C 
        WHERE H.id=C.hint_id AND C.occasion_id=(:occasion_id) AND C.place_id=(:place_id) AND C.style_id=(:style_id)
        GROUP BY H.id
        ORDER BY H.sent_at""", 
        {"place_id":place_id, "style_id":style_id, "occasion_id":occasion_id})
    tuple = [(item["id"], item["name"], item["composer"]) for item in result.fetchall()]
    return tuple

def get_place_style_composer(occasion_id, place_id, style_id):
    result = db.session.execute("""
        SELECT H.id, H.name, H.composer 
        FROM Hint H, Categories C 
        WHERE H.id=C.hint_id AND C.occasion_id=(:occasion_id) AND C.place_id=(:place_id) AND C.style_id=(:style_id)
        GROUP BY H.id
        ORDER BY H.composer""", 
        {"place_id":place_id, "style_id":style_id, "occasion_id":occasion_id})
    tuple = [(item["id"], item["name"], item["composer"]) for item in result.fetchall()]
    return tuple

def get_place_style_composer_reversed(occasion_id, place_id, style_id):
    result = db.session.execute("""
        SELECT H.id, H.name, H.composer 
        FROM Hint H, Categories C 
        WHERE H.id=C.hint_id AND C.occasion_id=(:occasion_id) AND C.place_id=(:place_id) AND C.style_id=(:style_id)
        GROUP BY H.id
        ORDER BY H.composer DESC""", 
        {"place_id":place_id, "style_id":style_id, "occasion_id":occasion_id})
    tuple = [(item["id"], item["name"], item["composer"]) for item in result.fetchall()]
    return tuple

def get_place_style_name(occasion_id, place_id, style_id):
    result = db.session.execute("""
        SELECT H.id, H.name, H.composer 
        FROM Hint H, Categories C 
        WHERE H.id=C.hint_id AND C.occasion_id=(:occasion_id) AND C.place_id=(:place_id) AND C.style_id=(:style_id)
        GROUP BY H.id
        ORDER BY H.name""", 
        {"place_id":place_id, "style_id":style_id, "occasion_id":occasion_id})
    tuple = [(item["id"], item["name"], item["composer"]) for item in result.fetchall()]
    return tuple

def get_place_style_name_reversed(occasion_id, place_id, style_id):
    result = db.session.execute("""
        SELECT H.id, H.name, H.composer 
        FROM Hint H, Categories C 
        WHERE H.id=C.hint_id AND C.occasion_id=(:occasion_id) AND C.place_id=(:place_id) AND C.style_id=(:style_id)
        GROUP BY H.id
        ORDER BY H.name DESC""", 
        {"place_id":place_id, "style_id":style_id, "occasion_id":occasion_id})
    tuple = [(item["id"], item["name"], item["composer"]) for item in result.fetchall()]
    return tuple
