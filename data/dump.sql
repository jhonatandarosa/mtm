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
INSERT INTO tournament (id, name) VALUES (1, '1° DGT Magic Tournament');
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



--- tournament 2
INSERT INTO tournament (id, name) VALUES (2, '2° DGT Magic Tournament');
INSERT INTO participant (id, tournament_id, player_id, deck_id) VALUES
  (7, 2, 1, 17),--Jhonatan
  (8, 2, 4, 3),--Alexandre
  (9, 2, 5, 6),--Anderson
  (10, 2, 2, 8),--Maurício
  (11, 2, 3, 2),--Sérgio
  (12, 2, 6, 15);--Israel

--rounds
INSERT into game(tournament_id, round, p1_id, p2_id, p1_wins, p2_wins) VALUES
  -- round 1
  (2, 1, 7, 12, 0, 2),
  (2, 1, 8, 10, 0, 2),
  (2, 1, 9, 11, 0, 2),
  -- round 2
  (2, 2, 7, 10, 0, 2),
  (2, 2, 8, 9, 2, 1),
  (2, 2, 12, 11, 2, 1),
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