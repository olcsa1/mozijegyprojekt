-- phpMyAdmin SQL Dump
-- version 5.2.1
-- https://www.phpmyadmin.net/
--
-- Gép: 127.0.0.1
-- Létrehozás ideje: 2025. Feb 14. 09:22
-- Kiszolgáló verziója: 10.4.32-MariaDB
-- PHP verzió: 8.2.12

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
START TRANSACTION;
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;

--
-- Adatbázis: `mozijegy`
--

-- --------------------------------------------------------

--
-- Tábla szerkezet ehhez a táblához `foglalások`
--

CREATE TABLE `foglalások` (
  `Sorszam` varchar(4) NOT NULL,
  `Keresztnev` varchar(35) NOT NULL,
  `Vezeteknev` varchar(35) NOT NULL,
  `Terem_szam` tinyint(4) NOT NULL,
  `Szekszam` tinyint(4) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_unicode_ci;

-- --------------------------------------------------------

--
-- Tábla szerkezet ehhez a táblához `termek`
--

CREATE TABLE `termek` (
  `Terem_szam` tinyint(4) NOT NULL,
  `Film_cime` varchar(50) NOT NULL,
  `Egyeb_adat` int(100) NOT NULL COMMENT 'pl. évszám, játékidő, műfaj, stb..',
  `Terem_kapacitas` tinyint(4) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_unicode_ci;

--
-- Indexek a kiírt táblákhoz
--

--
-- A tábla indexei `foglalások`
--
ALTER TABLE `foglalások`
  ADD PRIMARY KEY (`Sorszam`),
  ADD UNIQUE KEY `teremszam` (`Terem_szam`);

--
-- A tábla indexei `termek`
--
ALTER TABLE `termek`
  ADD PRIMARY KEY (`Terem_szam`);

--
-- Megkötések a kiírt táblákhoz
--

--
-- Megkötések a táblához `foglalások`
--
ALTER TABLE `foglalások`
  ADD CONSTRAINT `foglalások_ibfk_1` FOREIGN KEY (`Terem_szam`) REFERENCES `termek` (`Terem_szam`) ON DELETE CASCADE ON UPDATE CASCADE;
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
