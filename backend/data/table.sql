-- Создание таблицы пользователей
CREATE TABLE users (
    id VARCHAR(36) PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    email VARCHAR(100) NOT NULL UNIQUE,
    role VARCHAR(20) NOT NULL,
    group_id VARCHAR(20),
    department VARCHAR(100),
    CONSTRAINT chk_role CHECK (role IN ('student', 'teacher'))
);

-- Создание таблицы групп
CREATE TABLE groups (
    id VARCHAR(20) PRIMARY KEY,
    name VARCHAR(100) NOT NULL
);

-- Создание таблицы предметов
CREATE TABLE subjects (
    id VARCHAR(36) PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    teacher_id VARCHAR(36) NOT NULL REFERENCES users(id)
);

-- Создание связующей таблицы групп и предметов
CREATE TABLE group_subjects (
    group_id VARCHAR(20) REFERENCES groups(id),
    subject_id VARCHAR(36) REFERENCES subjects(id),
    PRIMARY KEY (group_id, subject_id)
);

-- Создание таблицы презентаций
CREATE TABLE presentations (
    id VARCHAR(36) PRIMARY KEY,
    title VARCHAR(255) NOT NULL,
    description TEXT,
    author_id VARCHAR(36) NOT NULL REFERENCES users(id),
    subject_id VARCHAR(36) NOT NULL REFERENCES subjects(id),
    group_id VARCHAR(20) REFERENCES groups(id),
    upload_date DATE NOT NULL,
    last_modified TIMESTAMP NOT NULL,
    file_name VARCHAR(255) NOT NULL,
    file_type VARCHAR(50) DEFAULT 'presentation',
    rating NUMERIC(3,1) DEFAULT 0,
    downloads INTEGER DEFAULT 0
);

-- Создание таблицы тегов
CREATE TABLE tags (
    id SERIAL PRIMARY KEY,
    name VARCHAR(50) NOT NULL UNIQUE
);

-- Создание связующей таблицы презентаций и тегов
CREATE TABLE presentation_tags (
    presentation_id VARCHAR(36) REFERENCES presentations(id) ON DELETE CASCADE,
    tag_id INTEGER REFERENCES tags(id) ON DELETE CASCADE,
    PRIMARY KEY (presentation_id, tag_id)
);

-- Создание таблицы комментариев
CREATE TABLE comments (
    id VARCHAR(36) PRIMARY KEY,
    presentation_id VARCHAR(36) NOT NULL REFERENCES presentations(id) ON DELETE CASCADE,
    user_id VARCHAR(36) NOT NULL REFERENCES users(id),
    text TEXT NOT NULL,
    date DATE NOT NULL
);

-- Создание таблицы дополнительных материалов
CREATE TABLE supplements (
    id VARCHAR(36) PRIMARY KEY,
    presentation_id VARCHAR(36) NOT NULL REFERENCES presentations(id) ON DELETE CASCADE,
    author_id VARCHAR(36) NOT NULL REFERENCES users(id),
    url TEXT NOT NULL,
    date DATE NOT NULL,
    description TEXT
);