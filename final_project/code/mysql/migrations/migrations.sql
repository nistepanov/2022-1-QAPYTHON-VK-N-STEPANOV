CREATE
USER if not exists 'test_qa'@'%' IDENTIFIED BY 'qa_test';
GRANT ALL PRIVILEGES ON *.* TO
'test_qa'@'%';
FLUSH
PRIVILEGES;
CREATE
database if not exists vkeducation;
USE
vkeducation;
CREATE TABLE if not exists `test_users`
(
    `id`
    int
    NOT
    NULL
    AUTO_INCREMENT,
    `name`
    varchar
(
    255
) NOT NULL,
    `surname` varchar
(
    255
) NOT NULL,
    `middle_name` varchar
(
    255
) DEFAULT NULL,
    `username` varchar
(
    16
) DEFAULT NULL,
    `password` varchar
(
    255
) NOT NULL,
    `email` varchar
(
    64
) NOT NULL,
    `access` smallint DEFAULT NULL,
    `active` smallint DEFAULT NULL,
    `start_active_time` datetime DEFAULT NULL,
    PRIMARY KEY
(
    `id`
),
    UNIQUE KEY `email`
(
    `email`
),
    UNIQUE KEY `ix_test_users_username`
(
    `username`
)
    );
INSERT INTO test_users (name, surname, username, password, email, access)
VALUES ('nikita', 'stepanov', 'nikita', 'test', 'nik-stepanov-2001@bk.ru', 1);
INSERT INTO test_users (name, surname, username, password, email, access)
VALUES ('block', 'block', 'block', 'block', 'block@mail.ru', 0);

