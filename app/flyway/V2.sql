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


INSERT INTO Institution(institutionName, parent, institutionType)
SELECT DISTINCT  eoname, eoparent, eotypename    FROM Examinations
UNION SELECT DISTINCT chemptname, NULL, NULL     FROM Examinations
UNION SELECT DISTINCT fraptname, NULL, NULL      FROM Examinations
UNION SELECT DISTINCT spaptname, NULL, NULL      FROM Examinations
UNION SELECT DISTINCT ukrptname, NULL, NULL      FROM Examinations
UNION SELECT DISTINCT deuptname, NULL, NULL      FROM Examinations
UNION SELECT DISTINCT engptname, NULL, NULL      FROM Examinations
UNION SELECT DISTINCT mathptname, NULL, NULL     FROM Examinations
UNION SELECT DISTINCT umlptname, NULL, NULL      FROM Examinations
UNION SELECT DISTINCT histptname, NULL, NULL     FROM Examinations
UNION SELECT DISTINCT geoptname, NULL, NULL      FROM Examinations
UNION SELECT DISTINCT rusptname, NULL, NULL      FROM Examinations
UNION SELECT DISTINCT bioptname, NULL, NULL      FROM Examinations
UNION SELECT DISTINCT physptname, NULL, NULL     FROM Examinations
UNION SELECT DISTINCT mathstptname, NULL, NULL   FROM Examinations;

UPDATE Institution
SET locationID = LocationInfo.locationID
WHERE Examinations.eoregname = LocationInfo.regionName AND
      Examinations.eoareaname = LocationInfo.areaName  AND
      Examinations.eotername = LocationInfo.territoryName;



INSERT INTO Student(OutID, Birth, SexTypeName, RegTypeName, ClassProfileName, ClassLangName)
SELECT DISTINCT outid, birth, sextypename, regtypename, classprofilename, classlangname;

UPDATE Student
SET locationID = LocationInfo.locationID
WHERE Examinations.regname = LocationInfo.regionName AND
      Examinations.areaname = LocationInfo.areaName  AND
      Examinations.tername = LocationInfo.territoryName;

UPDATE Student
SET InstitutionID = Institution.InstitutionID
WHERE Examinations.eoname = Institution.institutionName AND
      Examinations.eoparent = Institution.parent  AND
      Examinations.eotypename = Institution.institutionType;


-- INSERT INTO UkrTest(OutID, UkrAdaptScale, UkrSubTest)
-- SELECT DISTINCT   stid,
--

--
--
--
-- INSERT INTO Test(OutID, subject, lang, DPALevel, ball12, ball,
--                  ball100, InstitutionID, testStatus, testYear)
-- SELECT DISTINCT   outid, umltest, NULL, NULL, umlball12, umlball, umlball100, &&&, umlteststatus, year
-- FROM Examinations
-- WHERE umltest IS NOT NULL;