DROP TABLE IF EXISTS highBloodPressure;
CREATE TABLE highBloodPressure (
    Country TEXT,
    Sex VARCHAR(6),
    Year_ SMALLINT,
    avgSystolicBP DECIMAL(10, 7),
    avgDiastolicBP DECIMAL(10, 8),
    prevalenceRaisedBP DECIMAL(10, 9)
);