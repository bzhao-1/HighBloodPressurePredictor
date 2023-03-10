DROP TABLE IF EXISTS earthquakes;
CREATE TABLE earthquakes (
  quaketime TIMESTAMP,
  latitude REAL,
  longitude REAL,
  quakedepth REAL,
  mag REAL,
  magType TEXT,
  nst INT,
  gap REAL,
  dmin REAL,
  rms REAL,
  net CHAR(2),
  place VARCHAR,
  horizontalError REAL,
  depthError REAL,
  magError REAL, 
  magNst INT,
  locationSource CHAR(2),
  magSource CHAR(3)
);