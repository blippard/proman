ALTER TABLE IF EXISTS ONLY public.board DROP CONSTRAINT IF EXISTS pk_board_id CASCADE;
ALTER TABLE IF EXISTS ONLY public.board DROP CONSTRAINT IF EXISTS fk_user_id CASCADE;
ALTER TABLE IF EXISTS ONLY public.card DROP CONSTRAINT IF EXISTS pk_card_id CASCADE;
ALTER TABLE IF EXISTS ONLY public.card DROP CONSTRAINT IF EXISTS fk_board_id CASCADE;
ALTER TABLE IF EXISTS ONLY public.card DROP CONSTRAINT IF EXISTS fk_status_id CASCADE;
ALTER TABLE IF EXISTS ONLY public.status DROP CONSTRAINT IF EXISTS pk_status_id CASCADE;
ALTER TABLE IF EXISTS ONLY public.user DROP CONSTRAINT IF EXISTS pk_user_id CASCADE;
ALTER TABLE IF EXISTS ONLY public.board_to_status DROP CONSTRAINT IF EXISTS pk_board_to_status_id CASCADE;


DROP TABLE IF EXISTS public.board;
CREATE TABLE board (
    id SERIAL NOT NULL,
    title VARCHAR,    
    user_id INTEGER DEFAULT 0
);

DROP TABLE IF EXISTS public.card;
CREATE TABLE "card" (
    id SERIAL NOT NULL,
    board_id INTEGER NOT NULL,
    title VARCHAR,
    status_id INTEGER NOT NULL,
    "order" INTEGER
);

DROP TABLE IF EXISTS public.status;
CREATE TABLE "status" (
    id SERIAL NOT NULL,
    title VARCHAR    
);


DROP TABLE IF EXISTS public.user;
-- user is a reserved keyword (it returns the user logged into the DB), so need to escape the tablename
CREATE TABLE "user" (
    id SERIAL NOT NULL,
    username VARCHAR UNIQUE NOT NULL,
    "password" VARCHAR NOT NULL
);

DROP TABLE IF EXISTS public.board_to_status;
CREATE TABLE board_to_status (
    board_id INTEGER NOT NULL,
    status_id INTEGER NOT NULL   
);

INSERT INTO board VALUES (1,'Board 2',0);
INSERT INTO board VALUES (2,'new board',0);
INSERT INTO board VALUES (3,'3rd board',0);
INSERT INTO board VALUES (4,'4th board',0);
INSERT INTO board VALUES (5,'5th board',0);

INSERT INTO "card" VALUES (1,1,'new card 1',0,0);
INSERT INTO "card" VALUES (2,1,'new card 2',0,1);
INSERT INTO "card" VALUES (3,1,'in progress card',1,0);
INSERT INTO "card" VALUES (4,1,'planning',2,0);
INSERT INTO "card" VALUES (5,1,'done card 1',3,0);
INSERT INTO "card" VALUES (6,1,'done card 1',3,1);
INSERT INTO "card" VALUES (7,2,'new card 1',0,0);
INSERT INTO "card" VALUES (8,2,'new card 1',0,1);
INSERT INTO "card" VALUES (9,2,'progress card being tested',2,0);
INSERT INTO "card" VALUES (10,2,'more planning',2,1);
INSERT INTO "card" VALUES (11,2,'done card 1',3,0);
INSERT INTO "card" VALUES (12,2,'done card 2',3,1);
INSERT INTO "card" VALUES (13,1,'dummy 1 text',0,2);
INSERT INTO "card" VALUES (14,1,'',2,1);
INSERT INTO "card" VALUES (15,1,'dummy text beta',2,2);
INSERT INTO "card" VALUES (16,3,'random card',0,0);
INSERT INTO "card" VALUES (17,3,'random card alpha',1,0);
INSERT INTO "card" VALUES (18,3,'random card aleph',1,1);
INSERT INTO "card" VALUES (19,3,'random card 5',2,0);
INSERT INTO "card" VALUES (20,4,'ridiculously long titled card with lots of blah blah blah blah blah blah blah blah blah blah bleeeaaaahhrg',1,0);

INSERT INTO "status" VALUES (0,'new');
INSERT INTO "status" VALUES (1,'in progress');
INSERT INTO "status" VALUES (2,'testing');
INSERT INTO "status" VALUES (3,'done');

INSERT INTO "user" VALUES (0,'','');  -- the public user; empty strings are stored in the DB and are not equivalent to NULL

-- hashed passwords below are the equivalents of those in user.csv
INSERT INTO "user" VALUES (1,'harry','$2b$12$jjguD/Xo.pQDI3t/1UwJQeDnF2cjZzRyzqYOgWXxg.gEq4T5qplBu'); 
INSERT INTO "user" VALUES (2,'hermione','$2b$12$IjXkW021immjAA6dYu.UCOj9x2QqP/8IuzTSbgWg9U8eY8kdMkWwy');
INSERT INTO "user" VALUES (3,'ron','$2b$12$PiYRt9r7oZHrZt67n7zE3ukHG.Q78rN0x4YBI69N4dbSss3hLuTIi');
INSERT INTO "user" VALUES (4,'malfoy','$2b$12$BTNWBy8U0DqxXq/pkN5Ahu41dE6YRwMhyngnK8tIqzG4tm/58igAq');

INSERT INTO board_to_status VALUES (1,0);
INSERT INTO board_to_status VALUES (1,1);
INSERT INTO board_to_status VALUES (1,2);
INSERT INTO board_to_status VALUES (1,3);
INSERT INTO board_to_status VALUES (2,0);
INSERT INTO board_to_status VALUES (2,1);
INSERT INTO board_to_status VALUES (2,2);
INSERT INTO board_to_status VALUES (2,3);
INSERT INTO board_to_status VALUES (3,0);
INSERT INTO board_to_status VALUES (3,1);
INSERT INTO board_to_status VALUES (3,2);
INSERT INTO board_to_status VALUES (3,3);
INSERT INTO board_to_status VALUES (4,0);
INSERT INTO board_to_status VALUES (4,1);
INSERT INTO board_to_status VALUES (4,2);
INSERT INTO board_to_status VALUES (4,3);
INSERT INTO board_to_status VALUES (5,0);
INSERT INTO board_to_status VALUES (5,1);
INSERT INTO board_to_status VALUES (5,2);
INSERT INTO board_to_status VALUES (5,3);


ALTER TABLE ONLY board
    ADD CONSTRAINT pk_board_id PRIMARY KEY (id);

ALTER TABLE ONLY "card"
    ADD CONSTRAINT pk_card_id PRIMARY KEY (id);

ALTER TABLE ONLY "status"
    ADD CONSTRAINT pk_status_id PRIMARY KEY (id);

ALTER TABLE ONLY "user"
    ADD CONSTRAINT pk_user_id PRIMARY KEY (id);

ALTER TABLE ONLY board
    ADD CONSTRAINT fk_user_id FOREIGN KEY (user_id) REFERENCES "user" (id) ON DELETE CASCADE;

ALTER TABLE ONLY "card"
    ADD CONSTRAINT fk_board_id FOREIGN KEY (board_id) REFERENCES board(id) ON DELETE CASCADE;

ALTER TABLE ONLY "card"
    ADD CONSTRAINT fk_status_id FOREIGN KEY (status_id) REFERENCES "status" (id) ON DELETE CASCADE;

ALTER TABLE ONLY board_to_status
    ADD CONSTRAINT pk_board_to_status_id PRIMARY KEY (board_id, status_id);

ALTER TABLE ONLY board_to_status
    ADD CONSTRAINT fk_status_id FOREIGN KEY (status_id) REFERENCES "status" (id) ON DELETE CASCADE;

ALTER TABLE ONLY board_to_status
    ADD CONSTRAINT fk_board_id FOREIGN KEY (board_id) REFERENCES board(id) ON DELETE CASCADE;