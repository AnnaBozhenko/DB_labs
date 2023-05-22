INSERT INTO UkrTest(OutID, UkrAdaptScale, UkrSubTest)
SELECT DISTINCT  stid, ukradaptscale, ukrsubtest FROM Examinations;