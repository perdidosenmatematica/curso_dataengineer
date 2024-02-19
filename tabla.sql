-- Para subirlo a redshift debemos crear una tabla en la que volcaremos la extracción

CREATE TABLE IF NOT EXISTS tabla_ticketmaster_musica (
    name VARCHAR(255),
    id INT PRIMARY KEY,
    url VARCHAR(255),
    locale VARCHAR(50),
    startDateTime DATETIME,
    endDateTime DATETIME,
    timezone VARCHAR(50),
    localDate DATE,
    localTime TIME,
    type VARCHAR(50),
    currency VARCHAR(10),
    min DECIMAL(10, 2),
    max DECIMAL(10, 2)
);
)

