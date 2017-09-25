INSERT INTO player (id, name) VALUES
  (1, 'Jhonatan'),
  (2, 'Maurício'),
  (3, 'Sérgio'),
  (4, 'Alexandre'),
  (5, 'Anderson'),
  (6, 'Israel'),
  (7, 'Daniel');


INSERT INTO deck (id, name) VALUES
  (1, 'Mono White Espadas'),
  (2, 'Mono Black Vampiros'),
  (3, 'Mono Blue Milling'),
  (4, 'Dimir'),
  (5, 'Golgari'),
  (6, 'Boros'),
  (7, 'Mono Red Goblins'),
  (8, 'Mono Black Zombies'),
  (9, 'Mono Red LandDestroyer'),
  (10, 'GR Lobisomens'),
  (11, 'BW Vampiros'),
  (12, 'BU Descarte'),
  (13, 'WB Cura'),
  (14, 'WRG Aliados'),
  (15, 'RUW Spells'),
  (16, 'GB Elfos'),
  (17, 'GB Sacrifício');


--- tournament 1
INSERT INTO tournament (name) VALUES ('1° DGT Magic Tournament');
INSERT INTO participant (id, tournament_id, player_id, deck_id) VALUES
  (1, 1, 1, 16),--Jhonatan
  (2, 1, 4, 17),--Alexandre
  (3, 1, 5, 11),--Anderson
  (4, 1, 2, 14),--Maurício
  (5, 1, 3, 12),--Sérgio
  (6, 1, 6, 13);--Israel

--rounds
INSERT into game(tournament_id, round, p1_id, p2_id, p1_wins, p2_wins) VALUES
  -- round 1
  (1, 1, 2, 6, 2, 0),
  (1, 1, 1, 3, 2, 1),
  (1, 1, 4, 5, 0, 2),
  -- round 2
  (1, 2, 5, 3, 1, 2),
  (1, 2, 4, 6, 2, 0),
  (1, 2, 2, 1, 0, 2),
  -- round 3
  (1, 3, 2, 3, 1, 2),
  (1, 3, 6, 5, 2, 0),
  (1, 3, 1, 4, 0, 2),
  -- round 4
  (1, 4, 6, 3, 1, 0),
  (1, 4, 1, 5, 1, 2),
  (1, 4, 4, 2, 2, 0);
