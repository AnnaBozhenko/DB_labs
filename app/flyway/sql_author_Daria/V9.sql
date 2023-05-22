--RUS TEST
INSERT INTO Test(OutID, subject, lang, DPALevel, ball12, ball, ball100, testStatus, testYear)
SELECT DISTINCT   outid, rustest, NULL, NULL, rusball12, NULL, rusball100, rusteststatus, year FROM Examinations
WHERE rustest IS NOT NULL;

-- UPDATE Test
-- SET InstitutionID = Institution.InstitutionID
-- WHERE Examinations.rusptname = Institution.institutionName;
UPDATE Test
SET InstitutionID = Institution.locationID
FROM LocationInfo
INNER JOIN Examinations
ON Examinations.rusptname = Institution.institutionName AND
   Examinations.rusptareaname = Institution.areaName;

--UKR TEST
INSERT INTO Test(OutID, subject, lang, DPALevel, ball12, ball, ball100, testStatus, testYear)
SELECT DISTINCT   outid, ukrtest, NULL, NULL, ukrball12, ukrball, ukrball100, ukrteststatus, year FROM Examinations
WHERE ukrtest IS NOT NULL;

-- UPDATE Test
-- SET InstitutionID = Institution.InstitutionID
-- WHERE Examinations.ukrptname = Institution.institutionName;
UPDATE Test
SET InstitutionID = Institution.locationID
FROM LocationInfo
INNER JOIN Examinations
ON Examinations.ukrptname = Institution.institutionName AND
   Examinations.ukrptareaname = Institution.areaName;

--MATH TEST
INSERT INTO Test(OutID, subject, lang, DPALevel, ball12, ball, ball100, testStatus, testYear)
SELECT DISTINCT   outid, mathtest, mathlang, mathdpalevel, mathball12, mathball, mathball100, mathteststatus, year FROM Examinations
WHERE mathtest IS NOT NULL;

-- UPDATE Test
-- SET InstitutionID = Institution.InstitutionID
-- WHERE Examinations.mathptname = Institution.institutionName;
UPDATE Test
SET InstitutionID = Institution.locationID
FROM LocationInfo
INNER JOIN Examinations
ON Examinations.mathptname = Institution.institutionName AND
   Examinations.mathptareaname = Institution.areaName;