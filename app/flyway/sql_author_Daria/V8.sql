--DEU TEST
INSERT INTO Test(OutID, subject, lang, DPALevel, ball12, ball, ball100, testStatus, testYear)
SELECT DISTINCT   outid, deutest, NULL, deudpalevel, deuball12, deuball, deuball100, deuteststatus, year FROM Examinations
WHERE deutest IS NOT NULL;

-- UPDATE Test
-- SET InstitutionID = Institution.InstitutionID
-- WHERE Examinations.deuptname = Institution.institutionName;
UPDATE Test
SET InstitutionID = Institution.locationID
FROM LocationInfo
INNER JOIN Examinations
ON Examinations.deuptname = Institution.institutionName AND
   Examinations.deuptareaname = Institution.areaName;

--SPA TEST
INSERT INTO Test(OutID, subject, lang, DPALevel, ball12, ball, ball100, testStatus, testYear)
SELECT DISTINCT   outid, spatest, NULL, spadpalevel, spaball12, spaball, spaball100, spateststatus, year FROM Examinations
WHERE spatest IS NOT NULL;

-- UPDATE Test
-- SET InstitutionID = Institution.InstitutionID
-- WHERE Examinations.spptregname = Institution.institutionName;
UPDATE Test
SET InstitutionID = Institution.locationID
FROM LocationInfo
INNER JOIN Examinations
ON Examinations.spptregname = Institution.institutionName AND
   Examinations.spptareaname = Institution.areaName;

--FRA TEST
INSERT INTO Test(OutID, subject, lang, DPALevel, ball12, ball, ball100, testStatus, testYear)
SELECT DISTINCT   outid, fratest, NULL, fradpalevel, fraball12, fraball, fraball100, frateststatus, year FROM Examinations
WHERE fratest IS NOT NULL;

-- UPDATE Test
-- SET InstitutionID = Institution.InstitutionID
-- WHERE Examinations.frptname = Institution.institutionName;
UPDATE Test
SET InstitutionID = Institution.locationID
FROM LocationInfo
INNER JOIN Examinations
ON Examinations.frptname = Institution.institutionName AND
   Examinations.frptareaname = Institution.areaName;


--ENG TEST
INSERT INTO Test(OutID, subject, lang, DPALevel, ball12, ball, ball100, testStatus, testYear)
SELECT DISTINCT   outid, engtest, NULL, engdpalevel, engball12, engball, engball100, engteststatus, year FROM Examinations
WHERE engtest IS NOT NULL;

-- UPDATE Test
-- SET InstitutionID = Institution.InstitutionID
-- WHERE Examinations.engptname = Institution.institutionName;
UPDATE Test
SET InstitutionID = Institution.locationID
FROM LocationInfo
INNER JOIN Examinations
ON Examinations.engptname = Institution.institutionName AND
   Examinations.engptareaname = Institution.areaName;
