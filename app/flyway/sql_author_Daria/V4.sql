
INSERT INTO Institution(institutionName, parent, institutionType)
SELECT DISTINCT  eoname, eoparent, eotypename    FROM Examinations;
-- UNION SELECT DISTINCT chemptname, NULL, NULL     FROM Examinations
-- UNION SELECT DISTINCT frptname, NULL, NULL      FROM Examinations
-- UNION SELECT DISTINCT spptname, NULL, NULL      FROM Examinations
-- UNION SELECT DISTINCT ukrptname, NULL, NULL      FROM Examinations
-- UNION SELECT DISTINCT deuptname, NULL, NULL      FROM Examinations
-- UNION SELECT DISTINCT engptname, NULL, NULL      FROM Examinations
-- UNION SELECT DISTINCT mathptname, NULL, NULL     FROM Examinations
-- UNION SELECT DISTINCT umlptname, NULL, NULL      FROM Examinations
-- UNION SELECT DISTINCT histptname, NULL, NULL     FROM Examinations
-- UNION SELECT DISTINCT geoptname, NULL, NULL      FROM Examinations
-- UNION SELECT DISTINCT rusptname, NULL, NULL      FROM Examinations
-- UNION SELECT DISTINCT bioptname, NULL, NULL      FROM Examinations
-- UNION SELECT DISTINCT physptname, NULL, NULL     FROM Examinations
-- UNION SELECT DISTINCT mathstptname, NULL, NULL   FROM Examinations;

-- UPDATE Institution
-- SET locationID = LocationInfo.locationID
-- WHERE Examinations.eoregname = LocationInfo.regionName AND
--       Examinations.eoareaname = LocationInfo.areaName  AND
--       Examinations.eotername = LocationInfo.territoryName;



UPDATE Institution
SET locationID = LocationInfo.locationID
FROM LocationInfo
INNER JOIN Examinations
ON Examinations.eoregname = LocationInfo.regionName AND
   Examinations.eoareaname = LocationInfo.areaName  AND
   Examinations.eotername = LocationInfo.territoryName;


ALTER TABLE Institution ADD COLUMN InstitutionID SERIAL PRIMARY KEY;
ALTER TABLE Institution ADD CONSTRAINT fk_location  FOREIGN KEY(locationID) REFERENCES  LocationInfo(locationID);

