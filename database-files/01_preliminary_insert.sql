Use Consensus_DB;

INSERT INTO Users(UserID, Name, PoliticalParty, Bio)
        VALUES
        (1, "Prince Maximilian William-Lancelot Robertson III", "People's Party of Europe", "I'm British."),
        (2, "JT Nance", "Democrat Party", "I did NOT kill the pope"),
        (3, "Emeka Okonkwo", "Green Party", "Hello! I love the economy.");

INSERT INTO Roles(RoleType)
        VALUES
        ("Voter"),
        ("Politician"),
        ("Economist");

INSERT INTO RolesUsers(RoleID, UserID)
        VALUES
        (1, 1),
        (2, 2),
        (3, 3);

-- THE MOCK DATA WE HAVE IS FROM CHATGPT
-- WE ARE GOING TO MOCKAROO DATA AFTER THIS DELIVERABLE

INSERT INTO Graphs (
    XAxis, XMin, XMax, XStep,
    Population, GDP_per_capita, Trade_union_density, Unemployment_rate,
    Health, Education, Housing, Community_development,
    Real_interest_rates, Productivity, Corporate_tax_rate, Inflation, Personal_property_tax,
    IRLT,
    Region_East_Asia_and_Pacific,
    Region_Europe_and_Central_Asia,
    Region_Latin_America_and_Caribbean,
    Region_Middle_East_and_North_Africa
)
VALUES
    ('GDP_per_capita', 0, 100000, 1000,
     0, 0, 0, 0,
     0, 0, 0, 0,
     0, 0, 0, 0, 0,
     0,
     0, 0, 0, 0),
     
    ('Unemployment_rate', 0, 50, 1,
     0, 0, 0, 0,
     0, 0, 0, 0,
     0, 0, 0, 0, 0,
     0,
     0, 0, 0, 0),
     
    ('Inflation', 0, 20, 0.5,
     0, 0, 0, 0,
     0, 0, 0, 0,
     0, 0, 0, 0, 0,
     0,
     0, 0, 0, 0);


INSERT INTO Posts (Title, Description, UserID, GraphID, NumUpvotes, NumDownvotes)
VALUES
    ('Post 1 Title', 'This is the description of Post 1.', 1, 1, 3, 1),
    ('Post 2 Title', 'This is the description of Post 2.', 2, 2, 2, 2),
    ('Post 3 Title', 'This is the description of Post 3.', 3, 3, 1, 2),
    ('Post 4 Title', 'Exploring new policies in healthcare.', 1, 2, 1, 1),
    ('Post 5 Title', 'Debate on climate change strategies.', 2, 3, 2, 1),
    ('Post 6 Title', 'Economic impacts of tax reform.', 3, 1, 3, 1),
    ('Post 7 Title', 'Education reforms for the next decade.', 1, 3, 1, 2),
    ('Post 8 Title', 'Housing market trends and predictions.', 2, 1, 1, 3),
    ('Post 9 Title', 'Community engagement and public safety.', 3, 2, 2, 1);


INSERT INTO UpvotesUsers (UserID, PostID)
VALUES
    (1, 1),
    (2, 1),
    (3, 1),  -- Post 1 → 3 upvotes

    (1, 2),
    (3, 2),  -- Post 2 → 2 upvotes

    (2, 3),  -- Post 3 → 1 upvote

    (1, 4),  -- Post 4 → 1 upvote

    (2, 5), (3, 5),  -- Post 5 → 2 upvotes

    (1, 6), (2, 6), (3, 6),  -- Post 6 → 3 upvotes

    (1, 7),  -- Post 7 → 1 upvote

    (3, 8),  -- Post 8 → 1 upvote

    (1, 9), (2, 9);  -- Post 9 → 2 upvotes

INSERT INTO DownvotesUsers (UserID, PostID)
VALUES
    (2, 1),  -- Post 1 → 1 downvote

    (1, 2), (3, 2),  -- Post 2 → 2 downvotes

    (1, 3), (2, 3),  -- Post 3 → 2 downvotes

    (3, 4),  -- Post 4 → 1 downvote

    (2, 5),  -- Post 5 → 1 downvote

    (1, 6),  -- Post 6 → 1 downvote

    (2, 7), (3, 7),  -- Post 7 → 2 downvotes

    (1, 8), (2, 8), (3, 8),  -- Post 8 → 3 downvotes

    (3, 9);  -- Post 9 → 1 downvote


INSERT INTO BookmarkedUsers (UserID, PostID)
VALUES
    (1, 1),  -- Prince bookmarked Post 1
    (1, 4),  -- Prince bookmarked Post 4
    (1, 6),  -- Prince bookmarked Post 6

    (2, 2),  -- JT bookmarked Post 2
    (2, 5),  -- JT bookmarked Post 5
    (2, 9),  -- JT bookmarked Post 9

    (3, 3),  -- Emeka bookmarked Post 3
    (3, 7),  -- Emeka bookmarked Post 7
    (3, 8);  -- Emeka bookmarked Post 8
