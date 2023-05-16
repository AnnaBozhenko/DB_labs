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
    institutionName     VARCHAR,
    locationID          INTEGER,
    parent              VARCHAR,
    institutionType     VARCHAR,
    FOREIGN KEY(locationID) REFERENCES LocationInfo(locationID)
);


CREATE TABLE Student(
    OutID               VARCHAR NOT NULL,
    Birth               SMALLINT NOT NULL,
    SexTypeName         VARCHAR NOT NULL,
    InstitutionID       INTEGER,
    RegTypeName         VARCHAR NOT NULL,
    ClassProfileName    VARCHAR,
    ClassLangName       VARCHAR,
    UkrAdaptScale       SMALLINT,
    UkrSubTest          BOOLEAN,
    locationID          INTEGER,
    PRIMARY KEY(OutID)
);



CREATE TABLE Test(
    OutID           VARCHAR NOT NULL,
    subject         VARCHAR,
    lang            VARCHAR,
    DPALevel        VARCHAR,
    ball12          NUMERIC(4, 1),
    ball            NUMERIC(4, 1),
    ball100         NUMERIC(4, 1),
    InstitutionID   INTEGER,
    testStatus      VARCHAR,
    testYear        SMALLINT NOT NULL,
    FOREIGN KEY(OutID) REFERENCES Student(OutID)
);
