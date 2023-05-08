--Examinations
INSERT INTO LocationInfo(regionName, areaName, territoryName)
SELECT DISTINCT          regname, areaname, tername                         FROM Examinations
UNION SELECT DISTINCT    eoregname, eoareaname, eotername                   FROM Examinations
UNION SELECT DISTINCT    chemptregname, chemptareaname, chempttername       FROM Examinations
UNION SELECT DISTINCT    umlptregname, umlptareaname, umlpttername          FROM Examinations
UNION SELECT DISTINCT    deuptregname, deuptareaname, deupttername          FROM Examinations
UNION SELECT DISTINCT    rusptregname, rusptareaname, ruspttername          FROM Examinations
UNION SELECT DISTINCT    ukrptregname, ukrptareaname, ukrpttername          FROM Examinations
UNION SELECT DISTINCT    bioptregname, bioptareaname, biopttername          FROM Examinations
UNION SELECT DISTINCT    engptregname, engptareaname, engpttername          FROM Examinations
UNION SELECT DISTINCT    geoptregname, geoptareaname, geopttername          FROM Examinations
UNION SELECT DISTINCT    mathstptregname, mathstptareaname, mathstpttername FROM Examinations
UNION SELECT DISTINCT    histptregname, histptareaname,  histpttername      FROM Examinations
UNION SELECT DISTINCT    physptregname, physptareaname, physpttername       FROM Examinations
UNION SELECT DISTINCT    spaptregname, spaptareaname, spapttername          FROM Examinations
UNION SELECT DISTINCT    fraptregname, fraptareaname, frapttername          FROM Examinations
UNION SELECT DISTINCT    mathptregname, mathptareaname, mathpttername       FROM Examinations;





-- INSERT INTO Institution(InstitutionID, locationID, parent, institutionType)
--
--
--
-- INSERT INTO Student(OutID, Birth, SexTypeName, InstitutionID, RegTypeName, ClassProfileName,
--                     ClassLangName, locationID)
--
--
--
--
-- INSERT INTO UkrTest(OutID, UkrAdaptScale, UkrSubTest)
-- SELECT DISTINCT   stid,
--
--
--
--
--
-- INSERT INTO Test(OutID, subject, lang, DPALevel, ball12, ball,
--                  ball100, InstitutionID, testStatus, testYear)
-- SELECT DISTINCT   outid, umltest, NULL, NULL, umlball12, umlball, umlball100, &&&, umlteststatus, year
-- FROM Examinations
-- WHERE umltest IS NOT NULL;