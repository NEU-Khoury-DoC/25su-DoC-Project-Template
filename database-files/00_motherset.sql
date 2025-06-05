DROP DATABASE IF EXISTS Consensus_DB;

CREATE DATABASE Consensus_DB;

USE Consensus_DB;

CREATE TABLE Users (
    UserID INT UNSIGNED AUTO_INCREMENT PRIMARY KEY,
    Name VARCHAR(255) NOT NULL,
    PoliticalParty VARCHAR(100),
    Bio TEXT,
    NumFollowers INT DEFAULT 0,
    NumFollowing INT DEFAULT 0
);

CREATE TABLE Roles (
    RoleID INT UNSIGNED AUTO_INCREMENT PRIMARY KEY,
    RoleType VARCHAR(50) NOT NULL
);

CREATE TABLE Graphs (
    GraphID INT UNSIGNED AUTO_INCREMENT PRIMARY KEY,
    XAxis VARCHAR(100) NOT NULL,
    XMin FLOAT NOT NULL,
    XMax FLOAT NOT NULL,
    XStep FLOAT NOT NULL,
    Population INT NOT NULL,
    GDP_per_capita FLOAT NOT NULL,
    Trade_union_density FLOAT NOT NULL,
    Unemployment_rate FLOAT NOT NULL,
    Health FLOAT NOT NULL,
    Education FLOAT NOT NULL,
    Housing FLOAT NOT NULL,
    Community_development FLOAT NOT NULL,
    Real_interest_rates FLOAT NOT NULL,
    Productivity FLOAT NOT NULL,
    Corporate_tax_rate FLOAT NOT NULL,
    Inflation FLOAT NOT NULL,
    Personal_property_tax FLOAT NOT NULL,
    IRLT FLOAT NOT NULL,
    Region_East_Asia_and_Pacific FLOAT NOT NULL,
    Region_Europe_and_Central_Asia FLOAT NOT NULL,
    Region_Latin_America_and_Caribbean FLOAT NOT NULL,
    Region_Middle_East_and_North_Africa FLOAT NOT NULL
);


CREATE TABLE ModelWeights (
    ModelID INT UNSIGNED AUTO_INCREMENT PRIMARY KEY,
<<<<<<< HEAD
    ModelName VARCHAR(25) NOT NULL,
=======
    ModelName STRING NOT NULL,
>>>>>>> 7c0b63c (drafted prediction route)
    Population FLOAT NOT NULL,
    GDP_per_capita FLOAT NOT NULL,
    Trade_union_density FLOAT NOT NULL,
    Unemployment_rate FLOAT NOT NULL,
    Health FLOAT NOT NULL,
    Education FLOAT NOT NULL,
    Housing FLOAT NOT NULL,
    Community_development FLOAT NOT NULL,
    Real_interest_rates FLOAT NOT NULL,
    Productivity FLOAT NOT NULL,
    Corporate_tax_rate FLOAT NOT NULL,
    Inflation FLOAT NOT NULL,
    Personal_property_tax FLOAT NOT NULL,
    IRLT FLOAT NOT NULL,
    Region_East_Asia_and_Pacific FLOAT NOT NULL,
    Region_Europe_and_Central_Asia FLOAT NOT NULL,
    Region_Latin_America_and_Caribbean FLOAT NOT NULL,
    Region_Middle_East_and_North_Africa FLOAT NOT NULL,
    DateAdded DATETIME DEFAULT NOW()
);

CREATE TABLE PredictMetrics (
    MetricID INT UNSIGNED AUTO_INCREMENT PRIMARY KEY,
    Metric VARCHAR(10) NOT NULL,
    Population FLOAT NOT NULL,
    GDP_per_capita FLOAT NOT NULL,
    Trade_union_density FLOAT NOT NULL,
    Unemployment_rate FLOAT NOT NULL,
    Health FLOAT NOT NULL,
    Education FLOAT NOT NULL,
    Housing FLOAT NOT NULL,
    Community_development FLOAT NOT NULL,
    Real_interest_rates FLOAT NOT NULL,
    Productivity FLOAT NOT NULL,
    Corporate_tax_rate FLOAT NOT NULL,
    Inflation FLOAT NOT NULL,
    Personal_property_tax FLOAT NOT NULL,
    IRLT FLOAT NOT NULL,
    Region_East_Asia_and_Pacific FLOAT NOT NULL,
    Region_Europe_and_Central_Asia FLOAT NOT NULL,
    Region_Latin_America_and_Caribbean FLOAT NOT NULL,
    Region_Middle_East_and_North_Africa FLOAT NOT NULL,
    DateAdded DATETIME DEFAULT NOW()
);

CREATE TABLE Posts (
    PostID INT UNSIGNED AUTO_INCREMENT PRIMARY KEY,
    Title VARCHAR(255) NOT NULL,
    Description TEXT NOT NULL,
    NumUpvotes INT DEFAULT 0,
    NumDownvotes INT DEFAULT 0,
    NumEndorsements INT DEFAULT 0,
    IsHidden BOOLEAN DEFAULT false,
    CreatedAt DATETIME NOT NULL DEFAULT NOW(),
    UserID INT UNSIGNED NOT NULL,
    GraphID INT UNSIGNED NOT NULL,
    FOREIGN KEY (UserID) REFERENCES Users (UserID),
    FOREIGN KEY (GraphID) REFERENCES Graphs (GraphID)
);

CREATE TABLE RolesUsers (
    RoleID INT UNSIGNED,
    UserID INT UNSIGNED,
    PRIMARY KEY (RoleID, UserID),
    FOREIGN KEY (RoleID) REFERENCES Roles (RoleID),
    FOREIGN KEY (UserID) REFERENCES Users (UserID)
);

CREATE TABLE Questions (
    QuestionID INT UNSIGNED AUTO_INCREMENT PRIMARY KEY,
    IsHidden BOOLEAN DEFAULT false,
    CreatedAt DATETIME DEFAULT NOW(),
    QuestionText TEXT NOT NULL,
    PostID INT UNSIGNED NOT NULL,
    FOREIGN KEY (PostID) REFERENCES Posts (PostID)
);

CREATE TABLE UserQuestions (
    UserID INT UNSIGNED NOT NULL,
    QuestionID INT UNSIGNED NOT NULL,
    PRIMARY KEY (UserID, QuestionID),
    FOREIGN KEY (UserID) REFERENCES Users (UserID),
    FOREIGN KEY (QuestionID) REFERENCES Questions (QuestionID)
);

CREATE TABLE Answers (
    AnswerID INT UNSIGNED AUTO_INCREMENT PRIMARY KEY,
    AnswerText TEXT NOT NULL,
    CreatedAt DATETIME NOT NULL DEFAULT NOW(),
    QuestionID INT UNSIGNED NOT NULL,
    UserID INT UNSIGNED NOT NULL,
    FOREIGN KEY (QuestionID) REFERENCES Questions (QuestionID),
    FOREIGN KEY (UserID) REFERENCES Users (UserID)
);

CREATE TABLE FollowingFollowees (
    FollowerID INT UNSIGNED NOT NULL,
    FolloweeID INT UNSIGNED NOT NULL,
    PRIMARY KEY (FollowerID, FolloweeID),
    FOREIGN KEY (FollowerID) REFERENCES Users (UserID),
    FOREIGN KEY (FolloweeID) REFERENCES Users (UserID)
);

CREATE TABLE SavedGraphs (
    UserID INT UNSIGNED NOT NULL,
    GraphID INT UNSIGNED NOT NULL,
    Name VARCHAR(255) NOT NULL,
    DateTimeSaved DATETIME NOT NULL DEFAULT NOW(),
    PRIMARY KEY (UserID, GraphID),
    UNIQUE (UserID, Name),
    FOREIGN KEY (UserID) REFERENCES Users (UserID),
    FOREIGN KEY (GraphID) REFERENCES Graphs (GraphID)
);

CREATE TABLE BookmarkedUsers (
    UserID INT UNSIGNED NOT NULL,
    PostID INT UNSIGNED NOT NULL,
    CreatedAt DATETIME DEFAULT NOW(),
    PRIMARY KEY (UserID, PostID),
    FOREIGN KEY (UserID) REFERENCES Users (UserID),
    FOREIGN KEY (PostID) REFERENCES Posts (PostID)
);

CREATE TABLE UpvotesUsers (
    UserID INT UNSIGNED NOT NULL,
    PostID INT UNSIGNED NOT NULL,
    CreatedAt DATETIME DEFAULT NOW(),
    PRIMARY KEY (UserID, PostID),
    FOREIGN KEY (UserID) REFERENCES Users (UserID),
    FOREIGN KEY (PostID) REFERENCES Posts (PostID)
);

CREATE TABLE DownvotesUsers (
    UserID INT UNSIGNED NOT NULL,
    PostID INT UNSIGNED NOT NULL,
    CreatedAt DATETIME DEFAULT NOW(),
    PRIMARY KEY (UserID, PostID),
    FOREIGN KEY (UserID) REFERENCES Users (UserID),
    FOREIGN KEY (PostID) REFERENCES Posts (PostID)
);

CREATE TABLE EndorsementsUsers (
    UserID INT UNSIGNED NOT NULL,
    PostID INT UNSIGNED NOT NULL,
    CreatedAt DATETIME DEFAULT NOW(),
    PRIMARY KEY (UserID, PostID),
    FOREIGN KEY (UserID) REFERENCES Users (UserID),
    FOREIGN KEY (PostID) REFERENCES Posts (PostID)
);

CREATE TABLE ExpertOpinions (
    ExpertOpID INT UNSIGNED AUTO_INCREMENT PRIMARY KEY,
    BodyText TEXT NOT NULL,
    CreatedAt DATETIME NOT NULL DEFAULT NOW(),
    PostID INT UNSIGNED NOT NULL,
    FOREIGN KEY (PostID) REFERENCES Posts (PostID)
);

CREATE TABLE ExpertOpUsers (
    UserID INT UNSIGNED NOT NULL,
    ExpertOpID INT UNSIGNED NOT NULL,
    PRIMARY KEY (UserID, ExpertOpID),
    FOREIGN KEY (UserID) REFERENCES Users (UserID),
    FOREIGN KEY (ExpertOpID) REFERENCES ExpertOpinions (ExpertOpID)
);