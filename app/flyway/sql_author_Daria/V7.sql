-- UML TEST
INSERT INTO Test(OutID, subject, lang, DPALevel, ball12, ball, ball100, testStatus, testYear)
SELECT DISTINCT   outid, umltest, NULL, NULL, umlball12, umlball, umlball100, umlteststatus, year FROM Examinations
WHERE umltest IS NOT NULL;

-- UPDATE Test
-- SET InstitutionID = Institution.InstitutionID
-- WHERE Examinations.umlptname = Institution.institutionName;

UPDATE Test
SET InstitutionID = Institution.locationID
FROM LocationInfo
INNER JOIN Examinations
ON Examinations.umlptname = Institution.institutionName AND
   Examinations.umlptareaname = Institution.areaName;


-- MATH STANDARD TEST
INSERT INTO Test(OutID, subject, lang, DPALevel, ball12, ball, ball100, testStatus, testYear)
SELECT DISTINCT   outid, mathsttest, mathstlang, NULL, mathstball12, mathstball, NULL, mathstteststatus, year FROM Examinations
WHERE mathsttest IS NOT NULL;

-- UPDATE Test
-- SET InstitutionID = Institution.InstitutionID
-- WHERE Examinations.mathstptname = Institution.institutionName;
UPDATE Test
SET InstitutionID = Institution.locationID
FROM LocationInfo
INNER JOIN Examinations
ON Examinations.mathstptname = Institution.institutionName AND
   Examinations.mathstptareaname = Institution.areaName;

--PHYSICS TEST
INSERT INTO Test(OutID, subject, lang, DPALevel, ball12, ball, ball100, testStatus, testYear)
SELECT DISTINCT   outid, phystest, physlang, NULL, physball12, physball, physball100, physteststatus, year FROM Examinations
WHERE phystest IS NOT NULL;
--
-- UPDATE Test
-- SET InstitutionID = Institution.InstitutionID
-- WHERE Examinations.physptname = Institution.institutionName;
UPDATE Test
SET InstitutionID = Institution.locationID
FROM LocationInfo
INNER JOIN Examinations
ON Examinations.physptname = Institution.institutionName AND
   Examinations.physptareaname = Institution.areaName;