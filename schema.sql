CREATE TABLE semestres (
    id INT AUTO_INCREMENT PRIMARY KEY,
    nom VARCHAR(50) NOT NULL -- ex: Semestre 1, Semestre 2
);

CREATE TABLE blocs_competences (
    id INT AUTO_INCREMENT PRIMARY KEY,
    nom VARCHAR(100) NOT NULL, -- ex: Administration Réseaux
    id_semestre INT,
    FOREIGN KEY (id_semestre) REFERENCES semestres(id)
);

CREATE TABLE competences (
    id INT AUTO_INCREMENT PRIMARY KEY,
    nom VARCHAR(100) NOT NULL,
    niveau INT DEFAULT 0, -- de 0 à 100
    id_bloc INT,
    FOREIGN KEY (id_bloc) REFERENCES blocs_competences(id)
);