PRAGMA foreign_keys = ON;

-- Tábla: termek
CREATE TABLE termek (
  Terem_szam INTEGER PRIMARY KEY,
  Film_cime TEXT NOT NULL,
  Egyeb_adat INTEGER NOT NULL, -- pl. évszám, játékidő, műfaj, stb.
  Terem_kapacitas INTEGER NOT NULL
);

-- Tábla: foglalások
CREATE TABLE foglalások (
  Sorszam TEXT PRIMARY KEY,
  Keresztnev TEXT NOT NULL,
  Vezeteknev TEXT NOT NULL,
  Terem_szam INTEGER NOT NULL,
  Szekszam INTEGER NOT NULL,
  UNIQUE (Terem_szam),
  FOREIGN KEY (Terem_szam) REFERENCES termek (Terem_szam) ON DELETE CASCADE ON UPDATE CASCADE
);
