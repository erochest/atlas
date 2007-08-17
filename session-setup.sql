
CREATE DATABASE lap_sessions;
USE lap_sessions;
CREATE TABLE sessions (
  ID          VARCHAR(8) NOT NULL,
  hash        VARCHAR(8) NOT NULL,
  data        BLOB NOT NULL,
  created     INT UNSIGNED NOT NULL,
  updated     INT UNSIGNED NOT NULL,
  PRIMARY KEY (ID)
);
GRANT DELETE, INSERT, SELECT, UPDATE
ON lap_sessions.*
TO webuser@localhost IDENTIFIED BY 'webuser';

