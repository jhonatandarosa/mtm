/* ----------------------- data ----------------------- */

INSERT INTO player (id, name, nickname) VALUES
  (1, 'Jhonatan', NULL ),
  (2, 'Maurício', 'Dentz'),
  (3, 'Sérgio', 'Serjeta'),
  (4, 'Alexandre', 'Xandovisk'),
  (5, 'Anderson', 'Dentes de Sabre'),
  (6, 'Israel', 'Peter'),
  (7, 'Daniel', NULL),
  (8, 'Witor', NULL),
  (9, 'Heitor', 'Velheta')
;


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
  (27, 'Mono Black Demônios', 'active'),
  (28, 'GR Shaman Landfall', 'active'),
  (29, 'Green Devotion', 'active'),
  (30, 'WU Enchantment Milling', 'active'),
  (31, 'Ilusões', 'active'),
  (32, 'WR Guilty Conscience', 'active')
;


-- tournament 1
INSERT INTO tournament (id, name, status, type) VALUES (1, '1º DGT Magic Tournament', 'finished', 1);
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
INSERT INTO tournament (id, name, status, type) VALUES (2, '2º DGT Magic Tournament', 'finished', 1);
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
INSERT INTO tournament (id, name, status, type) VALUES (3, '3º DGT Magic Tournament', 'finished', 1);
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
INSERT INTO tournament (id, name, status, type) VALUES (4, '4º DGT Magic Tournament', 'finished', 1);
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
INSERT INTO tournament (id, name, status, type) VALUES (5, '1º Two Headed Giants', 'finished', 2);
INSERT INTO participant (id, tournament_id, player_id, deck_id, player2_id, deck2_id) VALUES (23, 5, 4, 6, 1, 12);
INSERT INTO participant (id, tournament_id, player_id, deck_id, player2_id, deck2_id) VALUES (24, 5, 4, 6, 2, 5);
INSERT INTO participant (id, tournament_id, player_id, deck_id, player2_id, deck2_id) VALUES (25, 5, 4, 6, 3, 2);
INSERT INTO participant (id, tournament_id, player_id, deck_id, player2_id, deck2_id) VALUES (26, 5, 1, 12, 2, 5);
INSERT INTO participant (id, tournament_id, player_id, deck_id, player2_id, deck2_id) VALUES (27, 5, 1, 12, 3, 2);
INSERT INTO participant (id, tournament_id, player_id, deck_id, player2_id, deck2_id) VALUES (28, 5, 2, 5, 3, 2);

INSERT INTO game (id, tournament_id, round, p1_id, p2_id, p1_wins, p2_wins) VALUES (48, 5, 1, 23, 28, 2, 0);
INSERT INTO game (id, tournament_id, round, p1_id, p2_id, p1_wins, p2_wins) VALUES (49, 5, 2, 24, 27, 0, 2);
INSERT INTO game (id, tournament_id, round, p1_id, p2_id, p1_wins, p2_wins) VALUES (50, 5, 3, 25, 26, 1, 2);

-- tournament 6
INSERT INTO tournament (id, name, status, type) VALUES (6, '1º Draftzinho', 'finished', 3);
INSERT INTO participant (id, tournament_id, player_id) VALUES (29, 6, 1);
INSERT INTO participant (id, tournament_id, player_id) VALUES (30, 6, 2);
INSERT INTO participant (id, tournament_id, player_id) VALUES (31, 6, 3);
INSERT INTO participant (id, tournament_id, player_id) VALUES (32, 6, 4);

INSERT INTO game (id, tournament_id, round, p1_id, p2_id, p1_wins, p2_wins) VALUES (51, 6, 1, 31, 29, 0, 2);
INSERT INTO game (id, tournament_id, round, p1_id, p2_id, p1_wins, p2_wins) VALUES (52, 6, 1, 30, 32, 0, 2);
INSERT INTO game (id, tournament_id, round, p1_id, p2_id, p1_wins, p2_wins) VALUES (53, 6, 2, 31, 32, 1, 2);
INSERT INTO game (id, tournament_id, round, p1_id, p2_id, p1_wins, p2_wins) VALUES (54, 6, 2, 29, 30, 2, 1);
INSERT INTO game (id, tournament_id, round, p1_id, p2_id, p1_wins, p2_wins) VALUES (55, 6, 3, 31, 30, 2, 0);
INSERT INTO game (id, tournament_id, round, p1_id, p2_id, p1_wins, p2_wins) VALUES (56, 6, 3, 32, 29, 0, 2);

-- tournament 7
INSERT INTO tournament (id, name, status, type) VALUES (7, '2º Draftzinho', 'finished', 3);
INSERT INTO participant (id, tournament_id, player_id) VALUES (33, 7, 4);
INSERT INTO participant (id, tournament_id, player_id) VALUES (34, 7, 3);
INSERT INTO participant (id, tournament_id, player_id) VALUES (35, 7, 1);
INSERT INTO participant (id, tournament_id, player_id) VALUES (36, 7, 2);

INSERT INTO game (id, tournament_id, round, p1_id, p2_id, p1_wins, p2_wins) VALUES (57, 7, 1, 33, 36, 1, 2);
INSERT INTO game (id, tournament_id, round, p1_id, p2_id, p1_wins, p2_wins) VALUES (58, 7, 1, 34, 35, 0, 2);
INSERT INTO game (id, tournament_id, round, p1_id, p2_id, p1_wins, p2_wins) VALUES (59, 7, 2, 33, 35, 2, 0);
INSERT INTO game (id, tournament_id, round, p1_id, p2_id, p1_wins, p2_wins) VALUES (60, 7, 2, 36, 34, 0, 2);
INSERT INTO game (id, tournament_id, round, p1_id, p2_id, p1_wins, p2_wins) VALUES (61, 7, 3, 33, 34, 2, 1);
INSERT INTO game (id, tournament_id, round, p1_id, p2_id, p1_wins, p2_wins) VALUES (62, 7, 3, 35, 36, 2, 1);

-- tournament 8
INSERT INTO tournament (id, name, status, type) VALUES (8, '3º Draftzinho', 'finished', 3);
INSERT INTO participant (id, tournament_id, player_id) VALUES (37, 8, 4);
INSERT INTO participant (id, tournament_id, player_id) VALUES (38, 8, 2);
INSERT INTO participant (id, tournament_id, player_id) VALUES (39,
                                                               8, 3);
INSERT INTO participant (id, tournament_id, player_id) VALUES (40, 8, 1);

INSERT INTO game (id, tournament_id, round, p1_id, p2_id, p1_wins, p2_wins) VALUES (63, 8, 1, 37, 40, 2, 1);
INSERT INTO game (id, tournament_id, round, p1_id, p2_id, p1_wins, p2_wins) VALUES (64, 8, 1, 38, 39, 2, 0);
INSERT INTO game (id, tournament_id, round, p1_id, p2_id, p1_wins, p2_wins) VALUES (65, 8, 2, 37, 39, 2, 0);
INSERT INTO game (id, tournament_id, round, p1_id, p2_id, p1_wins, p2_wins) VALUES (66, 8, 2, 40, 38, 2, 1);
INSERT INTO game (id, tournament_id, round, p1_id, p2_id, p1_wins, p2_wins) VALUES (67, 8, 3, 37, 38, 0, 2);
INSERT INTO game (id, tournament_id, round, p1_id, p2_id, p1_wins, p2_wins) VALUES (68, 8, 3, 39, 40, 1, 2);


-- tournament 9
INSERT INTO tournament (id, name, status, type) VALUES (9, '5º DGT Magic Tournament', 'finished', 1);
INSERT INTO participant (id, tournament_id, player_id, deck_id) VALUES (41, 9, 4, 1);
INSERT INTO participant (id, tournament_id, player_id, deck_id) VALUES (42, 9, 1, 7);
INSERT INTO participant (id, tournament_id, player_id, deck_id) VALUES (43, 9, 2, 9);
INSERT INTO participant (id, tournament_id, player_id, deck_id) VALUES (44, 9, 9, 18);
INSERT INTO participant (id, tournament_id, player_id, deck_id) VALUES (45, 9, 8, 19);
INSERT INTO participant (id, tournament_id, player_id, deck_id) VALUES (46, 9, 3, 20);

INSERT INTO game (id, tournament_id, round, p1_id, p2_id, p1_wins, p2_wins) VALUES (69, 9, 0, 41, 46, 2, 0);
INSERT INTO game (id, tournament_id, round, p1_id, p2_id, p1_wins, p2_wins) VALUES (70, 9, 0, 42, 45, 2, 1);
INSERT INTO game (id, tournament_id, round, p1_id, p2_id, p1_wins, p2_wins) VALUES (71, 9, 0, 43, 44, 1, 1);
INSERT INTO game (id, tournament_id, round, p1_id, p2_id, p1_wins, p2_wins) VALUES (72, 9, 1, 41, 44, 2, 1);
INSERT INTO game (id, tournament_id, round, p1_id, p2_id, p1_wins, p2_wins) VALUES (73, 9, 1, 46, 45, 2, 0);
INSERT INTO game (id, tournament_id, round, p1_id, p2_id, p1_wins, p2_wins) VALUES (74, 9, 1, 42, 43, 0, 2);
INSERT INTO game (id, tournament_id, round, p1_id, p2_id, p1_wins, p2_wins) VALUES (75, 9, 2, 41, 43, 2, 1);
INSERT INTO game (id, tournament_id, round, p1_id, p2_id, p1_wins, p2_wins) VALUES (76, 9, 2, 44, 45, 2, 1);
INSERT INTO game (id, tournament_id, round, p1_id, p2_id, p1_wins, p2_wins) VALUES (77, 9, 2, 46, 42, 2, 1);
INSERT INTO game (id, tournament_id, round, p1_id, p2_id, p1_wins, p2_wins) VALUES (78, 9, 3, 41, 42, 1, 2);
INSERT INTO game (id, tournament_id, round, p1_id, p2_id, p1_wins, p2_wins) VALUES (79, 9, 3, 43, 45, 0, 2);
INSERT INTO game (id, tournament_id, round, p1_id, p2_id, p1_wins, p2_wins) VALUES (80, 9, 3, 44, 46, 0, 2);
INSERT INTO game (id, tournament_id, round, p1_id, p2_id, p1_wins, p2_wins) VALUES (81, 9, 4, 41, 45, 2, 0);
INSERT INTO game (id, tournament_id, round, p1_id, p2_id, p1_wins, p2_wins) VALUES (82, 9, 4, 42, 44, 2, 1);
INSERT INTO game (id, tournament_id, round, p1_id, p2_id, p1_wins, p2_wins) VALUES (83, 9, 4, 43, 46, 0, 2);


-- tournament 10
INSERT INTO tournament (id, name, status, type) VALUES (10, '6º DGT Magic Tournament', 'finished', 1);
INSERT INTO participant (id, tournament_id, player_id, deck_id) VALUES(47, 10, 3, 30);
INSERT INTO participant (id, tournament_id, player_id, deck_id) VALUES(48, 10, 1, 29);
INSERT INTO participant (id, tournament_id, player_id, deck_id) VALUES(49, 10, 4, 25);
INSERT INTO participant (id, tournament_id, player_id, deck_id) VALUES(50, 10, 8, 23);
INSERT INTO participant (id, tournament_id, player_id, deck_id) VALUES(51, 10, 2, 28);
INSERT INTO participant (id, tournament_id, player_id, deck_id) VALUES(52, 10, 9, 24);


INSERT INTO game (id, tournament_id, round, p1_id, p2_id, p1_wins, p2_wins) VALUES (84, 10, 0, 47, 52, 1, 1);
INSERT INTO game (id, tournament_id, round, p1_id, p2_id, p1_wins, p2_wins) VALUES (85, 10, 0, 48, 51, 2, 1);
INSERT INTO game (id, tournament_id, round, p1_id, p2_id, p1_wins, p2_wins) VALUES (86, 10, 0, 49, 50, 2, 1);
INSERT INTO game (id, tournament_id, round, p1_id, p2_id, p1_wins, p2_wins) VALUES (87, 10, 1, 47, 51, 2, 1);
INSERT INTO game (id, tournament_id, round, p1_id, p2_id, p1_wins, p2_wins) VALUES (88, 10, 1, 52, 50, 0, 2);
INSERT INTO game (id, tournament_id, round, p1_id, p2_id, p1_wins, p2_wins) VALUES (89, 10, 1, 48, 49, 2, 0);
INSERT INTO game (id, tournament_id, round, p1_id, p2_id, p1_wins, p2_wins) VALUES (90, 10, 2, 47, 50, 0, 2);
INSERT INTO game (id, tournament_id, round, p1_id, p2_id, p1_wins, p2_wins) VALUES (91, 10, 2, 51, 49, 2, 1);
INSERT INTO game (id, tournament_id, round, p1_id, p2_id, p1_wins, p2_wins) VALUES (92, 10, 2, 52, 48, 0, 2);
INSERT INTO game (id, tournament_id, round, p1_id, p2_id, p1_wins, p2_wins) VALUES (93, 10, 3, 47, 49, 2, 0);
INSERT INTO game (id, tournament_id, round, p1_id, p2_id, p1_wins, p2_wins) VALUES (94, 10, 3, 50, 48, 0, 2);
INSERT INTO game (id, tournament_id, round, p1_id, p2_id, p1_wins, p2_wins) VALUES (95, 10, 3, 51, 52, 2, 0);
INSERT INTO game (id, tournament_id, round, p1_id, p2_id, p1_wins, p2_wins) VALUES (96, 10, 4, 47, 48, 2, 0);
INSERT INTO game (id, tournament_id, round, p1_id, p2_id, p1_wins, p2_wins) VALUES (97, 10, 4, 49, 52, 2, 1);
INSERT INTO game (id, tournament_id, round, p1_id, p2_id, p1_wins, p2_wins) VALUES (98, 10, 4, 50, 51, 1, 2);


-- tournament 11
INSERT INTO tournament (id, name, status, type) VALUES (11, '7º DGT Magic Tournament', 'active', 1);
INSERT INTO participant (id, tournament_id, player_id, deck_id) VALUES(53, 11, 4, 21);
INSERT INTO participant (id, tournament_id, player_id, deck_id) VALUES(54, 11, 3, 22);
INSERT INTO participant (id, tournament_id, player_id, deck_id) VALUES(55, 11, 8, 26);
INSERT INTO participant (id, tournament_id, player_id, deck_id) VALUES(56, 11, 2, 32);
INSERT INTO participant (id, tournament_id, player_id, deck_id) VALUES(57, 11, 1, 27);
INSERT INTO participant (id, tournament_id, player_id, deck_id) VALUES(58, 11, 5, 31);

INSERT INTO game (id, tournament_id, round, p1_id, p2_id, p1_wins, p2_wins) VALUES (99, 11, 0, 53, 58, 0, 0);
INSERT INTO game (id, tournament_id, round, p1_id, p2_id, p1_wins, p2_wins) VALUES (100, 11, 0, 54, 57, 0, 0);
INSERT INTO game (id, tournament_id, round, p1_id, p2_id, p1_wins, p2_wins) VALUES (101, 11, 0, 55, 56, 0, 0);
INSERT INTO game (id, tournament_id, round, p1_id, p2_id, p1_wins, p2_wins) VALUES (102, 11, 1, 53, 57, 0, 0);
INSERT INTO game (id, tournament_id, round, p1_id, p2_id, p1_wins, p2_wins) VALUES (103, 11, 1, 58, 56, 0, 0);
INSERT INTO game (id, tournament_id, round, p1_id, p2_id, p1_wins, p2_wins) VALUES (104, 11, 1, 54, 55, 0, 0);
INSERT INTO game (id, tournament_id, round, p1_id, p2_id, p1_wins, p2_wins) VALUES (105, 11, 2, 53, 56, 0, 0);
INSERT INTO game (id, tournament_id, round, p1_id, p2_id, p1_wins, p2_wins) VALUES (106, 11, 2, 57, 55, 0, 0);
INSERT INTO game (id, tournament_id, round, p1_id, p2_id, p1_wins, p2_wins) VALUES (107, 11, 2, 58, 54, 0, 0);
INSERT INTO game (id, tournament_id, round, p1_id, p2_id, p1_wins, p2_wins) VALUES (108, 11, 3, 53, 55, 0, 0);
INSERT INTO game (id, tournament_id, round, p1_id, p2_id, p1_wins, p2_wins) VALUES (109, 11, 3, 56, 54, 0, 0);
INSERT INTO game (id, tournament_id, round, p1_id, p2_id, p1_wins, p2_wins) VALUES (110, 11, 3, 57, 58, 0, 0);
INSERT INTO game (id, tournament_id, round, p1_id, p2_id, p1_wins, p2_wins) VALUES (111, 11, 4, 53, 54, 0, 0);
INSERT INTO game (id, tournament_id, round, p1_id, p2_id, p1_wins, p2_wins) VALUES (112, 11, 4, 55, 58, 0, 0);
INSERT INTO game (id, tournament_id, round, p1_id, p2_id, p1_wins, p2_wins) VALUES (113, 11, 4, 56, 57, 0, 0);
