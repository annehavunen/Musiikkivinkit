# Musiikkivinkit
Sovellus tarjoaa musiikki-ideoita kirkollisiin häihin ja hautajaisiin.
Kirjautuneet käyttäjät voivat ehdottaa uusia musiikkivinkkejä, vinkkien muuttamista tai niiden poistamista. Ylläpitäjät hyväksyvät tai hylkäävät ehdotukset.
Musiikkivinkkejä voi selata ilman kirjautumista.

## Sovelluksen tämänhetkisiä ominaisuuksia
**Kirjautumaton käyttäjä voi**

- selata musiikkivinkkejä
- tarkentaa selatessa, mikä on musiikin paikka tilaisuudessa ja musiikkityyli
- järjestää musiikkivinkit päiväyksen, säveltäjän nimen tai kappaleen nimen mukaan
- hakea musiikkivinkkejä sanahaulla

**Kirjautunut käyttäjä voi**

- tehdä edellä mainitut
- ehdottaa uutta musiikkivinkkiä
- ehdottaa musiikkivinkin muuttamista
- ehdottaa musiikkivinkin poistamista
- vaihtaa salasanan
- katsoa profiilia

**Ylläpitäjä voi**

- tehdä edellä mainitut
- hyväksyä tai hylätä ehdotetut vinkit, muutokset tai poistot

## Sovelluksen suunnitteilla olevia ominaisuuksia

- salasanalle on tarkemmat kriteerit
- ulkoasun parantamista
  - erityisesti yksittäisten musiikkivinkkien ulkoasun selkeyttämistä

## Sovelluksen testaaminen Herokussa

- sovellusta voi testata [Herokussa](https://musiikkivinkit.herokuapp.com)
- vinkkiehdotusten hyväksyminen tai hylkääminen vaatii ylläpitäjän oikeudet. Testataksesi ominaisuuksia syötä kirjautuessa (ei-niin-salaisesti):
  - Tunnus: ylläpitäjä
  - Salasana: ylläpito
