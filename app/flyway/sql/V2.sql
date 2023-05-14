DROP TABLE IF EXISTS Test;
DROP TABLE IF EXISTS UkrTest;
DROP TABLE IF EXISTS Student;
DROP TABLE IF EXISTS Institution;
DROP TABLE IF EXISTS LocationInfo;


CREATE TABLE LocationInfo(
    locationID          SERIAL NOT NULL,
    regionName          VARCHAR,
    areaName            VARCHAR,
    territoryName       VARCHAR,
    PRIMARY KEY(locationID)
);

CREATE TABLE Institution(
    InstitutionID       SERIAL NOT NULL,
    institutionName     VARCHAR,
    locationID          INTEGER,
    parent              VARCHAR,
    institutionType     VARCHAR,
    PRIMARY KEY(InstitutionID),
    FOREIGN KEY(locationID) REFERENCES LocationInfo(locationID)
);


CREATE TABLE Student(
    OutID               SERIAL NOT NULL,
    Birth               SMALLINT NOT NULL,
    SexTypeName         VARCHAR NOT NULL,
    InstitutionID       INTEGER,
    RegTypeName         VARCHAR NOT NULL,
    ClassProfileName    VARCHAR,
    ClassLangName       VARCHAR,
    locationID          INTEGER,
    PRIMARY KEY(OutID),
    FOREIGN KEY(InstitutionID) REFERENCES Institution(InstitutionID)
);


CREATE TABLE UkrTest(
    testID          SERIAL NOT NULL,
    OutID           INTEGER NOT NULL,
    UkrAdaptScale   SMALLINT,
    UkrSubTest      BOOLEAN,
    PRIMARY KEY(testID, OutID),
    FOREIGN KEY(OutID) REFERENCES Student(OutID)
);


CREATE TABLE Test(
    testID          SERIAL NOT NULL,
    OutID           INTEGER NOT NULL,
    subject         VARCHAR,
    lang            VARCHAR,
    DPALevel        VARCHAR,
    ball12          NUMERIC(4, 1),
    ball            NUMERIC(4, 1),
    ball100         NUMERIC(4, 1),
    InstitutionID   INTEGER,
    testStatus      VARCHAR,
    testYear        SMALLINT NOT NULL,
    PRIMARY KEY(testID, OutID),
    FOREIGN KEY(OutID) REFERENCES Student(OutID),
    FOREIGN KEY(InstitutionID) REFERENCES Institution(InstitutionID)
);
