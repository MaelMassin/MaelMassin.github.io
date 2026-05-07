-- 1. ON CRÉE LES TABLES (Ordre : Semestre -> Bloc -> Compétence)
CREATE TABLE IF NOT EXISTS semestres (
    id INT AUTO_INCREMENT PRIMARY KEY,
    nom VARCHAR(50),
    code VARCHAR(10)
);

CREATE TABLE IF NOT EXISTS blocs (
    id INT AUTO_INCREMENT PRIMARY KEY,
    nom VARCHAR(100),
    code VARCHAR(20),
    semestre_id INT,
    FOREIGN KEY (semestre_id) REFERENCES semestres(id)
);

CREATE TABLE IF NOT EXISTS competences (
    id INT AUTO_INCREMENT PRIMARY KEY,
    code VARCHAR(20),
    nom VARCHAR(255),
    fait TEXT,
    pourquoi TEXT,
    comment TEXT,
    difficultes TEXT,
    appris TEXT,
    autrement TEXT,
    niveau VARCHAR(50),
    bloc_id INT,
    FOREIGN KEY (bloc_id) REFERENCES blocs(id)
);

-- 2. ON INSÈRE LES DONNÉES DE TEST
INSERT INTO semestres (nom, code) VALUES ('Semestre 1', 'S1');

-- Ici le semestre_id est 1 car c'est la première ligne du dessus
INSERT INTO blocs (nom, code, semestre_id) VALUES ('Connecter', 'RT1-B1', 1);

-- Ici le bloc_id est 1 car c'est la première ligne du dessus
INSERT INTO competences (code, nom, niveau, bloc_id, fait) 
VALUES ('AC12.01', 'Mesurer des signaux', 'Expert', 1, 'Mesures de signaux électriques via oscilloscope.');