-- Таблица пользователей (только студенты)
CREATE TABLE users (
    id VARCHAR(36) PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    email VARCHAR(100) NOT NULL UNIQUE,
    role VARCHAR(20) NOT NULL,
    group_id VARCHAR(20),
    department VARCHAR(100),
    CONSTRAINT chk_role CHECK (role = 'student')
);

-- Таблица групп
CREATE TABLE groups (
    id VARCHAR(20) PRIMARY KEY,
    name VARCHAR(100) NOT NULL
);

-- Таблица предметов
CREATE TABLE subjects (
    id VARCHAR(36) PRIMARY KEY,
    name VARCHAR(100) NOT NULL
);

-- Связующая таблица групп и предметов
CREATE TABLE group_subjects (
    group_id VARCHAR(20) REFERENCES groups(id) ON DELETE CASCADE,
    subject_id VARCHAR(36) REFERENCES subjects(id) ON DELETE CASCADE,
    PRIMARY KEY (group_id, subject_id)
);

-- Таблица презентаций
CREATE TABLE presentations (
    id VARCHAR(36) PRIMARY KEY,
    title VARCHAR(255) NOT NULL,
    description TEXT,
    author_id VARCHAR(36) NOT NULL REFERENCES users(id) ON DELETE CASCADE,
    subject_id VARCHAR(36) NOT NULL REFERENCES subjects(id) ON DELETE CASCADE,
    group_id VARCHAR(20) REFERENCES groups(id) ON DELETE SET NULL,
    upload_date DATE NOT NULL,
    last_modified TIMESTAMP NOT NULL,
    file_name VARCHAR(255) NOT NULL,
    file_type VARCHAR(50) DEFAULT 'presentation',
    rating NUMERIC(3,1) DEFAULT 0,
    downloads INTEGER DEFAULT 0
);

-- Таблица комментариев
CREATE TABLE comments (
    id VARCHAR(36) PRIMARY KEY,
    presentation_id VARCHAR(36) NOT NULL REFERENCES presentations(id) ON DELETE CASCADE,
    user_id VARCHAR(36) NOT NULL REFERENCES users(id) ON DELETE CASCADE,
    text TEXT NOT NULL,
    date DATE NOT NULL
);

-- Таблица дополнительных материалов
CREATE TABLE supplements (
    id VARCHAR(36) PRIMARY KEY,
    presentation_id VARCHAR(36) NOT NULL REFERENCES presentations(id) ON DELETE CASCADE,
    author_id VARCHAR(36) NOT NULL REFERENCES users(id) ON DELETE CASCADE,
    url TEXT NOT NULL,
    date DATE NOT NULL,
    description TEXT
);
