USE loyalty_lines;

-- PREPARE POLIICAL PARTIES
INSERT INTO political_party (partyName)
VALUES ("European People's Party");

INSERT INTO political_party (partyName)
VALUES ("Progressive Alliance of Socialists and Democrats");

INSERT INTO political_party (partyName)
VALUES ("Patriots for Europe");

INSERT INTO political_party (partyName)
VALUES ("European Conservatives and Reformists");

INSERT INTO political_party (partyName)
VALUES ("Renew Europe");

INSERT INTO political_party (partyName)
VALUES ("Greens/European Free Alliance");

INSERT INTO political_party (partyName)
VALUES ("The Left in the European Parliament - GUE/NGL");

INSERT INTO political_party (partyName)
VALUES ("Europe of Sovereign Nations");

INSERT INTO political_party (partyName)
VALUES ("Non-attached Members");

INSERT INTO political_party(partyName)
VALUES ("Identity and Democracy");

-- PREPARE USER ROLES
INSERT INTO userRole(userRoleID, userRoleName)
VALUES (1, "PartyLeader");

INSERT INTO userRole(userRoleID, userRoleName)
VALUES (2, "PoliticalJournalist");

INSERT INTO userRole(userRoleID, userRoleName)
VALUES (3, "Citizen");

-- PREARE USER PERSONAS
INSERT INTO user (age, countryOfOrigin, firstName, lastName, partyID, userRoleID)
VALUES ("59", "Greece", "Yanni", "Polous", 1, 1),
("45", "Germany", "Anna", "Schmidt", 2, 1),
("38", "France", "Jean", "Dubois", 3, 1),
("50", "Poland", "Marek", "Nowak", 4, 1),
("34", "Italy", "Luca", "Bianchi", 5, 1),
("29", "Ireland", "Siobhan", "Murphy", 6, 1);


INSERT INTO user (age, countryOfOrigin, firstName, lastName, userRoleID)
VALUES ("30", "Spain", "Camila", "Romero", 2),
("27", "Netherlands", "Eva", "Jansen", 2),
("41", "Austria", "Karl", "Müller", 2),
("36", "Portugal", "Ines", "Fernandes", 2),
("33", "Belgium", "Tom", "Lemoine", 2),
("22", "Czech Republic", "Petr", "Novák", 2);

INSERT INTO user (age, countryOfOrigin, firstName, lastName, partyID, userRoleID)
VALUES ("23", "Switzerland", "Greg", "Gerborg", 3, 3),
("60", "Hungary", "Ilona", "Toth", 2, 3),
("52", "Denmark", "Niels", "Christensen", 3, 3),
("47", "Slovakia", "Jana", "Kováčová", 1, 3),
("44", "Sweden", "Erik", "Svensson", 2, 3),
("39", "Romania", "Andrei", "Popescu", 3, 3);


