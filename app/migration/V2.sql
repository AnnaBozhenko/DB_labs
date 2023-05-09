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


INSERT INTO UkrTest(OutID, UkrAdaptScale, UkrSubTest)
SELECT DISTINCT  stid, ukradaptscale, ukrsubtest FROM Examinations;
--SELECT DISTINCT  stid, umladaptscale, ukrsubtest FROM Examinations;


-- UML TEST
INSERT INTO Test(OutID, subject, lang, DPALevel, ball12, ball, ball100, testStatus, testYear)
SELECT DISTINCT   outid, umltest, NULL, NULL, umlball12, umlball, umlball100, umlteststatus, year FROM Examinations
WHERE umltest IS NOT NULL;

UPDATE Test
SET InstitutionID = Institution.InstitutionID
WHERE Examinations.umlptname = Institution.institutionName;


-- MATH STANDARD TEST
INSERT INTO Test(OutID, subject, lang, DPALevel, ball12, ball, ball100, testStatus, testYear)
SELECT DISTINCT   outid, mathsttest, mathstlang, NULL, mathstball12, mathstball, NULL, mathstteststatus, year FROM Examinations
WHERE mathsttest IS NOT NULL;

UPDATE Test
SET InstitutionID = Institution.InstitutionID
WHERE Examinations.mathstptname = Institution.institutionName;


--PHYSICS TEST
INSERT INTO Test(OutID, subject, lang, DPALevel, ball12, ball, ball100, testStatus, testYear)
SELECT DISTINCT   outid, phystest, physlang, NULL, physball12, physball, physball100, physteststatus, year FROM Examinations
WHERE phystest IS NOT NULL;

UPDATE Test
SET InstitutionID = Institution.InstitutionID
WHERE Examinations.physptname = Institution.institutionName;


--DEU TEST
INSERT INTO Test(OutID, subject, lang, DPALevel, ball12, ball, ball100, testStatus, testYear)
SELECT DISTINCT   outid, deutest, NULL, deudpalevel, deuball12, deuball, deuball100, deuteststatus, year FROM Examinations
WHERE deutest IS NOT NULL;

UPDATE Test
SET InstitutionID = Institution.InstitutionID
WHERE Examinations.deuptname = Institution.institutionName;


--SPA TEST
INSERT INTO Test(OutID, subject, lang, DPALevel, ball12, ball, ball100, testStatus, testYear)
SELECT DISTINCT   outid, spatest, NULL, spadpalevel, spaball12, spaball, spaball100, spateststatus, year FROM Examinations
WHERE spatest IS NOT NULL;

UPDATE Test
SET InstitutionID = Institution.InstitutionID
WHERE Examinations.spaptregname = Institution.institutionName;


--FRA TEST
INSERT INTO Test(OutID, subject, lang, DPALevel, ball12, ball, ball100, testStatus, testYear)
SELECT DISTINCT   outid, fratest, NULL, fradpalevel, fraball12, fraball, fraball100, frateststatus, year FROM Examinations
WHERE fratest IS NOT NULL;

UPDATE Test
SET InstitutionID = Institution.InstitutionID
WHERE Examinations.fraptname = Institution.institutionName;


--ENG TEST
INSERT INTO Test(OutID, subject, lang, DPALevel, ball12, ball, ball100, testStatus, testYear)
SELECT DISTINCT   outid, engtest, NULL, engdpalevel, engball12, engball, engball100, engteststatus, year FROM Examinations
WHERE engtest IS NOT NULL;

UPDATE Test
SET InstitutionID = Institution.InstitutionID
WHERE Examinations.engptname = Institution.institutionName;


--RUS TEST
INSERT INTO Test(OutID, subject, lang, DPALevel, ball12, ball, ball100, testStatus, testYear)
SELECT DISTINCT   outid, rustest, NULL, NULL, rusball12, NULL, rusball100, rusteststatus, year FROM Examinations
WHERE rustest IS NOT NULL;

UPDATE Test
SET InstitutionID = Institution.InstitutionID
WHERE Examinations.rusptname = Institution.institutionName;


--UKR TEST
INSERT INTO Test(OutID, subject, lang, DPALevel, ball12, ball, ball100, testStatus, testYear)
SELECT DISTINCT   outid, ukrtest, NULL, NULL, ukrball12, ukrball, ukrball100, ukrteststatus, year FROM Examinations
WHERE ukrtest IS NOT NULL;

UPDATE Test
SET InstitutionID = Institution.InstitutionID
WHERE Examinations.ukrptname = Institution.institutionName;


--MATH TEST
INSERT INTO Test(OutID, subject, lang, DPALevel, ball12, ball, ball100, testStatus, testYear)
SELECT DISTINCT   outid, mathtest, mathlang, mathdpalevel, mathball12, mathball, mathball100, mathteststatus, year FROM Examinations
WHERE mathtest IS NOT NULL;

UPDATE Test
SET InstitutionID = Institution.InstitutionID
WHERE Examinations.mathptname = Institution.institutionName;


--BIO TEST
INSERT INTO Test(OutID, subject, lang, DPALevel, ball12, ball, ball100, testStatus, testYear)
SELECT DISTINCT   outid, biotest, biolang, NULL, bioball12, bioball, bioball100, bioteststatus, year FROM Examinations
WHERE biotest IS NOT NULL;

UPDATE Test
SET InstitutionID = Institution.InstitutionID
WHERE Examinations.bioptname = Institution.institutionName;


--HIST TEST
INSERT INTO Test(OutID, subject, lang, DPALevel, ball12, ball, ball100, testStatus, testYear)
SELECT DISTINCT   outid, histtest, histlang, NULL, histball12, histball, histball100, histteststatus, year FROM Examinations
WHERE histtest IS NOT NULL;

UPDATE Test
SET InstitutionID = Institution.InstitutionID
WHERE Examinations.histptname = Institution.institutionName;


--CHEM TEST
INSERT INTO Test(OutID, subject, lang, DPALevel, ball12, ball, ball100, testStatus, testYear)
SELECT DISTINCT   outid, chemtest, chemlang, NULL, chemball12, chemball, chemball100, chemteststatus, year FROM Examinations
WHERE chemtest IS NOT NULL;

UPDATE Test
SET InstitutionID = Institution.InstitutionID
WHERE Examinations.chemptname = Institution.institutionName;


--GEO TEST
INSERT INTO Test(OutID, subject, lang, DPALevel, ball12, ball, ball100, testStatus, testYear)
SELECT DISTINCT   outid, geotest, geolang, NULL, geoball12, geoball, geoball100, geoteststatus, year FROM Examinations
WHERE geotest IS NOT NULL;

UPDATE Test
SET InstitutionID = Institution.InstitutionID
WHERE Examinations.geoptname = Institution.institutionName;