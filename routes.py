from flask import render_template, redirect, request
from app import app
import string
import hints, users


@app.route("/")
def index():
    elements = hints.get_latest()
    latest = []
    for hint_id, name, composer in elements:
        latest.append((name, composer, f"/page/{hint_id}"))
    return render_template("index.html", latest=latest)

@app.route("/loginpage")
def loginpage():
    return render_template("loginpage.html")

@app.route("/login", methods=["POST"])
def login():
    username = request.form["username"]
    password = request.form["password"]
    if users.login(username, password):
        return redirect("/")
    return render_template("error.html", error="Väärä tunnus tai salasana")

@app.route("/logout")
def logout():
    users.logout()
    return redirect("/")

@app.route("/registerpage")
def registerpage():
    error = ""
    return render_template("registerpage.html", error=error)

@app.route("/register", methods=["POST"])
def register():
    username = request.form["username"]
    password1 = request.form["password1"]
    password2 = request.form["password2"]
    error = ""
    if not username:
        error = "Lisää käyttäjätunnus."
    elif len(username) > 50:
        error = "Käyttäjätunnus on liian pitkä."
    elif username[0] == " " or username[len(username)-1] == " ":
        error = "Käyttäjätunnus ei saa alkaa eikä päättyä välilyönnillä."
    elif password1 != password2:
        error = "Salasanat eroavat."
    elif not password1:
        error = "Lisää salasana."
    elif len(password1) > 100:
        error = "Salasana on liian pitkä."
    elif not accept_password(password1):
        error = "Salasana ei täytä kriteerejä."
    if error:
        return render_template("error.html", error=error)
    if users.register(username, password1):
        return redirect("/")
    return render_template("registerpage.html", error="Käyttäjätunnus on jo käytössä.")

@app.route("/page/<int:id>")
def page(id):
    hint_id = int(id)
    hint = hints.get_hint(hint_id)
    wed_places = hints.get_hint_places(hint_id, 1)
    wed_styles = hints.get_hint_styles(hint_id, 1)
    fun_places = hints.get_hint_places(hint_id, 2)
    fun_styles = hints.get_hint_styles(hint_id, 2)
    return render_template("hint.html", hint_id=hint_id, name=hint.name,
                           composer=hint.composer, alternatives=hint.alternatives,
                           link1=hint.link1, link2=hint.link2, link3=hint.link3,
                           sent_at=hint.sent_at.strftime("%d.%m.%Y %H:%M"),
                           wed_places=wed_places, wed_styles=wed_styles,
                           fun_places=fun_places, fun_styles=fun_styles)

@app.route("/profile")
def profile():
    admin = users.admin()
    number = hints.get_number_of_suggestions()
    return render_template("profile.html", admin=admin, number=number)

@app.route("/change_password")
def change_password():
    admin = users.admin()
    number = hints.get_number_of_suggestions()
    return render_template("change_password.html", admin=admin, number=number)

@app.route("/save_password", methods=["POST"])
def save_password():
    users.check_csrf()
    password = request.form["password"]
    password1 = request.form["password1"]
    password2 = request.form["password2"]
    error = ""
    if not password:
        error = "Kirjoita nykyinen salasana."
    elif password1 != password2:
        error = "Salasanat eroavat."
    elif not password1:
        error = "Lisää uusi salasana."
    elif len(password1) > 100:
        error = "Uusi salasana on liian pitkä."
    elif not accept_password(password1):
        error = "Uusi salasana ei täytä kriteerejä."
    if error:
        return render_template("error.html", error=error)
    if users.change_password(password, password1):
        return redirect("/")
    return render_template("error.html", error="Nykyinen salasana on väärä.")

@app.route("/propositions")
def propositions():
    admin = users.admin()
    number = hints.get_number_of_suggestions()
    elements = hints.get_new_suggestions()
    new_hints = []
    for hint_id, name, composer in elements:
        new_hints.append((name, composer, f"/page/new/{hint_id}"))
    number_new = hints.get_number_of_new()
    elements = hints.get_change_suggestions()
    change_hints = []
    for hint_id, name, composer in elements:
        change_hints.append((name, composer, f"/page/change/{hint_id}"))
    number_change = hints.get_number_of_changed()
    elements = hints.get_remove_suggestions()
    remove_hints = []
    for hint_id, name, composer in elements:
        remove_hints.append((name, composer, f"/page/remove/{hint_id}"))
    number_remove = hints.get_number_of_removed()
    return render_template("propositions.html", admin=admin,
                           number=number, number_new=number_new,
                           number_change=number_change, number_remove=number_remove,
                           new_hints=new_hints, change_hints=change_hints, remove_hints=remove_hints)

@app.route("/page/new/<int:id>")
def page_new(id):
    admin = users.admin()
    hint_id = int(id)
    hint = hints.get_hint(hint_id)
    wed_places = hints.get_new_places(hint_id, 1)
    wed_styles = hints.get_new_styles(hint_id, 1)
    fun_places = hints.get_new_places(hint_id, 2)
    fun_styles = hints.get_new_styles(hint_id, 2)
    return render_template("hint_new.html", hint_id=hint_id, admin=admin,
                           name=hint.name, composer=hint.composer, alternatives=hint.alternatives,
                           link1=hint.link1, link2=hint.link2, link3=hint.link3,
                           sent_at=hint.sent_at.strftime("%d.%m.%Y %H:%M"),
                           wed_places=wed_places, wed_styles=wed_styles,
                           fun_places=fun_places, fun_styles=fun_styles)

@app.route("/page/change/<int:id>")
def page_change(id):
    admin = users.admin()
    hint_id = int(id)
    hint = hints.get_hint(hint_id)
    old_id = hints.get_previous_id(hint_id)
    current_hint = f"/page/{old_id}"
    wed_places = hints.get_changed_places(hint_id, 1)
    wed_styles = hints.get_changed_styles(hint_id, 1)
    fun_places = hints.get_changed_places(hint_id, 2)
    fun_styles = hints.get_changed_styles(hint_id, 2)
    return render_template("hint_change.html", hint_id=hint_id, admin=admin,
                           name=hint.name, composer=hint.composer, alternatives=hint.alternatives,
                           link1=hint.link1, link2=hint.link2, link3=hint.link3,
                           sent_at=hint.sent_at.strftime("%d.%m.%Y %H:%M"),
                           wed_places=wed_places, wed_styles=wed_styles,
                           fun_places=fun_places, fun_styles=fun_styles, current_hint=current_hint)

@app.route("/page/remove/<int:id>")
def page_remove(id):
    admin = users.admin()
    remove_id = int(id)
    hint_id, reason = hints.get_removed_hint(remove_id)
    hint = hints.get_hint(hint_id)
    wed_places = hints.get_place_names(hint_id, 1)
    wed_styles = hints.get_style_names(hint_id, 1)
    fun_places = hints.get_place_names(hint_id, 2)
    fun_styles = hints.get_style_names(hint_id, 2)
    return render_template("hint_remove.html", hint_id=hint_id, admin=admin,
                           name=hint.name, composer=hint.composer, alternatives=hint.alternatives,
                           link1=hint.link1, link2=hint.link2, link3=hint.link3,
                           sent_at=hint.sent_at.strftime("%d.%m.%Y %H:%M"),
                           wed_places=wed_places, wed_styles=wed_styles,
                           fun_places=fun_places, fun_styles=fun_styles, reason=reason)

@app.route("/new")
def new():
    return render_template("new.html")

@app.route("/confirm_new", methods=["POST"])
def confirm_new():
    users.check_csrf()
    composer = request.form["composer"]
    name = request.form["name"]
    alternatives = request.form["alternatives"]
    link1 = request.form["link1"]
    link2 = request.form["link2"]
    link3 = request.form["link3"]
    places1 = request.form.getlist("place1")
    styles1 = request.form.getlist("style1")
    places2 = request.form.getlist("place2")
    styles2 = request.form.getlist("style2")
    wed_places = []
    for place in places1:
        wed_places.append(hints.get_name_place(int(place)))
    wed_styles = []
    for style in styles1:
        wed_styles.append(hints.get_name_style(int(style)))
    fun_places = []
    for place in places2:
        fun_places.append(hints.get_name_place(int(place)))
    fun_styles = []
    for style in styles2:
        fun_styles.append(hints.get_name_style(int(style)))
    error = check_input(composer, name, alternatives, link1, link2, link3, places1, styles1, places2, styles2)
    if error:
        return render_template("error.html", error=error)
    return render_template("confirm_new.html",
                           composer=composer, name=name, alternatives=alternatives,
                           link1=link1, link2=link2, link3=link3,
                           wed_places=wed_places, wed_styles=wed_styles,
                           fun_places=fun_places, fun_styles=fun_styles,
                           places1=places1, styles1=styles1, places2=places2, styles2=styles2)

@app.route("/save_hint_suggestion", methods=["POST"])
def save_hint_suggestion():
    users.check_csrf()
    composer = request.form["composer"]
    name = request.form["name"]
    alternatives = request.form["alternatives"]
    link1 = request.form["link1"]
    link2 = request.form["link2"]
    link3 = request.form["link3"]
    places1 = str(request.form.getlist("places1")[0])
    styles1 = str(request.form.getlist("styles1")[0])
    places2 = str(request.form.getlist("places2")[0])
    styles2 = str(request.form.getlist("styles2")[0])
    places1 = [int(item) for item in places1 if item in ["1", "2", "3"]]
    styles1 = [int(item) for item in styles1 if item in ["1", "2", "3", "4"]]
    places2 = [int(item) for item in places2 if item in ["1", "2", "3"]]
    styles2 = [int(item) for item in styles2 if item in ["1", "2", "3", "4"]]
    hint_id = hints.create_hint(composer, name, alternatives, link1, link2, link3)
    if places1:
        for place_id in places1:
            for style_id in styles1:
                hints.create_new_suggestion(hint_id, 1, place_id, style_id)
    if places2:
        for place_id in places2:
            for style_id in styles2:
                hints.create_new_suggestion(hint_id, 2, place_id, style_id)
    return render_template("saved.html", message="Vinkkiehdotus")

@app.route("/accept_new", methods=["POST"])
def accept_new():
    users.check_csrf()
    hint_id = request.form["hint_id"]
    hints.set_categories_new(hint_id)
    hints.delete_new_suggestion(hint_id)
    return redirect("/propositions")

@app.route("/reject_new", methods=["POST"])
def reject_new():
    users.check_csrf()
    hint_id = request.form["hint_id"]
    hints.delete_new_suggestion(hint_id)
    hints.delete_hint(hint_id)
    return redirect("/propositions")

@app.route("/change", methods=["POST"])
def change():
    hint_id = request.form["hint_id"]
    hint = hints.get_hint(hint_id)
    selected = hints.get_places(hint_id, 1)
    wed_places = ["" for i in range(3)]
    for selection in selected:
        wed_places[selection[0]-1] = "checked"
    selected = hints.get_styles(hint_id, 1)
    wed_styles = ["" for i in range(4)]
    for selection in selected:
        wed_styles[selection[0]-1] = "checked"
    selected = hints.get_places(hint_id, 2)
    fun_places = ["" for i in range(3)]
    for selection in selected:
        fun_places[selection[0]-1] = "checked"
    selected = hints.get_styles(hint_id, 2)
    fun_styles = ["" for i in range(4)]
    for selection in selected:
        fun_styles[selection[0]-1] = "checked"
    return render_template("change.html", hint_id=hint_id,
                           composer=hint.composer, name=hint.name, alternatives=hint.alternatives,
                           link1=hint.link1, link2=hint.link2, link3=hint.link3,
                           wed_places=wed_places, wed_styles=wed_styles,
                           fun_places=fun_places, fun_styles=fun_styles)

@app.route("/confirm_change", methods=["POST"])
def confirm_change():
    users.check_csrf()
    hint_id = request.form["hint_id"]
    composer = request.form["new_composer"]
    name = request.form["new_name"]
    alternatives = request.form["new_alternatives"]
    link1 = request.form["new_link1"]
    link2 = request.form["new_link2"]
    link3 = request.form["new_link3"]
    places1 = request.form.getlist("place1")
    styles1 = request.form.getlist("style1")
    places2 = request.form.getlist("place2")
    styles2 = request.form.getlist("style2")
    wed_places = []
    for place in places1:
        wed_places.append(hints.get_name_place(place))
    wed_styles = []
    for style in styles1:
        wed_styles.append(hints.get_name_style(style))
    fun_places = []
    for place in places2:
        fun_places.append(hints.get_name_place(place))
    fun_styles = []
    for style in styles2:
        fun_styles.append(hints.get_name_style(style))
    error = check_input(composer, name, alternatives, link1, link2, link3, places1, styles1, places2, styles2)
    if error:
        return render_template("error.html", error=error)
    return render_template("confirm_change.html", hint_id=hint_id,
                           composer=composer, name=name, alternatives=alternatives,
                           link1=link1, link2=link2, link3=link3,
                           wed_places=wed_places, wed_styles=wed_styles,
                           fun_places=fun_places, fun_styles=fun_styles,
                           places1=places1, styles1=styles1, places2=places2, styles2=styles2)

@app.route("/save_change_suggestion", methods=["POST"])
def save_change_suggestion():
    users.check_csrf()
    old_id = request.form["hint_id"]
    composer = request.form["composer"]
    name = request.form["name"]
    alternatives = request.form["alternatives"]
    link1 = request.form["link1"]
    link2 = request.form["link2"]
    link3 = request.form["link3"]
    places1 = str(request.form.getlist("places1")[0])
    styles1 = str(request.form.getlist("styles1")[0])
    places2 = str(request.form.getlist("places2")[0])
    styles2 = str(request.form.getlist("styles2")[0])
    places1 = [int(item) for item in places1 if item in ["1", "2", "3"]]
    styles1 = [int(item) for item in styles1 if item in ["1", "2", "3", "4"]]
    places2 = [int(item) for item in places2 if item in ["1", "2", "3"]]
    styles2 = [int(item) for item in styles2 if item in ["1", "2", "3", "4"]]
    new_id = hints.create_hint(composer, name, alternatives, link1, link2, link3)
    if places1:
        for place_id in places1:
            for style_id in styles1:
                hints.create_change_suggestion(old_id, new_id, 1, place_id, style_id)
    if places2:
        for place_id in places2:
            for style_id in styles2:
                hints.create_change_suggestion(old_id, new_id, 2, place_id, style_id)
    return render_template("saved.html", message="Muutosehdotus")

@app.route("/accept_change", methods=["POST"])
def accept_change():
    users.check_csrf()
    hint_id = request.form["hint_id"]
    old_id = hints.get_old_id(hint_id)
    hints.set_categories_changed(hint_id)
    hints.delete_change_suggestion(hint_id)
    hints.update_change_suggestions(hint_id, old_id)
    hints.delete_categories(old_id)
    hints.update_remove_suggestions(hint_id, old_id)
    hints.delete_hint(old_id)
    return redirect("/propositions")

@app.route("/reject_change", methods=["POST"])
def reject_change():
    users.check_csrf()
    hint_id = request.form["hint_id"]
    hints.delete_change_suggestion(hint_id)
    hints.delete_hint(hint_id)
    return redirect("/propositions")

@app.route("/confirm_remove", methods=["POST"])
def confirm_remove():
    users.check_csrf()
    reason = request.form["reason"]
    if not reason:
        return render_template("error.html", error="Lisää perustelu vinkin poistamiselle.")
    elif len(reason) > 1000:
        return render_template("error.html", error="Poistamisen perustelu on liian pitkä.")
    hint_id = request.form["hint_id"]
    composer = request.form["composer"]
    name = request.form["name"]
    return render_template("confirm_remove.html", hint_id=hint_id, reason=reason, composer=composer, name=name)

@app.route("/save_remove_suggestion", methods=["POST"])
def save_remove_suggestion():
    users.check_csrf()
    hint_id = request.form["hint_id"]
    reason = request.form["reason"]
    hints.create_remove_suggestion(hint_id, reason)
    return render_template("saved.html", message="Poistoehdotus")

@app.route("/accept_remove", methods=["POST"])
def accept_remove():
    users.check_csrf()
    hint_id = request.form["hint_id"]
    change_suggestions = hints.get_change_suggestions_by_id(hint_id)
    for suggestion in change_suggestions:
        hints.delete_change_suggestion(suggestion[0])
        hints.delete_hint(suggestion[0])
    hints.delete_remove_suggestion(hint_id)
    hints.delete_categories(hint_id)
    hints.delete_hint(hint_id)
    return redirect("/propositions")

@app.route("/reject_remove", methods=["POST"])
def reject_remove():
    users.check_csrf()
    hint_id = request.form["hint_id"]
    hints.delete_remove_suggestion(hint_id)
    return redirect("/propositions")

@app.route("/result")
def result():
    query = request.args["query"]
    elements = hints.search(query)
    result = []
    for hint_id, name, composer in elements:
        result.append((name, composer, f"/page/{hint_id}"))
    return render_template("result.html", result=result, query=query)

@app.route("/customs")
def customs():
    return render_template("customs.html")

@app.route("/cancel", methods=["POST"])
def cancel():
    return redirect("/")
@app.route("/wedding")
def wedding():
    elements = hints.get_occasion_latest(1)
    weddings = []
    for hint_id, name, composer in elements:
        weddings.append((name, composer, f"/page/{hint_id}"))
    return render_template("wedding.html", weddings=weddings)

@app.route("/wedding_selected", methods=["POST"])
def wedding_selected():
    place_id = int(request.form["place"])
    places = []
    for i in range(4):
        if place_id == i:
            places.append("checked")
        else:
            places.append("")
    style_id = int(request.form["style"])
    styles = []
    for i in range(5):
        if style_id == i:
            styles.append("checked")
        else:
            styles.append("")
    order = request.form["order"]
    elements, number = get_selected_hints(order, place_id, style_id, 1)
    selected = []
    for i in range(6):
        if number == i:
            selected.append("selected")
        else:
            selected.append("")
    selected_hints = []
    for hint_id, name, composer in elements:
        selected_hints.append((name, composer, f"/page/{hint_id}"))
    return render_template("wedding_selected.html", places=places, styles=styles,
                           selected_hints=selected_hints, selected=selected)

@app.route("/funeral")
def funeral():
    elements = hints.get_occasion_latest(2)
    funerals = []
    for hint_id, name, composer in elements:
        funerals.append((name, composer, f"/page/{hint_id}"))
    return render_template("funeral.html", funerals=funerals)

@app.route("/funeral_selected", methods=["POST"])
def funeral_selected():
    place_id = int(request.form["place"])
    places = []
    for i in range(4):
        if place_id == i:
            places.append("checked")
        else:
            places.append("")
    style_id = int(request.form["style"])
    styles = []
    for i in range(5):
        if style_id == i:
            styles.append("checked")
        else:
            styles.append("")
    order = request.form["order"]
    elements, number = get_selected_hints(order, place_id, style_id, 2)
    selected = []
    for i in range(6):
        if number == i:
            selected.append("selected")
        else:
            selected.append("")
    funerals = []
    for hint_id, name, composer in elements:
        funerals.append((name, composer, f"/page/{hint_id}"))
    return render_template("funeral_selected.html",
                           places=places, styles=styles, funerals=funerals, selected=selected)

def accept_password(password):
    lowercase = string.ascii_lowercase + "åäö"
    uppercase = string.ascii_uppercase + "ÅÄÖ"
    lower, upper, punctuation, number = 0, 0, 0, 0
    if (len(password) >= 8):
        for char in password:
            if (char in lowercase):
                lower+=1           
            if (char in uppercase):
                upper+=1          
            if (char in string.digits):
                number+=1           
            if(char in string.punctuation):
                punctuation+=1
    if (lower>=1 and upper>=1 and number>=1 and punctuation>=1 and lower+upper+punctuation+number==len(password)):
        return True
    return False

def check_input(composer, name, alternatives, link1, link2, link3, places1, styles1, places2, styles2):
    message = ""
    if not composer:
        message = "Lisää kappaleen esittäjä/säveltäjä."
    elif not name:
        message = "Lisää kappaleen nimi."
    elif len(composer) > 100:
        message = "Säveltäjän/esittäjän nimi on liian pitkä."
    elif len(name) > 100:
        message = "Kappaleen nimi on liian pitkä."
    elif len(alternatives) > 500:
        message = "Vaihtoehtoisissa tiedoissa on liikaa merkkejä."
    elif len(link1) > 200 or len(link2) > 200 or len(link3) > 200:
        message = "Verkko-osoitteessa on liikaa merkkejä."
    elif not (places1 or styles1 or places2 or styles2):
        message = "Kappaleella ei ole kategorioita"
    elif (places1 and not styles1) or (styles1 and not places1):
        message = "Tarkista kappaleen kategoriat."
    elif (places2 and not styles2) or (styles2 and not places2):
        message = "Tarkista kappaleen kategoriat."
    return message

def get_selected_hints(order, place_id, style_id, occasion_id):
    if place_id == 0:
        if style_id == 0:
            if order == "latest":
                number = 0
                elements = hints.get_occasion_latest(occasion_id)
            elif order == "oldest":
                number = 1
                elements = hints.get_occasion_oldest(occasion_id)
            elif order == "composer":
                number = 2
                elements = hints.get_occasion_composer(occasion_id)
            elif order == "composer_rev":
                number = 3
                elements = hints.get_occasion_composer_reversed(occasion_id)
            elif order == "name":
                number = 4
                elements = hints.get_occasion_name(occasion_id)
            elif order == "name_rev":
                number = 5
                elements = hints.get_occasion_name_reversed(occasion_id)
        else:
            if order == "latest":
                number = 0
                elements = hints.get_style_latest(occasion_id, style_id)
            elif order == "oldest":
                number = 1
                elements = hints.get_style_oldest(occasion_id, style_id)
            elif order == "composer":
                number = 2
                elements = hints.get_style_composer(occasion_id, style_id)
            elif order == "composer_rev":
                number = 3
                elements = hints.get_style_composer_reversed(occasion_id, style_id)
            elif order == "name":
                number = 4
                elements = hints.get_style_name(occasion_id, style_id)
            elif order == "name_rev":
                number = 5
                elements = hints.get_style_name_reversed(occasion_id, style_id)
    else:
        if style_id == 0:
            if order == "latest":
                number = 0
                elements = hints.get_place_latest(occasion_id, place_id)
            elif order == "oldest":
                number = 1
                elements = hints.get_place_oldest(occasion_id, place_id)
            elif order == "composer":
                number = 2
                elements = hints.get_place_composer(occasion_id, place_id)
            elif order == "composer_rev":
                number = 3
                elements = hints.get_place_composer_reversed(occasion_id, place_id)
            elif order == "name":
                number = 4
                elements = hints.get_place_name(occasion_id, place_id)
            elif order == "name_rev":
                number = 5
                elements = hints.get_place_name_reversed(occasion_id, place_id)
        else:
            if order == "latest":
                number = 0
                elements = hints.get_place_style_latest(occasion_id, place_id, style_id)
            elif order == "oldest":
                number = 1
                elements = hints.get_place_style_oldest(occasion_id, place_id, style_id)
            elif order == "composer":
                number = 2
                elements = hints.get_place_style_composer(occasion_id, place_id, style_id)
            elif order == "composer_rev":
                number = 3
                elements = hints.get_place_style_composer_reversed(occasion_id, place_id, style_id)
            elif order == "name":
                number = 4
                elements = hints.get_place_style_name(occasion_id, place_id, style_id)
            elif order == "name_rev":
                number = 5
                elements = hints.get_place_style_name_reversed(occasion_id, place_id, style_id)
    return elements, number
