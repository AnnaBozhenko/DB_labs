--BIO TEST
INSERT INTO Test(OutID, subject, lang, DPALevel, ball12, ball, ball100, testStatus, testYear)
SELECT DISTINCT   outid, biotest, biolang, NULL, bioball12, bioball, bioball100, bioteststatus, year FROM Examinations
WHERE biotest IS NOT NULL;

-- UPDATE Test
-- SET InstitutionID = Institution.InstitutionID
-- WHERE Examinations.bioptname = Institution.institutionName;
UPDATE Test
SET InstitutionID = Institution.locationID
FROM LocationInfo
INNER JOIN Examinations
ON Examinations.bioptname = Institution.institutionName AND
   Examinations.bioptareaname = Institution.areaName;

--HIST TEST
INSERT INTO Test(OutID, subject, lang, DPALevel, ball12, ball, ball100, testStatus, testYear)
SELECT DISTINCT   outid, histtest, histlang, NULL, histball12, histball, histball100, histteststatus, year FROM Examinations
WHERE histtest IS NOT NULL;

-- UPDATE Test
-- SET InstitutionID = Institution.InstitutionID
-- WHERE Examinations.histptname = Institution.institutionName;
UPDATE Test
SET InstitutionID = Institution.locationID
FROM LocationInfo
INNER JOIN Examinations
ON Examinations.histptname = Institution.institutionName AND
   Examinations.histptareaname = Institution.areaName;


--CHEM TEST
INSERT INTO Test(OutID, subject, lang, DPALevel, ball12, ball, ball100, testStatus, testYear)
SELECT DISTINCT   outid, chemtest, chemlang, NULL, chemball12, chemball, chemball100, chemteststatus, year FROM Examinations
WHERE chemtest IS NOT NULL;

-- UPDATE Test
-- SET InstitutionID = Institution.InstitutionID
-- WHERE Examinations.chemptname = Institution.institutionName;
UPDATE Test
SET InstitutionID = Institution.locationID
FROM LocationInfo
INNER JOIN Examinations
ON Examinations.chemptname = Institution.institutionName AND
   Examinations.chemptareaname = Institution.areaName;

--GEO TEST
INSERT INTO Test(OutID, subject, lang, DPALevel, ball12, ball, ball100, testStatus, testYear)
SELECT DISTINCT   outid, geotest, geolang, NULL, geoball12, geoball, geoball100, geoteststatus, year FROM Examinations
WHERE geotest IS NOT NULL;

-- UPDATE Test
-- SET InstitutionID = Institution.InstitutionID
-- WHERE Examinations.geoptname = Institution.institutionName;
UPDATE Test
SET InstitutionID = Institution.locationID
FROM LocationInfo
INNER JOIN Examinations
ON Examinations.geoptname = Institution.institutionName AND
   Examinations.geoptareaname = Institution.areaName;


