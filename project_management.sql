DROP SCHEMA IF EXISTS project_management;

CREATE SCHEMA IF NOT EXISTS project_management
    AUTHORIZATION postgres;

CREATE TABLE project_management.accounts_profile
(
    id         SERIAL PRIMARY KEY,
    user_id    INTEGER UNIQUE NOT NULL
        REFERENCES project_management.auth_user (id) ON DELETE CASCADE,
    phone      VARCHAR(15),
    role       VARCHAR(20) CHECK (role IN ('admin', 'manager', 'member')),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE project_management.project_status
(
    id   SERIAL PRIMARY KEY,
    code VARCHAR(30) UNIQUE NOT NULL,
    name VARCHAR(50)        NOT NULL
);

INSERT INTO project_management.project_status (code, name)
VALUES ('active', 'Active'),
       ('completed', 'Completed'),
       ('archived', 'Archived');


CREATE TABLE project_management.task_status
(
    id   SERIAL PRIMARY KEY,
    code VARCHAR(30) UNIQUE NOT NULL,
    name VARCHAR(50)        NOT NULL
);

INSERT INTO project_management.task_status (code, name)
VALUES ('todo', 'To Do'),
       ('in_progress', 'In Progress'),
       ('done', 'Done');

CREATE TABLE project_management.task_priority
(
    id   SERIAL PRIMARY KEY,
    code VARCHAR(20) UNIQUE NOT NULL,
    name VARCHAR(50)        NOT NULL
);

INSERT INTO project_management.task_priority (code, name)
VALUES ('low', 'Low'),
       ('medium', 'Medium'),
       ('high', 'High');


CREATE TABLE project_management.projects
(
    id          SERIAL PRIMARY KEY,
    name        VARCHAR(200) NOT NULL,
    description TEXT,
    created_by  INTEGER      NOT NULL REFERENCES project_management.auth_user (id),
    status_id   INTEGER      NOT NULL REFERENCES project_management.project_status (id),
    created_at  TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE project_management.tasks
(
    id           SERIAL PRIMARY KEY,
    project_id   INTEGER      NOT NULL REFERENCES project_management.projects (id) ON DELETE CASCADE,

    title        VARCHAR(200) NOT NULL,
    description  TEXT,

    assigned_to  INTEGER      NOT NULL REFERENCES project_management.auth_user (id),
    assigned_by  INTEGER      NOT NULL REFERENCES project_management.auth_user (id),

    status_id    INTEGER      NOT NULL REFERENCES project_management.task_status (id),
    priority_id  INTEGER      NOT NULL REFERENCES project_management.task_priority (id),

    assigned_at  TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    due_date     DATE,
    completed_at TIMESTAMP
);


CREATE TABLE project_management.conversations
(
    id         SERIAL PRIMARY KEY,
    user1_id   INTEGER NOT NULL REFERENCES project_management.auth_user (id),
    user2_id   INTEGER NOT NULL REFERENCES project_management.auth_user (id),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    UNIQUE (user1_id, user2_id)
);


CREATE TABLE project_management.messages
(
    id              SERIAL PRIMARY KEY,
    conversation_id INTEGER NOT NULL REFERENCES project_management.conversations (id) ON DELETE CASCADE,
    sender_id       INTEGER NOT NULL REFERENCES project_management.auth_user (id),
    content         TEXT    NOT NULL,
    created_at      TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);