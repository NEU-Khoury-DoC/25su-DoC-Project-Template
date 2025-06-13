DROP DATABASE IF EXISTS loyalty_lines;
CREATE DATABASE IF NOT EXISTS loyalty_lines;

USE loyalty_lines;


CREATE TABLE IF NOT EXISTS political_party (
    partyID INT AUTO_INCREMENT PRIMARY KEY,
    partyCohesionScore INT,
    partyName VARCHAR(255)
);

CREATE TABLE IF NOT EXISTS mep (
    mepID INT PRIMARY KEY,
    name VARCHAR(255),
    contactInformation VARCHAR(255),
    countryOfOrigin VARCHAR(255),
    loyaltyScore DECIMAL(3, 1),
    percentDisagree VARCHAR(100),
    percentTurnout VARCHAR(100),
    partyID INT,
    recommendedPartyID INT,
    voteForPct DECIMAL(5, 2),
    voteAgainstPct DECIMAL(5, 2),
    voteAbstainPct DECIMAL(5, 2),
    didNotVotePct DECIMAL(5, 2),
    photoURL VARCHAR(255),
    FOREIGN KEY (partyID) REFERENCES political_party(partyID),
    FOREIGN KEY (recommendedPartyID) REFERENCES political_party(partyID)
);

CREATE TABLE IF NOT EXISTS userRole (
    userRoleID INT PRIMARY KEY,
    userRoleName VARCHAR(255)
);

CREATE TABLE IF NOT EXISTS user (
    userID INT AUTO_INCREMENT PRIMARY KEY,
    age INT,
    countryOfOrigin VARCHAR(255),
    firstName VARCHAR(255),
    lastName VARCHAR(255),
    partyID INT,
    watchListID INT,
    userRoleID INT,
    FOREIGN KEY (partyID) REFERENCES political_party(partyID),
    FOREIGN KEY (userRoleID) REFERENCES userRole(userRoleID)
);

CREATE TABLE IF NOT EXISTS watchList (
    mepID INT,
    userID INT,
    PRIMARY KEY (userID, mepID),
    FOREIGN KEY (userID) REFERENCES user(userID),
    FOREIGN KEY (mepID) REFERENCES mep(mepID)
);

CREATE TABLE IF NOT EXISTS legislation (
    legislationID INT PRIMARY KEY,
    title VARCHAR(255),
    dateOfVote DATE
);

CREATE TABLE IF NOT EXISTS referenceDocument (
    legislationID INT,
    referenceID INT,
    PRIMARY KEY (legislationID, referenceID),
    FOREIGN KEY (legislationID) REFERENCES legislation(legislationID)
);
