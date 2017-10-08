CREATE TABLE player
(
  id   SERIAL PRIMARY KEY,
  name VARCHAR(64) NOT NULL
);

CREATE TABLE deck
(
  id     SERIAL PRIMARY KEY,
  name   VARCHAR(64) NOT NULL,
  type   INT         NOT NULL,
  status VARCHAR(32) NOT NULL
);

CREATE TABLE tournament
(
  id     SERIAL PRIMARY KEY,
  name   VARCHAR(64) NOT NULL,
  status VARCHAR(32) NOT NULL,
  type   INT         NOT NULL
);

CREATE TABLE participant
(
  id            SERIAL PRIMARY KEY,
  tournament_id INT NOT NULL,
  player_id     INT NOT NULL,
  deck_id       INT NULL,
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
  id            SERIAL PRIMARY KEY,
  tournament_id INT    NOT NULL,
  round         INT    NOT NULL,
  p1_id         INT    NOT NULL,
  p2_id         INT    NOT NULL,
  p1_wins       INT    NOT NULL DEFAULT 0,
  p2_wins       INT    NOT NULL DEFAULT 0,
  CONSTRAINT uix_trp1 UNIQUE (tournament_id, round, p1_id),
  CONSTRAINT uix_trp2 UNIQUE (tournament_id, round, p2_id),
  CONSTRAINT game_ibfk_1 FOREIGN KEY (tournament_id) REFERENCES tournament (id),
  CONSTRAINT game_ibfk_2 FOREIGN KEY (p1_id) REFERENCES participant (id),
  CONSTRAINT game_ibfk_3 FOREIGN KEY (p2_id) REFERENCES participant (id)
);

CREATE INDEX p1_id ON game (p1_id);
CREATE INDEX p2_id ON game (p2_id);