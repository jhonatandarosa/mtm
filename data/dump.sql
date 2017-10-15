/* ----------------------- data ----------------------- */

INSERT INTO player (id, name) VALUES
  (1, 'Jhonatan'),
  (2, 'Maurício'),
  (3, 'Sérgio'),
  (4, 'Alexandre'),
  (5, 'Anderson'),
  (6, 'Israel'),
  (7, 'Daniel');


INSERT INTO deck (id, name, status) VALUES
  (1, 'Mono White Espadas', 'active'),
  (2, 'Mono Black Vampiros', 'active'),
  (3, 'Mono Blue Milling', 'inactive'),
  (4, 'Dimir', 'active'),
  (5, 'Golgari', 'active'),
  (6, 'Boros', 'active'),
  (7, 'Mono Red Goblins', 'active'),
  (8, 'Mono Black Zombies', 'active'),
  (9, 'Mono Red LandDestroyer', 'active'),
  (10, 'GR Lobisomens', 'active'),
  (11, 'BW Vampiros', 'active'),
  (12, 'BU Descarte', 'active'),
  (13, 'WB Cura', 'inactive'),
  (14, 'WRG Aliados', 'active'),
  (15, 'RUW Spells', 'active'),
  (16, 'GB Elfos', 'active'),
  (17, 'GB Sacrifício', 'active'),
  (18, 'Temur', 'active'),
  (19, 'Abzan', 'active'),
  (20, 'Rakdos', 'active'),
  (21, 'Azorius', 'active'),
  (22, 'Simic', 'active'),
  (23, 'Gruul', 'active'),
  (24, 'Orzhov', 'active'),
  (25, 'Mono Black Ratos', 'active'),
  (26, 'Mono Black Sombras', 'active'),
  (27, 'Mono Black Demônios', 'active')
;


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
  (4, 5, 22, 18, 0, 2);


-- tournament 5
INSERT INTO tournament (id, name, status, type) VALUES (5, '1° Two Headed Giants', 'finished', 2);
INSERT INTO participant (id, tournament_id, player_id, deck_id, player2_id, deck2_id) VALUES (23, 5, 4, 6, 1, 12);
INSERT INTO participant (id, tournament_id, player_id, deck_id, player2_id, deck2_id) VALUES (24, 5, 4, 6, 2, 5);
INSERT INTO participant (id, tournament_id, player_id, deck_id, player2_id, deck2_id) VALUES (25, 5, 4, 6, 3, 2);
INSERT INTO participant (id, tournament_id, player_id, deck_id, player2_id, deck2_id) VALUES (26, 5, 1, 12, 2, 5);
INSERT INTO participant (id, tournament_id, player_id, deck_id, player2_id, deck2_id) VALUES (27, 5, 1, 12, 3, 2);
INSERT INTO participant (id, tournament_id, player_id, deck_id, player2_id, deck2_id) VALUES (28, 5, 2, 5, 3, 2);

INSERT INTO game (id, tournament_id, round, p1_id, p2_id, p1_wins, p2_wins) VALUES (48, 5, 1, 23, 28, 2, 0);
INSERT INTO game (id, tournament_id, round, p1_id, p2_id, p1_wins, p2_wins) VALUES (49, 5, 2, 24, 27, 0, 2);
INSERT INTO game (id, tournament_id, round, p1_id, p2_id, p1_wins, p2_wins) VALUES (50, 5, 3, 25, 26, 1, 2);