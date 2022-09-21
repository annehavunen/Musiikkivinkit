from flask import render_template, redirect, request
from app import app
import hints, users


@app.route("/")
def index():
    tuple = hints.get_latest()
    latest = []
    for id, name, composer in tuple:
        latest.append((name, composer, f"/page/{id}"))
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
    else:
        return render_template("error.html", error="Väärä tunnus tai salasana")

@app.route("/logout")
def logout():
    users.logout()
    return redirect("/")

@app.route("/registerpage")
def registerpage():
    return render_template("registerpage.html")

@app.route("/register", methods=["POST"])
def register():
    username = request.form["username"]
    password1 = request.form["password1"]
    password2 = request.form["password2"]
    if not username:
        return render_template("error.html", error="Lisää käyttäjätunnus.")
    elif len(username) > 50:
        return render_template("error.html", error="Käyttäjätunnus on liian pitkä.")
    elif password1 != password2:
        return render_template("error.html", error="Salasanat eroavat.")
    elif not password1:
        return render_template("error.html", error="Lisää salasana.")
    elif len(password1) > 100:
        return render_template("error.html", error="Salasana on liian pitkä.")
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
    return render_template("hint.html", hint_id=hint_id, name=hint.name, composer=hint.composer, alternatives=hint.alternatives,
            link1=hint.link1, link2=hint.link2, link3=hint.link3, sent_at=hint.sent_at.strftime("%d.%m.%Y %H:%M"),
            wed_places=wed_places, wed_styles=wed_styles, fun_places=fun_places, fun_styles=fun_styles)

@app.route("/profile")
def profile():
    admin = users.admin()
    number = hints.get_number_of_new()
    return render_template("profile.html", admin=admin, number=number)

@app.route("/change_password")
def change_password():
    admin = users.admin()
    number = hints.get_number_of_new()
    return render_template("change_password.html", admin=admin, number=number)

@app.route("/propositions")
def propositions():
    admin = users.admin()
    tuple = hints.get_new()
    new_hints = []
    for id, name, composer in tuple:
        new_hints.append((name, composer, f"/page/new/{id}"))
    number = hints.get_number_of_new()
    return render_template("propositions.html", admin=admin, number=number, new_hints=new_hints)

@app.route("/page/new/<int:id>")
def page_new(id):
    admin = users.admin()
    hint_id = int(id)
    hint = hints.get_hint(hint_id)
    wed_places = hints.get_new_places(hint_id, 1)
    wed_styles = hints.get_new_styles(hint_id, 1)
    fun_places = hints.get_new_places(hint_id, 2)
    fun_styles = hints.get_new_styles(hint_id, 2)
    return render_template("hint_new.html", 
            admin=admin, hint_id=hint_id, name=hint.name, composer=hint.composer, alternatives=hint.alternatives,
            link1=hint.link1, link2=hint.link2, link3=hint.link3,
            sent_at=hint.sent_at.strftime("%d.%m.%Y %H:%M"),
            wed_places=wed_places, wed_styles=wed_styles, fun_places=fun_places, fun_styles=fun_styles)

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
    if not composer:
        return render_template("error.html", error="Lisää kappaleen esittäjä/säveltäjä.")
    elif not name:
        return render_template("error.html", error="Lisää kappaleen nimi.")
    elif len(composer) > 100:
        return render_template("error.html", error="Säveltäjän/esittäjän nimi on liian pitkä")
    elif len(name) > 150:
        return render_template("error.html", error="Kappaleen nimi on liian pitkä.")
    elif len(alternatives) > 1000:
        return render_template("error.html", error="Vaihtoehtoisissa tiedoissa on liikaa merkkejä.")
    elif len(link1) > 300 or len(link2) > 300 or len(link3) > 300:
        return render_template("error.html", error="Verkko-osoitteessa on liikaa merkkejä.")
    elif not (places1 or styles1 or places2 or styles2):
        return render_template("error.html", error="Kappaleella ei ole kategorioita")
    elif (places1 and not styles1) or (styles1 and not places1):
        return render_template("error.html", error="Tarkista kappaleen kategoriat")
    elif (places2 and not styles2) or (styles2 and not places2):
        return render_template("error.html", error="Tarkista kappaleen kategoriat")
    return render_template("confirm_new.html",
            composer=composer, name=name, alternatives=alternatives,
            link1=link1, link2=link2, link3=link3,
            wed_places=wed_places, wed_styles=wed_styles, fun_places=fun_places, fun_styles=fun_styles,
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
                hints.new_hint_categories(hint_id, 1, place_id, style_id)
    if places2:
        for place_id in places2:
            for style_id in styles2:
                hints.new_hint_categories(hint_id, 2, place_id, style_id)
    return render_template("saved.html", message="Vinkkiehdotus")

@app.route("/save_new", methods=["POST"])
def save_new():
    users.check_csrf()
    hint_id = request.form["hint_id"]
    hints.set_categories_new(hint_id)
    hints.delete_new_hint(hint_id)
    return redirect("/propositions")

@app.route("/reject_new", methods=["POST"])
def reject_new():
    users.check_csrf()
    hint_id = request.form["hint_id"]
    hints.delete_new_hint(hint_id)
    hints.delete_hint(hint_id)
    return redirect("/propositions")

@app.route("/wedding")
def wedding():
    tuple = hints.get_occasion_latest(1)
    weddings = []
    for id, name, composer in tuple:
        weddings.append((name, composer, f"/page/{id}"))
    return render_template("wedding.html", weddings=weddings)

@app.route("/funeral")
def funeral():
    tuple = hints.get_occasion_latest(2)
    funerals = []
    for id, name, composer in tuple:
        funerals.append((name, composer, f"/page/{id}"))
    return render_template("funeral.html", funerals=funerals)

@app.route("/result")
def result():
    return render_template("result.html")

@app.route("/customs")
def customs():
    return render_template("customs.html")

@app.route("/cancel", methods=["POST"])
def cancel():
    return redirect("/")
