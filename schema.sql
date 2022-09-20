CREATE TABLE Hint (
    id SERIAL PRIMARY KEY,
    composer TEXT,
    name TEXT,
    alternatives TEXT,
    link1 TEXT,
    link2 TEXT,
    link3 TEXT,
    sent_at TIMESTAMP
);

CREATE TABLE Occasion (
    id SERIAL PRIMARY KEY,
    name TEXT
);

CREATE TABLE Place (
    id SERIAL PRIMARY KEY,
    name TEXT
);

CREATE TABLE Style (
    id SERIAL PRIMARY KEY,
    name TEXT
);

CREATE TABLE Categories (
    hint_id INTEGER REFERENCES Hint,
    occasion_id INTEGER REFERENCES Occasion,
    place_id INTEGER REFERENCES Place,
    style_id INTEGER REFERENCES Style
);

CREATE TABLE New_hint (
    hint_id INTEGER REFERENCES Hint,
    occasion_id INTEGER REFERENCES Occasion,
    place_id INTEGER REFERENCES Place,
    style_id INTEGER REFERENCES Style
);

CREATE TABLE Users (
    id SERIAL PRIMARY KEY, 
    username TEXT UNIQUE, 
    password TEXT,
    admin BOOLEAN
);

