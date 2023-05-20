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
UNION SELECT DISTINCT    spptregname, spptareaname, sppttername             FROM Examinations
UNION SELECT DISTINCT    frptregname, frptareaname, frpttername          FROM Examinations
UNION SELECT DISTINCT    mathptregname, mathptareaname, mathpttername       FROM Examinations;

