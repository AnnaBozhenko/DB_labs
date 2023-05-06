DROP TABLE IF EXISTS Student;
DROP TABLE IF EXISTS UkrTest;
DROP TABLE IF EXISTS Test;
DROP TABLE IF EXISTS Institution;
DROP TABLE IF EXISTS LocationInfo;


CREATE TABLE LocationInfo(
    locationID          SERIAL NOT NULL PRIMARY KEY,
    regionName          VARCHAR NULL,
    areaName            VARCHAR NULL,
    territoryName       VARCHAR NULL,
    territoryType       VARCHAR NULL
);


CREATE TABLE Institution(
    InstitutionID       SERIAL NOT NULL PRIMARY KEY,
    locationID          SERIAL NOT NULL REFERENCES LocationInfo(locationID),
    parent              VARCHAR NOT NULL,
    institutionType     VARCHAR NULL
);


CREATE TABLE Student(
    OutID               SERIAL NOT NULL PRIMARY KEY,
    Birth               SMALLINT NOT NULL,
    SexTypeName         VARCHAR NOT NULL,
    InstitutionID       SERIAL NOT NULL REFERENCES Institution(InstitutionID),
    RegTypeName         VARCHAR NOT NULL,
    ClassProfileName    VARCHAR NULL,
    ClassLangName       VARCHAR NULL,
    locationID          SERIAL NOT NULL
);


CREATE TABLE UkrTest(
    testID          SERIAL NOT NULL,
    OutID           SERIAL NOT NULL REFERENCES Student(OutID),
    UkrAdaptScale   SMALLINT NULL,
    UkrSubTest      BOOLEAN NULL,
    PRIMARY KEY(testID, OutID)
);


CREATE TABLE Test(
    testID          SERIAL NOT NULL,
    OutID           SERIAL NOT NULL,
    subject         VARCHAR NULL,
    lang            VARCHAR NULL,
    DPALevel        VARCHAR NULL,
    ball12          NUMERIC(4, 1) NULL,
    ball            NUMERIC(4, 1) NULL,
    ball100         NUMERIC(4, 1) NULL,
    InstitutionID   SERIAL NOT NULL REFERENCES Institution(InstitutionID),
    testStatus      VARCHAR NULL,
    testYear        SMALLINT NOT NULL,
    PRIMARY KEY(testID, OutID)
);

