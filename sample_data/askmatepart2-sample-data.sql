--
-- PostgreSQL database dump
--

-- Dumped from database version 9.5.6
-- Dumped by pg_dump version 9.5.6

ALTER TABLE IF EXISTS ONLY public.question DROP CONSTRAINT IF EXISTS pk_question_id CASCADE;
ALTER TABLE IF EXISTS ONLY public.answer DROP CONSTRAINT IF EXISTS pk_answer_id CASCADE;
ALTER TABLE IF EXISTS ONLY public.answer DROP CONSTRAINT IF EXISTS fk_question_id CASCADE;
ALTER TABLE IF EXISTS ONLY public.comment DROP CONSTRAINT IF EXISTS pk_comment_id CASCADE;
ALTER TABLE IF EXISTS ONLY public.comment DROP CONSTRAINT IF EXISTS fk_question_id CASCADE;
ALTER TABLE IF EXISTS ONLY public.comment DROP CONSTRAINT IF EXISTS fk_answer_id CASCADE;
ALTER TABLE IF EXISTS ONLY public.question_tag DROP CONSTRAINT IF EXISTS pk_question_tag_id CASCADE;
ALTER TABLE IF EXISTS ONLY public.question_tag DROP CONSTRAINT IF EXISTS fk_question_id CASCADE;
ALTER TABLE IF EXISTS ONLY public.tag DROP CONSTRAINT IF EXISTS pk_tag_id CASCADE;
ALTER TABLE IF EXISTS ONLY public.question_tag DROP CONSTRAINT IF EXISTS fk_tag_id CASCADE;

DROP TABLE IF EXISTS public.question;
CREATE TABLE question (
    id serial NOT NULL,
    submission_time timestamp without time zone,
    view_number integer,
    vote_number integer,
    title text,
    message text,
    image text NOT NULL DEFAULT ''
);

DROP TABLE IF EXISTS public.answer;
CREATE TABLE answer (
    id serial NOT NULL,
    submission_time timestamp without time zone,
    vote_number integer,
    question_id integer,
    message text,
    image text NOT NULL DEFAULT ''
);

DROP TABLE IF EXISTS public.comment;
CREATE TABLE comment (
    id serial NOT NULL,
    question_id integer,
    answer_id integer,
    message text,
    submission_time timestamp without time zone,
    edited_number integer NOT NULL
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


ALTER TABLE ONLY answer
    ADD CONSTRAINT pk_answer_id PRIMARY KEY (id);

ALTER TABLE ONLY comment
    ADD CONSTRAINT pk_comment_id PRIMARY KEY (id);

ALTER TABLE ONLY question
    ADD CONSTRAINT pk_question_id PRIMARY KEY (id);

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

INSERT INTO question VALUES (0, '2017-04-28 08:29:00', 29, 7, 'How to make lists in Python?', 'I am totally new to this, any hints?', '');
INSERT INTO question VALUES (1, '2017-05-15 09:19:00', 15, 9, 'Wordpress loading multiple jQuery Versions', 'I like my pepper onion, Wordpress is totaly absurd!', '');
INSERT INTO question VALUES (2, '2017-12-02 10:41:00', 712, 57, 'Drawing canvas with an image picked with Cordova Camera Plugin', 'Wet closure of my pickles, oh no, I need to screw this on again', '');
INSERT INTO question VALUES (3, '2018-03-31 08:29:00', 41, 19, 'How to prepare some onions for my trip?', 'Because I need fly carpet', '');
INSERT INTO question VALUES (4, '2018-01-27 09:19:00', 88, 16, 'I got a problem guys', 'Sometimes I got this', '');
INSERT INTO question VALUES (5, '2018-12-11 10:41:00', 136, 57, 'Vatican lies', 'Pickled oguras in sloikex', '');
SELECT pg_catalog.setval('question_id_seq', 6, true);

INSERT INTO answer VALUES (1, '2017-04-28 16:49:00', 4, 1, 'You need to use baskets.', 15);
INSERT INTO answer VALUES (2, '2017-04-25 14:42:00', 35, 1, 'Prepare Spartans, gone to the ride!', 11);
INSERT INTO answer VALUES (3, '2017-04-28 16:49:00', 4, 2, 'Do you know about ALT + F4 shortcut?', 2);
INSERT INTO answer VALUES (4, '2017-04-25 14:42:00', 35, 2, 'Drop the water drop', 4);
INSERT INTO answer VALUES (5, '2017-04-28 16:49:00', 4, 3, 'Blanket is wet, oyoy', 1);
INSERT INTO answer VALUES (6, '2017-04-25 14:42:00', 35, 4, 'Doctor pepper have some issue', 0);
SELECT pg_catalog.setval('answer_id_seq', 6, true);

INSERT INTO comment VALUES (1, 0, NULL, 'Totally worth it!', '2017-05-01 05:49:00');
INSERT INTO comment VALUES (2, NULL, 1, 'Mayoneyzing is a sport', '2017-05-02 16:55:00');
INSERT INTO comment VALUES (3, 2, NULL, 'Too bad I am that great and glorious', '2017-05-01 05:49:00');
INSERT INTO comment VALUES (4, NULL, 3, 'Be my valentine.', '2017-05-02 16:55:00');
INSERT INTO comment VALUES (5, 4, NULL, 'Touch the sky, yhym', '2017-05-01 05:49:00');
INSERT INTO comment VALUES (6, NULL, 5, 'I believe I can fly', '2017-05-02 16:55:00');
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
