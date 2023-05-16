
INSERT INTO Student(OutID, Birth, SexTypeName, RegTypeName, ClassProfileName, ClassLangName)
SELECT DISTINCT outid, birth, sextypename, regtypename, classprofilename, classlangname;

-- UPDATE Student
-- SET locationID = LocationInfo.locationID
-- WHERE Examinations.regname = LocationInfo.regionName AND
--       Examinations.areaname = LocationInfo.areaName  AND
--       Examinations.tername = LocationInfo.territoryName;



UPDATE Student
SET locationID = LocationInfo.locationID
FROM LocationInfo
INNER JOIN Examinations
ON Examinations.eoregname = LocationInfo.regionName AND
   Examinations.eoareaname = LocationInfo.areaName  AND
   Examinations.eotername = LocationInfo.territoryName;



-- UPDATE Student
-- SET InstitutionID = Institution.InstitutionID
-- WHERE Examinations.eoname = Institution.institutionName AND
--       Examinations.eoparent = Institution.parent  AND
--       Examinations.eotypename = Institution.institutionType;

UPDATE Student
SET InstitutionID = Institution.locationID
FROM LocationInfo
INNER JOIN Examinations
ON Examinations.eoname = Institution.institutionName AND
   Examinations.eoparent = Institution.parent  AND
   Examinations.eotypename = Institution.institutionType;


ALTER TABLE Student ADD CONSTRAINT fk_institution FOREIGN KEY(InstitutionID) REFERENCES Institution(InstitutionID);
