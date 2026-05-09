CREATE DATABASE DBproject;
USE DBproject;
-- 1) this part is for creating tables
CREATE TABLE Club (
    ClubID CHAR(4) PRIMARY KEY,
    ClubName VARCHAR(100) NOT NULL UNIQUE,
    PresidentName VARCHAR(100) NOT NULL,
    Status VARCHAR(20) DEFAULT 'Active',
    Description VARCHAR(500)
);
-- for this table we added DEFAULT 'Active' since all clubs start active

CREATE TABLE Member (
    StudentID CHAR(5) PRIMARY KEY,
    Name VARCHAR(100) NOT NULL,
    Status VARCHAR(20) NOT NULL,
    Email VARCHAR(100) NOT NULL UNIQUE,
    JoinDate DATE
);
-- the status can bo one of those (active-graduated-left)

CREATE TABLE Account (
    Username VARCHAR(50) PRIMARY KEY,
    StudentID CHAR(5) NOT NULL UNIQUE,
    Password VARCHAR(50) NOT NULL,
    Role VARCHAR(20) NOT NULL,
    FOREIGN KEY (StudentID) REFERENCES Member(StudentID)
);
-- the role can bo one of those (member-president-admin)

CREATE TABLE Event (
    EventID CHAR(4) PRIMARY KEY,
    EventName VARCHAR(150) NOT NULL,
    Date DATE,
    Location VARCHAR(100),
    ClubID CHAR(4),
    Status VARCHAR(20) DEFAULT 'Scheduled',
    FOREIGN KEY (ClubID) REFERENCES Club(ClubID)
);
-- the status can bo one of those (scheduled-done-cancelled), it will always be first considered scheduled 

CREATE TABLE Belong_to (
    StudentID CHAR(5),
    ClubID CHAR(4),
    JoinDate DATE,
    PRIMARY KEY (StudentID, ClubID),
    FOREIGN KEY (StudentID) REFERENCES Member(StudentID),
    FOREIGN KEY (ClubID) REFERENCES Club(ClubID)
);

CREATE TABLE Participate (
    StudentID CHAR(5),
    EventID CHAR(4),
    PRIMARY KEY (StudentID, EventID),
    FOREIGN KEY (StudentID) REFERENCES Member(StudentID),
    FOREIGN KEY (EventID) REFERENCES Event(EventID)
);

-- 2) this part is for inserting info (with many diff cases)

-- inserts for clubs
INSERT INTO Club (ClubID, ClubName, PresidentName, Status, Description) VALUES
('C001', 'Visual Arts Club', 'Ibtihal Fallatah', 'Active', 'Talent development in Drawing, Photography and Graphic Design.'),
('C002', 'Coding Club', 'Rimas Alhazmi', 'Active', 'Focuses on programming, hackathons, and coding projects.'),
('C003', 'TV Shows & Movies Club', 'Reem Aljuwayd', 'Inactive', 'Discuss and review popular TV shows and movies; currently inactive.'),
('C004', 'Drama Club', 'Lama Alawfi', 'Active', 'Focus on theater plays and acting skills.'),
('C005', 'Sports Club', 'Maram Haroon', 'Active', 'Organizes sports activities and tournaments.');

-- inserts for members
INSERT INTO Member (StudentID, Name, Email, Status, JoinDate) VALUES
('S1001', 'Ibtihal Fallatah', 'S1001@uni.edu', 'Active', '2025-01-10'),
('S1002', 'Rimas Alhazmi', 'S1002@uni.edu', 'Active', '2024-09-05'),
('S1003', 'Reem Aljuwayd', 'S1003@uni.edu', 'Active', '2023-08-20'),
('S1004', 'Lama Alawfi', 'S1004@uni.edu', 'Active', '2024-01-15'),
('S1005', 'Maram Haroon', 'S1005@uni.edu', 'Active', '2024-01-20'),
('S1006', 'Ali Mohammed', 'S1006@uni.edu', 'Active', '2025-09-01'),
('S1007', 'Hind Jamal', 'S1007@uni.edu', 'Active', '2024-09-10'),
('S1008', 'Yasser Nasser', 'S1008@uni.edu', 'Active', '2025-01-05'),
('S1013', 'Maha Saud', 'S1013@uni.edu', 'Active', '2025-03-01'),
('S1014', 'Faisal Turki', 'S1014@uni.edu', 'Active', '2025-04-12'),
('S1015', 'Dana Khalid', 'S1015@uni.edu', 'Active', '2025-02-18'),
('S1016', 'Layla Ahmed', 'S1016@uni.edu', 'Active', '2025-01-22'),
('S1017', 'Omar Hassan', 'S1017@uni.edu', 'Active', '2024-10-10'),
('S1009', 'Reem Abdullah', 'S1009@uni.edu', 'Graduated', '2021-09-01'),
('S1010', 'Saud Fahad', 'S1010@uni.edu', 'Graduated', '2020-09-01'),
('S1018', 'Nora Sami', 'S1018@uni.edu', 'Graduated', '2020-01-15'),
('S1011', 'Nawaf Omar', 'S1011@uni.edu', 'Left', '2023-09-05'),
('S1012', 'Dana Ali', 'S1012@uni.edu', 'Left', '2024-01-15'),
('S1019', 'Amal Hamed', 'S1019@uni.edu', 'Left', '2023-05-10'),
('S1020', 'Bandar Adel', 'S1020@uni.edu', 'Left', '2023-06-20'),
('S1021', 'Admin User', 'S1021@uni.edu', 'Active', '2025-01-01');

-- inserts for accounts 
INSERT INTO Account (Username, StudentID, Password, Role) VALUES
('Admin1', 'S1021', 'adminpass', 'Admin'),
('Ibtihal_P', 'S1001', 'pass1', 'President'),
('Rimas_P', 'S1002', 'pass2', 'President'),
('Reem_P', 'S1003', 'pass3', 'President'),
('Lama_P', 'S1004', 'pass4', 'President'),
('Maram_P', 'S1005', 'pass5', 'President'),
('Ali_M', 'S1006', 'pass6', 'Member'),
('Hind_J', 'S1007', 'pass7', 'Member'),
('Yasser_N', 'S1008', 'pass8', 'Member'),
('Reem_A', 'S1009', 'pass9', 'Member'),
('Saud_F', 'S1010', 'pass10', 'Member'),
('Nawaf_O', 'S1011', 'pass11', 'Member'),
('Dana_A', 'S1012', 'pass12', 'Member'),
('Maha_S', 'S1013', 'pass13', 'Member'),
('Faisal_T', 'S1014', 'pass14', 'Member'),
('Dana_K', 'S1015', 'pass15', 'Member'),
('Layla_A', 'S1016', 'pass16', 'Member'),
('Omar_H', 'S1017', 'pass17', 'Member'),
('Nora_S', 'S1018', 'pass18', 'Member'),
('Amal_H', 'S1019', 'pass19', 'Member'),
('Bandar_A', 'S1020', 'pass20', 'Member');

-- inserts for events
INSERT INTO Event (EventID, EventName, Date, Location, ClubID, Status) VALUES
-- visual arts
('E101', 'Annual Arts Exhibition', '2025-12-15', 'Female Campus: C120', 'C001', 'Scheduled'),
('E102', 'Workshop: Oil Painting', '2025-11-20', 'Female Campus: C237', 'C001', 'Done'),
('E103', 'Photography Challenge', '2026-02-14', 'Male Campus: Main Hall', 'C001', 'Cancelled'),
-- coding
('E201', 'Hackathon 2025', '2025-11-28', 'Engineering Lab', 'C002', 'Scheduled'),
('E202', 'Python Workshop', '2025-10-05', 'Computer Lab', 'C002', 'Done'),
('E203', 'AI Seminar', '2026-02-20', 'Lecture Hall', 'C002', 'Cancelled'),
-- tv shows & movies club
('E301', 'Movie Night: Classics', '2024-12-05', 'Media Room', 'C003', 'Done'),    
('E302', 'TV Series Review Session', '2025-01-20', 'Room 101', 'C003', 'Done'),     
('E303', 'Trivia Night: Movie Quiz', '2025-05-10', 'Room 102', 'C003', 'Cancelled'),
-- drama
('E401', 'Drama Play: Hamlet', '2025-12-10', 'Auditorium', 'C004', 'Scheduled'),
('E402', 'Acting Workshop', '2025-10-20', 'Drama Room', 'C004', 'Done'),
-- sports
('E501', 'Inter-College Football', '2025-12-01', 'Sports Field', 'C005', 'Scheduled'),
('E502', 'Basketball Tournament', '2025-11-10', 'Gym Hall', 'C005', 'Done'),
('E503', 'Volleyball Friendly Match', '2025-09-25', 'Gym Hall', 'C005', 'Cancelled');


-- inserts for members in clubs
INSERT INTO Belong_to (StudentID, ClubID, JoinDate) VALUES
('S1001', 'C001', '2025-01-10'),
('S1006', 'C001', '2025-09-01'),
('S1007', 'C001', '2024-09-10'),
('S1002', 'C002', '2024-09-05'),
('S1014', 'C002', '2025-04-12'),
('S1003', 'C003', '2023-08-20'),
('S1009', 'C003', '2021-09-01'),
('S1010', 'C003', '2020-09-01'),
('S1004', 'C004', '2024-01-15'),
('S1015', 'C004', '2025-02-18'),
('S1005', 'C005', '2024-01-20'),
('S1016', 'C005', '2025-01-22');

-- inserts for participating memebrs
INSERT INTO Participate (StudentID, EventID) VALUES
('S1001', 'E101'),
('S1006', 'E101'),
('S1007', 'E102'),
('S1002', 'E201'),
('S1014', 'E202'),
('S1003', 'E301'),
('S1009', 'E302'),
('S1010', 'E303'),
('S1004', 'E401'),
('S1015', 'E402'),
('S1005', 'E501'),
('S1016', 'E502'),
('S1017', 'E503');

-- some testing
SELECT * FROM Club;

SELECT * FROM Member WHERE Status='Active';

SELECT m.Name, a.Username, a.Role FROM Member m
JOIN Account a ON m.StudentID = a.StudentID
WHERE a.Role='President';

SELECT e.EventName, c.ClubName, e.Status FROM Event e
JOIN Club c ON e.ClubID = c.ClubID;

-- queris for the report

-- (basic queries)
SELECT * FROM Club;
SELECT ClubName, Status FROM Club WHERE Status = 'Active';
SELECT ClubName, PresidentName FROM Club ORDER BY ClubName;

SELECT * FROM Member WHERE Status = 'Active';
SELECT Name, Email FROM Member WHERE Status = 'Graduated';
SELECT Name, JoinDate FROM Member
WHERE JoinDate BETWEEN '2024-01-01' AND '2024-12-31';

SELECT Username, Role FROM Account;
SELECT Username FROM Account WHERE Role = 'President';
SELECT Role, COUNT(*) AS NumUsers FROM Account GROUP BY Role;

SELECT * FROM Event;
SELECT EventName, Date FROM Event WHERE Status = 'Scheduled';
SELECT EventName, Location FROM Event WHERE Location LIKE '%Gym%';

SELECT * FROM Belong_to;
SELECT StudentID, ClubID FROM Belong_to WHERE JoinDate > '2024-01-01';
SELECT ClubID, COUNT(*) AS NumMembers
FROM Belong_to
GROUP BY ClubID;

SELECT * FROM Participate;
SELECT StudentID, EventID FROM Participate WHERE EventID = 'E101';
SELECT EventID, COUNT(*) AS NumParticipants
FROM Participate
GROUP BY EventID;

-- (aggregate queries)

-- distribution by status
SELECT Status, COUNT(*) AS NumMembers
FROM Member
GROUP BY Status;

-- earliest and latest join date
SELECT MIN(JoinDate) AS FirstJoinDate,
       MAX(JoinDate) AS LastJoinDate
FROM Member;

-- number of events per club
SELECT ClubID, COUNT(*) AS NumEvents
FROM Event
GROUP BY ClubID;

-- events per status
SELECT Status, COUNT(*) AS NumEvents
FROM Event
GROUP BY Status;

-- (join queries)

-- Members with their usernames and roles (Presidents only)
SELECT m.Name, a.Username, a.Role
FROM Member m
JOIN Account a ON m.StudentID = a.StudentID
WHERE a.Role = 'President';

-- Events with their club names
SELECT e.EventName, c.ClubName, e.Status
FROM Event e
JOIN Club c ON e.ClubID = c.ClubID;

-- Members and the clubs they belong to
SELECT m.Name, c.ClubName, b.JoinDate
FROM Belong_to b
JOIN Member m ON b.StudentID = m.StudentID
JOIN Club c ON b.ClubID = c.ClubID;

-- (views)

-- View of all active members
CREATE OR REPLACE VIEW ActiveMembers AS
SELECT StudentID, Name, Email, JoinDate
FROM Member
WHERE Status = 'Active';

-- View of scheduled events with their club names
CREATE OR REPLACE VIEW ScheduledEventsWithClubs AS
SELECT e.EventName, e.Date, e.Location, c.ClubName
FROM Event e
JOIN Club c ON e.ClubID = c.ClubID
WHERE e.Status = 'Scheduled';

