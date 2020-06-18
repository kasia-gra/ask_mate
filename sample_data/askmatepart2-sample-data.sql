--
-- PostgreSQL database dump
--

-- Dumped from database version 9.5.6
-- Dumped by pg_dump version 9.5.6

ALTER TABLE IF EXISTS ONLY public.question DROP CONSTRAINT IF EXISTS pk_question_id CASCADE;
ALTER TABLE IF EXISTS ONLY public.question DROP CONSTRAINT IF EXISTS fk_user_id CASCADE;
ALTER TABLE IF EXISTS ONLY public.answer DROP CONSTRAINT IF EXISTS pk_answer_id CASCADE;
ALTER TABLE IF EXISTS ONLY public.answer DROP CONSTRAINT IF EXISTS fk_question_id CASCADE;
ALTER TABLE IF EXISTS ONLY public.answer DROP CONSTRAINT IF EXISTS fk_user_id CASCADE;
ALTER TABLE IF EXISTS ONLY public.comment DROP CONSTRAINT IF EXISTS pk_comment_id CASCADE;
ALTER TABLE IF EXISTS ONLY public.comment DROP CONSTRAINT IF EXISTS fk_question_id CASCADE;
ALTER TABLE IF EXISTS ONLY public.comment DROP CONSTRAINT IF EXISTS fk_answer_id CASCADE;
ALTER TABLE IF EXISTS ONLY public.comment DROP CONSTRAINT IF EXISTS fk_user_id CASCADE;
ALTER TABLE IF EXISTS ONLY public.question_tag DROP CONSTRAINT IF EXISTS pk_question_tag_id CASCADE;
ALTER TABLE IF EXISTS ONLY public.question_tag DROP CONSTRAINT IF EXISTS fk_question_id CASCADE;
ALTER TABLE IF EXISTS ONLY public.tag DROP CONSTRAINT IF EXISTS pk_tag_id CASCADE;
ALTER TABLE IF EXISTS ONLY public.question_tag DROP CONSTRAINT IF EXISTS fk_tag_id CASCADE;
ALTER TABLE IF EXISTS ONLY public.users DROP CONSTRAINT IF EXISTS pk_user_id CASCADE;
ALTER TABLE IF EXISTS ONLY public.roles DROP CONSTRAINT IF EXISTS pk_role_id CASCADE;
ALTER TABLE IF EXISTS ONLY public.roles DROP CONSTRAINT IF EXISTS fk_user_id CASCADE;


DROP TABLE IF EXISTS public.question;
CREATE TABLE question (
    id serial NOT NULL,
    submission_time timestamp without time zone,
    view_number integer,
    vote_number integer,
    title text,
    message text,
    image text NOT NULL DEFAULT '',
    user_id integer
);

DROP TABLE IF EXISTS public.answer;
CREATE TABLE answer (
    id serial NOT NULL,
    submission_time timestamp without time zone,
    vote_number integer,
    question_id integer,
    message text,
    image text NOT NULL DEFAULT '',
    user_id integer,
    accepted boolean
);

DROP TABLE IF EXISTS public.comment;
CREATE TABLE comment (
    id serial NOT NULL,
    question_id integer,
    answer_id integer,
    message text,
    submission_time timestamp without time zone,
    edited_number integer NOT NULL,
    user_id integer
);


DROP TABLE IF EXISTS public.question_tag;
CREATE TABLE question_tag (
    question_id integer NOT NULL,
    tag_id integer NOT NULL
);

DROP TABLE IF EXISTS public.tag;
CREATE TABLE tag (
    id serial NOT NULL,
    name text
);

DROP TABLE IF EXISTS public.votes;
CREATE TABLE votes (
    id serial NOT NULL,
    user_id integer NOT NULL,
    question_id integer,
    answer_id integer,
    vote_time timestamp without time zone
);

DROP TABLE IF EXISTS public.users;
CREATE TABLE users (
    id serial NOT NULL,
    email text,
    password text,
    registration_time timestamp without time zone,
    reputation integer
);


DROP TABLE IF EXISTS public.roles;
CREATE TABLE roles (
    id serial NOT NULL,
    user_id integer NOT NULL,
    role text
);


ALTER TABLE ONLY users
    ADD CONSTRAINT pk_user_id PRIMARY KEY (id);

ALTER TABLE ONLY roles
    ADD CONSTRAINT pk_role_id PRIMARY KEY (id);

ALTER TABLE ONLY roles
    ADD CONSTRAINT fk_user_id FOREIGN KEY (user_id) REFERENCES users(id);

ALTER TABLE ONLY answer
    ADD CONSTRAINT pk_answer_id PRIMARY KEY (id);

ALTER TABLE ONLY answer
    ADD CONSTRAINT fk_user_id FOREIGN KEY (user_id) REFERENCES users(id);

ALTER TABLE ONLY comment
    ADD CONSTRAINT pk_comment_id PRIMARY KEY (id);

ALTER TABLE ONLY comment
    ADD CONSTRAINT fk_user_id FOREIGN KEY (user_id) REFERENCES users(id);

ALTER TABLE ONLY question
    ADD CONSTRAINT pk_question_id PRIMARY KEY (id);

ALTER TABLE ONLY question
    ADD CONSTRAINT fk_user_id FOREIGN KEY (user_id) REFERENCES users(id);

ALTER TABLE ONLY question_tag
    ADD CONSTRAINT pk_question_tag_id PRIMARY KEY (question_id, tag_id);

ALTER TABLE ONLY tag
    ADD CONSTRAINT pk_tag_id PRIMARY KEY (id);

ALTER TABLE ONLY comment
    ADD CONSTRAINT fk_answer_id FOREIGN KEY (answer_id) REFERENCES answer(id);

ALTER TABLE ONLY answer
    ADD CONSTRAINT fk_question_id FOREIGN KEY (question_id) REFERENCES question(id);

ALTER TABLE ONLY question_tag
    ADD CONSTRAINT fk_question_id FOREIGN KEY (question_id) REFERENCES question(id);

ALTER TABLE ONLY comment
    ADD CONSTRAINT fk_question_id FOREIGN KEY (question_id) REFERENCES question(id);

ALTER TABLE ONLY question_tag
    ADD CONSTRAINT fk_tag_id FOREIGN KEY (tag_id) REFERENCES tag(id);



INSERT INTO users VALUES (1, 'user@user.com', '$2b$10$YkDZUREQVA5e1XQ2e9ECbeZOTrPlIpJ7VdsO0FIvH/elv6yva/xfm', '2017-04-28 08:29:00', 5);
SELECT pg_catalog.setval('users_id_seq', 1, true);

INSERT INTO roles VALUES (1, 1, 'user');
SELECT pg_catalog.setval('roles_id_seq', 1, true);

INSERT INTO question VALUES (0, '2017-04-28 08:29:00', 29, 7, 'How to make lists in Python?', 'I am totally new to this, any hints?', '', 1);
INSERT INTO question VALUES (1, '2017-05-15 09:19:00', 15, 9, 'Wordpress loading multiple jQuery Versions', 'I like my pepper onion, Wordpress is totaly absurd!', '', 1);
INSERT INTO question VALUES (2, '2017-12-02 10:41:00', 712, 57, 'Drawing canvas with an image picked with Cordova Camera Plugin', 'Wet closure of my pickles, oh no, I need to screw this on again', '', 1);
INSERT INTO question VALUES (3, '2018-03-31 08:29:00', 41, 19, 'How to prepare some onions for my trip?', 'Because I need fly carpet', '', 1);
INSERT INTO question VALUES (4, '2018-01-27 09:19:00', 88, 16, 'I got a problem guys', 'Lorem ipsum dolor sit amet, consectetur adipiscing elit. Quisque accumsan nisi at dolor condimentum mattis. Suspendisse potenti. Proin feugiat magna quis magna sodales, a eleifend tellus pellentesque. Mauris nec nibh porttitor, laoreet mi eu, lobortis turpis. Morbi eleifend, metus sed facilisis congue, odio nibh viverra leo, nec eleifend purus quam ut ipsum. Aenean vel volutpat nisl. Duis luctus purus urna, vitae commodo turpis ullamcorper sed. Integer ac posuere est. Nulla sit amet hendrerit ipsum, quis suscipit est. Duis in metus aliquam, tempus lectus eget, luctus dolor. Pellentesque a tortor et erat consequat ultrices. In hac habitasse platea dictumst. ', '', 1);
INSERT INTO question VALUES (5, '2018-12-11 10:41:00', 136, 57, 'Vatican lies', 'Pickled oguras in sloikex', '', 1);
SELECT pg_catalog.setval('question_id_seq', 6, true);

INSERT INTO answer VALUES (1, '2017-04-28 16:49:00', 4, 1, 'You need to use baskets.', 15, 1, False);
INSERT INTO answer VALUES (2, '2017-04-25 14:42:00', 35, 1, 'Prepare Spartans, gone to the ride!', 11, 1, False);
INSERT INTO answer VALUES (3, '2017-04-28 16:49:00', 4, 2, 'Do you know about ALT + F4 shortcut?', 2, 1, False);
INSERT INTO answer VALUES (4, '2017-04-25 14:42:00', 35, 2, 'Drop the water drop', 4, 1, True);
INSERT INTO answer VALUES (5, '2017-04-28 16:49:00', 4, 3, 'Blanket is wet, oyoy', 1, 1, True);
INSERT INTO answer VALUES (6, '2017-04-25 14:42:00', 35, 4, 'I got umbrella, umbrella, ye, ye, ye, ya, ye, ye i ye', 0, 1, False);
SELECT pg_catalog.setval('answer_id_seq', 6, true);

INSERT INTO comment VALUES (1, 0, NULL, 'Totally worth it!', '2017-05-01 05:49:00', 2, 1);
INSERT INTO comment VALUES (2, NULL, 1, 'Mayoneyzing is a sport', '2017-05-02 16:55:00', 7, 1);
INSERT INTO comment VALUES (3, 2, NULL, 'Too bad I am that great and glorious', '2017-05-01 05:49:00', 1, 1);
INSERT INTO comment VALUES (4, NULL, 3, 'Be my valentine.', '2017-05-02 16:55:00', 3, 1);
INSERT INTO comment VALUES (5, 4, NULL, 'Touch the sky, yhym', '2017-05-01 05:49:00', 0, 1);
INSERT INTO comment VALUES (6, NULL, 5, 'I believe I can fly', '2017-05-02 16:55:00', 5, 1);
SELECT pg_catalog.setval('comment_id_seq', 6, true);

INSERT INTO tag VALUES (1, 'python');
INSERT INTO tag VALUES (2, 'sql');
INSERT INTO tag VALUES (3, 'css');
INSERT INTO tag VALUES (4, 'food');
INSERT INTO tag VALUES (5, 'household');
INSERT INTO tag VALUES (6, 'church');
SELECT pg_catalog.setval('tag_id_seq', 8, true);

INSERT INTO question_tag VALUES (0, 1);
INSERT INTO question_tag VALUES (1, 3);
INSERT INTO question_tag VALUES (2, 5);
INSERT INTO question_tag VALUES (4, 1);
INSERT INTO question_tag VALUES (3, 4);
INSERT INTO question_tag VALUES (5, 5);
INSERT INTO question_tag VALUES (3, 6);
INSERT INTO question_tag VALUES (4, 6);
INSERT INTO question_tag VALUES (5, 6);
