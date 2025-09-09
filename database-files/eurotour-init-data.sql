DROP DATABASE IF EXISTS EuroTour;

CREATE DATABASE EuroTour;

USE EuroTour;

CREATE TABLE RoadQuality (
    Country VARCHAR(255) NOT NULL,
    RoadYear YEAR,
    Score DECIMAL,
    PRIMARY KEY (Country, RoadYear)
);

CREATE TABLE TourismPrioritization (
    Country VARCHAR(255) NOT NULL,
    TourismYear YEAR,
    Score DECIMAL(1, 4),
    PRIMARY KEY (Country, TourismYear)
);

CREATE TABLE RoadDensity (
    Country VARCHAR(255) NOT NULL,
    DataYear YEAR,
    KmRoadPerKmSquared DECIMAL(3, 3),
    Score DECIMAL(1, 4),
    PRIMARY KEY (country, DataYear)
);

CREATE TABLE AvgFuelPrice (
    Country VARCHAR(255) NOT NULL,
    FuelPriceYear YEAR,
    Score DECIMAL(1, 4),
    AvgPricePerLiter DECIMAL(1, 4),
    PRIMARY KEY (Country, FuelPriceYear)
);

CREATE TABLE RoadSpending (
    Country VARCHAR(255) NOT NULL,
    SpendingYear YEAR,
    RoadSpending DECIMAL(2, 6),
    GDP DECIMAL(2, 6),
    SpendingByGDPPercent DECIMAL(2, 6),
    PRIMARY KEY (Country, SpendingYear),
    CONSTRAINT fk_3 FOREIGN KEY (country, year) REFERENCES RoadQuality (Country, SpendingYear)
);

CREATE TABLE PassengerCars (
    Country VARCHAR(255) NOT NULL,
    PCDataYear YEAR,
    MotorType VARCHAR(50),
    EngineSize VARCHAR(100),
    Numcars INT,
    PRIMARY KEY (Country, PCDataYear, MotorType, EngineSize),
    CONSTRAINT fk_2 FOREIGN KEY (country, year) REFERENCES RoadQuality (Country, PCDataYear),
    CONSTRAINT fk_5 FOREIGN KEY (country, year) REFERENCES RoadDensity (Country, PCDataYear),
    CONSTRAINT fk_6 FOREIGN KEY (country, year) REFERENCES AvgFuelPrice (Country, PCDataYear)
);

CREATE TABLE Trips (
    Country VARCHAR(255) NOT NULL,
    TripYear YEAR,
    Purpose VARCHAR(255),
    Duration VARCHAR(255),
    NumTrips INTEGER,
    PRIMARY KEY (Country, TripYear, Purpose, Duration),
    CONSTRAINT fk_1 FOREIGN KEY (Country, TripYear) REFERENCES RoadQuality (Country, TripYear),
    CONSTRAINT fk_4 FOREIGN KEY (Country, TripYear) REFERENCES TourismPrioritization (Country, TripYear)
);


-- Researcher Stuff
CREATE TABLE Researcher (
    ResearcherID INT AUTO_INCREMENT PRIMARY KEY,
    ResearcherName VARCHAR(255),
    FieldOfStudy VARCHAR(255)
);

CREATE TABLE ResearchFindings (
    ResearchPostID INT AUTO_INCREMENT PRIMARY KEY,
    Title VARCHAR(255),
    PostDate DATE,
    Research TEXT,
    AuthorID INT,
    FOREIGN KEY (AuthorID) REFERENCES Researcher (AuthorID)
);

CREATE TABLE Image (
    ImageID INT AUTO_INCREMENT PRIMARY KEY,
    Link VARCHAR(255),
    ResearchPostID INT,
    FOREIGN KEY (ResearchPostID) REFERENCES ResearchFindings (ResearchPostID)
);