SET sql_mode='NO_AUTO_VALUE_ON_ZERO';

CREATE TABLE player
(
  id   INT AUTO_INCREMENT PRIMARY KEY,
  name VARCHAR(64) NOT NULL
);

CREATE TABLE deck
(
  id     INT AUTO_INCREMENT PRIMARY KEY,
  name   VARCHAR(64) NOT NULL,
  type   INT(1)      NOT NULL,
  status VARCHAR(32) NOT NULL
);

CREATE TABLE tournament
(
  id     INT AUTO_INCREMENT PRIMARY KEY,
  name   VARCHAR(64) NOT NULL,
  status VARCHAR(32) NOT NULL,
  type   INT(1)      NOT NULL
);

CREATE TABLE participant
(
  id            INT AUTO_INCREMENT PRIMARY KEY,
  tournament_id INT NOT NULL,
  player_id     INT NOT NULL,
  deck_id       INT NOT NULL,
  player2_id    INT NULL,
  deck2_id      INT NULL,
  CONSTRAINT uix_players_tournament UNIQUE (player_id, player2_id, tournament_id),
  CONSTRAINT uix_decks_tournament UNIQUE (deck_id, deck2_id, tournament_id),
  CONSTRAINT participant_ibfk_1 FOREIGN KEY (tournament_id) REFERENCES tournament (id),
  CONSTRAINT participant_ibfk_2 FOREIGN KEY (player_id) REFERENCES player (id),
  CONSTRAINT participant_ibfk_3 FOREIGN KEY (deck_id) REFERENCES deck (id),
  CONSTRAINT participant_ibfk_4 FOREIGN KEY (player2_id) REFERENCES player (id),
  CONSTRAINT participant_ibfk_5 FOREIGN KEY (deck2_id) REFERENCES deck (id)
);

CREATE INDEX tournament_id ON participant (tournament_id);
CREATE INDEX player_id ON participant (player_id);
CREATE INDEX deck_id ON participant (deck_id);
CREATE INDEX deck2_id ON participant (deck2_id);
CREATE INDEX player2_id ON participant (player2_id);

CREATE TABLE game
(
  id            INT AUTO_INCREMENT PRIMARY KEY,
  tournament_id INT    NOT NULL,
  round         INT(2) NOT NULL,
  p1_id         INT    NOT NULL,
  p2_id         INT    NOT NULL,
  p1_wins       INT(1) NOT NULL DEFAULT 0,
  p2_wins       INT(1) NOT NULL DEFAULT 0,
  CONSTRAINT uix_trp1 UNIQUE (tournament_id, round, p1_id),
  CONSTRAINT uix_trp2 UNIQUE (tournament_id, round, p2_id),
  CONSTRAINT game_ibfk_1 FOREIGN KEY (tournament_id) REFERENCES tournament (id),
  CONSTRAINT game_ibfk_2 FOREIGN KEY (p1_id) REFERENCES participant (id),
  CONSTRAINT game_ibfk_3 FOREIGN KEY (p2_id) REFERENCES participant (id)
);

CREATE INDEX p1_id ON game (p1_id);
CREATE INDEX p2_id ON game (p2_id);


/* ----------------------- data ----------------------- */

INSERT INTO player (id, name) VALUES
  (1, 'Jhonatan'),
  (2, 'Maurício'),
  (3, 'Sérgio'),
  (4, 'Alexandre'),
  (5, 'Anderson'),
  (6, 'Israel'),
  (7, 'Daniel');


INSERT INTO deck (id, name, type, status) VALUES
  (0, 'Sem informação', 2, 'active'),
  (1, 'Mono White Espadas', 1, 'active'),
  (2, 'Mono Black Vampiros', 1, 'active'),
  (3, 'Mono Blue Milling', 1, 'active'),
  (4, 'Dimir', 1, 'active'),
  (5, 'Golgari', 1, 'active'),
  (6, 'Boros', 1, 'active'),
  (7, 'Mono Red Goblins', 1, 'active'),
  (8, 'Mono Black Zombies', 1, 'active'),
  (9, 'Mono Red LandDestroyer', 1, 'active'),
  (10, 'GR Lobisomens', 1, 'active'),
  (11, 'BW Vampiros', 1, 'active'),
  (12, 'BU Descarte', 1, 'active'),
  (13, 'WB Cura', 1, 'inactive'),
  (14, 'WRG Aliados', 1, 'active'),
  (15, 'RUW Spells', 1, 'active'),
  (16, 'GB Elfos', 1, 'active'),
  (17, 'GB Sacrifício', 1, 'active');


-- tournament 1
INSERT INTO tournament (id, name, status, type) VALUES (1, '1° DGT Magic Tournament', 'finished', 1);
INSERT INTO participant (id, tournament_id, player_id, deck_id) VALUES
  (1, 1, 1, 16), -- Jhonatan
  (2, 1, 4, 17), -- Alexandre
  (3, 1, 5, 11), -- Anderson
  (4, 1, 2, 14), -- Maurício
  (5, 1, 3, 12), -- Sérgio
  (6, 1, 6, 13); -- Israel

-- rounds
INSERT into game(tournament_id, round, p1_id, p2_id, p1_wins, p2_wins) VALUES
  -- round 1
  (1, 1, 2, 6, 2, 0),
  (1, 1, 1, 3, 2, 1),
  (1, 1, 4, 5, 2, 0),
  -- round 2
  (1, 2, 5, 3, 1, 2),
  (1, 2, 4, 6, 2, 0),
  (1, 2, 2, 1, 0, 2),
  -- round 3
  (1, 3, 2, 3, 1, 2),
  (1, 3, 6, 5, 2, 0),
  (1, 3, 1, 4, 0, 2),
  -- round 4
  (1, 4, 6, 3, 0, 1),
  (1, 4, 1, 5, 1, 2),
  (1, 4, 4, 2, 2, 0);



-- tournament 2
INSERT INTO tournament (id, name, status, type) VALUES (2, '2° DGT Magic Tournament', 'finished', 1);
INSERT INTO participant (id, tournament_id, player_id, deck_id) VALUES
  (7, 2, 1, 17), -- Jhonatan
  (8, 2, 4, 3),  -- Alexandre
  (9, 2, 5, 6),  -- Anderson
  (10, 2, 2, 8), -- Maurício
  (11, 2, 3, 2), -- Sérgio
  (12, 2, 6, 15);-- Israel

-- rounds
INSERT into game(tournament_id, round, p1_id, p2_id, p1_wins, p2_wins) VALUES
  -- round 1
  (2, 1, 7, 12, 0, 2),
  (2, 1, 8, 10, 0, 2),
  (2, 1, 9, 11, 0, 2),
  -- round 2
  (2, 2, 7, 10, 0, 2),
  (2, 2, 8, 9, 2, 1),
  (2, 2, 12, 11, 1, 2),
  -- round 3
  (2, 3, 7, 9, 2, 0),
  (2, 3, 12, 10, 2, 0),
  (2, 3, 8, 11, 1, 2),
  -- round 4
  (2, 4, 7, 11, 2, 1),
  (2, 4, 9, 10, 0, 2),
  (2, 4, 12, 8, 2, 0),
  -- round 5
  (2, 5, 7, 8, 2, 0),
  (2, 5, 9, 12, 0, 2),
  (2, 5, 11, 10, 2, 0);

-- tournament 3
INSERT INTO tournament (id, name, status, type) VALUES (3, '3° DGT Magic Tournament', 'finished', 1);
INSERT INTO participant (id, tournament_id, player_id, deck_id) VALUES
  (13, 3, 1, 8),  -- Jhonatan
  (14, 3, 4, 10), -- Alexandre
  (15, 3, 2, 4),  -- Maurício
  (16, 3, 3, 16), -- Sérgio
  (17, 3, 7, 3);  -- Daniel

-- rounds
INSERT into game(tournament_id, round, p1_id, p2_id, p1_wins, p2_wins) VALUES
  -- round 1
  (3, 1, 15, 17, 2, 1),
  (3, 1, 16, 14, 2, 1),
  -- round 2
  (3, 2, 17, 16, 2, 1),--
  (3, 2, 13, 15, 2, 0),
  -- round 3
  (3, 3, 16, 13, 2, 1),
  (3, 3, 14, 17, 2, 0),
  -- round 4
  (3, 4, 13, 14, 2, 0),
  (3, 4, 15, 16, 0, 2),
  -- round 5
  (3, 5, 14, 15, 1, 2),
  (3, 5, 17, 13, 0, 2);



-- tournament 4
INSERT INTO tournament (id, name, status, type) VALUES (4, '4° DGT Magic Tournament', 'finished', 1);
INSERT INTO participant (id, tournament_id, player_id, deck_id) VALUES
  (18, 4, 1, 4),  -- Jhonatan
  (19, 4, 4, 11), -- Alexandre
  (20, 4, 2, 17),  -- Maurício
  (21, 4, 3, 10), -- Sérgio
  (22, 4, 7, 5);  -- Daniel

-- rounds
INSERT into game(tournament_id, round, p1_id, p2_id, p1_wins, p2_wins) VALUES
  -- round 1
  (4, 1, 21, 22, 2, 0),
  (4, 1, 20, 19, 0, 2),
  -- round 2
  (4, 2, 22, 20, 0, 2),
  (4, 2, 18, 21, 2, 0),
  -- round 3
  (4, 3, 20, 18, 2, 0),
  (4, 3, 19, 22, 2, 0),
  -- round 4
  (4, 4, 18, 19, 2, 1),
  (4, 4, 21, 20, 0, 2),
  -- round 5
  (4, 5, 19, 21, 1, 2),
  (4, 5, 22, 18, 2, 0);


-- tournament 5
INSERT INTO tournament (id, name, status, type) VALUES (5, '1° Two Headed Giants', 'active', 2);
INSERT INTO participant (id, tournament_id, player_id, deck_id, player2_id, deck2_id) VALUES (23, 5, 4, 6, 1, 12);
INSERT INTO participant (id, tournament_id, player_id, deck_id, player2_id, deck2_id) VALUES (24, 5, 4, 6, 2, 5);
INSERT INTO participant (id, tournament_id, player_id, deck_id, player2_id, deck2_id) VALUES (25, 5, 4, 6, 3, 2);
INSERT INTO participant (id, tournament_id, player_id, deck_id, player2_id, deck2_id) VALUES (26, 5, 1, 12, 2, 5);
INSERT INTO participant (id, tournament_id, player_id, deck_id, player2_id, deck2_id) VALUES (27, 5, 1, 12, 3, 2);
INSERT INTO participant (id, tournament_id, player_id, deck_id, player2_id, deck2_id) VALUES (28, 5, 2, 5, 3, 2);

INSERT INTO game (id, tournament_id, round, p1_id, p2_id, p1_wins, p2_wins) VALUES (48, 5, 1, 23, 28, 0, 0);
INSERT INTO game (id, tournament_id, round, p1_id, p2_id, p1_wins, p2_wins) VALUES (49, 5, 2, 24, 27, 0, 0);
INSERT INTO game (id, tournament_id, round, p1_id, p2_id, p1_wins, p2_wins) VALUES (50, 5, 3, 25, 26, 1, 2);