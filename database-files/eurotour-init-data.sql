DROP DATABASE IF EXISTS EuroTour;

CREATE DATABASE EuroTour;

USE EuroTour;

CREATE TABLE road_quality (
    country VARCHAR(255) NOT NULL,
    year YEAR,
    score DECIMAL,
    PRIMARY KEY (country, year)
);

CREATE TABLE tourism_prioritization (
    country VARCHAR(255) NOT NULL,
    year YEAR,
    score DECIMAL,
    PRIMARY KEY (country, year)
);

CREATE TABLE road_density (
    country VARCHAR(255) NOT NULL,
    year YEAR,
    value DECIMAL,
    score DECIMAL,
    PRIMARY KEY (country, year)
);

CREATE TABLE avg_fuel_price (
    country VARCHAR(255) NOT NULL,
    year YEAR,
    score DECIMAL,
    value DECIMAL,
    PRIMARY KEY (country, year)
);

CREATE TABLE road_spending (
    country VARCHAR(255) NOT NULL,
    year YEAR,
    road_spending DECIMAL,
    gdp DECIMAL,
    spending_by_gdp_percent DECIMAL,
    PRIMARY KEY (country, year),
    CONSTRAINT fk_3 FOREIGN KEY (country, year) REFERENCES road_quality (country, year)
);

CREATE TABLE passenger_cars (
    country VARCHAR(255) NOT NULL,
    year YEAR,
    motor_type VARCHAR(50),
    engine_size VARCHAR(100),
    num_cars INTEGER,
    PRIMARY KEY (country, year, motor_type, engine_size),
    CONSTRAINT fk_2 FOREIGN KEY (country, year) REFERENCES road_quality (country, year),
    CONSTRAINT fk_5 FOREIGN KEY (country, year) REFERENCES road_density (country, year),
    CONSTRAINT fk_6 FOREIGN KEY (country, year) REFERENCES avg_fuel_price (country, year)
);

CREATE TABLE trips (
    country VARCHAR(255) NOT NULL,
    year YEAR,
    purpose VARCHAR(255),
    duration VARCHAR(255),
    num_trips INTEGER,
    PRIMARY KEY (country, year, purpose, duration),
    CONSTRAINT fk_1 FOREIGN KEY (country, year) REFERENCES road_quality (country, year),
    CONSTRAINT fk_4 FOREIGN KEY (country, year) REFERENCES tourism_prioritization (country, year)
);