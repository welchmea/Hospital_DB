-- -- CS340 Portfolio Project deliverables: Data Definition Queries

-- -- Creates the table for Jobs with jobID as PK.
-- CREATE TABLE IF NOT EXISTS Jobs (
--     jobID SERIAL PRIMARY KEY,
--     jobName varchar(100) NOT NULL,
--     description varchar(255)
-- );


-- -- Creates the table for EmploymentTypes with typeName as PK.
-- CREATE TABLE IF NOT EXISTS EmploymentTypes (
--     typeName varchar(20) NOT NULL PRIMARY KEY,
--     hoursAllow int NOT NULL
-- );


-- -- Creates the table for Departments with departmentID as PK.
-- CREATE TABLE IF NOT EXISTS Departments (
--     departmentID SERIAL PRIMARY KEY,
--     depName varchar(30) NOT NULL,
--     description varchar(100)
-- );


-- -- Creates the table for Employees with employeeID as PK; typeName
-- -- and jobID as FK.
-- CREATE TABLE IF NOT EXISTS Employees (
--     employeeID SERIAL PRIMARY KEY,
--     name varchar(50) NOT NULL,
--     email varchar(255),
--     phoneNum varchar(20) NOT NULL,
--     typeName varchar(20) DEFAULT NULL,
--     jobID int DEFAULT NULL,
--     departmentID int DEFAULT NULL,
--     FOREIGN KEY (departmentID)
--     REFERENCES Departments(departmentID)
--     ON UPDATE CASCADE
--     ON DELETE SET NULL,
--     FOREIGN KEY (typeName)
--     REFERENCES EmploymentTypes(typeName)
--     ON UPDATE CASCADE
--     ON DELETE SET NULL,
--     FOREIGN KEY (jobID)
--     REFERENCES Jobs(jobID)
--     ON UPDATE CASCADE
--     ON DELETE SET NULL
-- );


-- -- Creates the table for Schedules with scheduleID as PK; employeeID, 
-- -- departmentID, and typeName as FK.
-- CREATE TABLE IF NOT EXISTS Schedules (
--     scheduleID SERIAL PRIMARY KEY,
--     scheduleType varchar(50) NOT NULL,
--     shift varchar(10) NOT NULL,
--     startTime timestamp NOT NULL,
--     endTime timestamp NOT NULL,
--     employeeID int NOT NULL,
--     typeName varchar(20) default NULL,
--     departmentID int,
--     FOREIGN KEY (employeeID)
--     REFERENCES Employees(employeeID)
--     ON UPDATE CASCADE
--     ON DELETE CASCADE,
--     FOREIGN KEY (typeName)
--     REFERENCES EmploymentTypes(typeName)
--     ON DELETE SET NULL, 
--     FOREIGN KEY (departmentID)
--     REFERENCES Departments(departmentID) 
--     ON UPDATE CASCADE
--     ON DELETE SET NULL
-- );


-- -- Creates an intersection table for Departments and EmploymentTypes.
-- CREATE TABLE IF NOT EXISTS Department_has_EmploymentTypes (
--     empDeptID SERIAL PRIMARY KEY, 
--     departmentID int,
--     typeName varchar(20),
--     FOREIGN KEY (departmentID) REFERENCES Departments(departmentID) 
--     ON UPDATE CASCADE
--     ON DELETE CASCADE,
--     FOREIGN KEY (typeName) REFERENCES EmploymentTypes(typeName)
--     ON UPDATE CASCADE
--     ON DELETE CASCADE
-- );

-- -- Creates an intersection table for Jobs and Departments.
-- CREATE TABLE IF NOT EXISTS Jobs_has_Departments (
--     jobDeptID SERIAL PRIMARY KEY,
--     jobID int,
--     departmentID int,
--     FOREIGN KEY (jobID) REFERENCES Jobs (jobID)
--     ON UPDATE CASCADE
--     ON DELETE CASCADE,
--     FOREIGN KEY (departmentID) REFERENCES Departments (departmentID)
--     ON UPDATE CASCADE
--     ON DELETE CASCADE
-- );


-- -- Inserts sample data for jobID, jobName, and description into
-- -- the Jobs table.
-- INSERT INTO Jobs (jobName, description)
-- VALUES('Cardiologist', 'Physician that specializes in Cardiology'),
-- ('Radiographer', 'Technician that performs X-Rays'),
-- ('Neurologist', 'Physician that specializes in Neurology'),
-- ('General Physician', 'Physician that provides a range of non-surgical health care'),
-- ('Surgeon', 'Medical practitioner qualified to practice surgery');


-- Inserts sample data for name, email, phoneNum, jobID, departmentID, and typeName
-- into the Employees table.
-- INSERT INTO Employees (name, email, phoneNum, jobID, departmentID, typeName)
-- VALUES('John Adams', 'jadams@ghospital.org', '206-555-1212', 1, 3, 'Full Time'),
-- ('George Washington','gwash@ghospital.org','204-556-1234', 4, 2, 'Full Time'),
-- ('Abraham Lincoln','alinc@ghospital.org','123-456-7891', 4, 2, 'Resident'),
-- ('Ronald Reagan','rreagan@ghospital.org','987-654-3210', 5, 1, 'Part Time'),
-- ('Richard Nixon','rnixon@ghospital.org','360-777-1000', 2, 4, 'Part Time');


-- -- Inserts sample data for departmentID, depName, and description
-- -- into the Departments table.
-- INSERT INTO Departments (depName, description)
-- VALUES('General Surgery','Covers a wide range of types of surgery and procedures on patients.'),
-- ('General Internal Medicine','Deals with the prevention, diagnosis, and treatment of internal diseases.'),
-- ('Cardiology','Provides medical care to patients who have problems with their heart or circulation.'),
-- ('Radiology','This is where imaging tests are performed.'),
-- ('Neurology','This unit deals with disorders of the nervous system, including the brain and spinal cord.');


-- -- Inserts sample data for typeName and hoursAllow into the EmploymentTypes
-- -- table.
-- INSERT INTO EmploymentTypes (typeName, hoursAllow)
-- VALUES('Part Time', 30),
-- ('Full Time', 60),
-- ('PRN', 40),
-- ('Resident', 50);


-- Inserts sample data for scheduleID, scheduleType, shift, startTime, endTime,
-- employeeID, departmentID, and typeName into the Schedules table.
INSERT INTO Schedules (scheduleType, shift, startTime, endTime, employeeID, typeName, departmentID)
VALUES('Daily','Morning', '2023-03-03 08:00:00', '2023-03-03 16:00:00', 6, 'Full Time', 3),
('Daily','Evening', '2023-03-03 23:00:00', '2023-03-04 06:00:00', 7,'Full Time', 2),
('Holiday', 'Swing', '2023-04-01 15:00:00', '2023-03-04 23:00:00', 8, 'Resident', 2),
('Daily', 'Evening', '2023-04-02 23:00:00', '2023-04-03 06:00:00', 9, 'Part Time', 1),
('Emergency', 'Morning', '2023-05-01 07:00:00', '2023-05-01 15:00:00', 10,'Part Time', 4);


-- -- Inserts sample data for empDeptID, departmentID, and typeName into the intersection 
-- -- table Department_has_EmploymentTypes.
-- INSERT INTO Department_has_EmploymentTypes (departmentID, typeName)
-- VALUES (1, 'Part Time'),
-- (2, 'Full Time'),
-- (3, 'Full Time'),
-- (4, 'Resident'),
-- (5, 'PRN');

-- -- Inserts sample data for jobDeptID, jobID, and departmentID into the intersection 
-- -- table Jobs_has_Departments.
-- INSERT INTO Jobs_has_Departments (jobID, departmentID)
-- VALUES (4, 2),
-- (4, 2),
-- (1, 3),
-- (5, 1),
-- (2, 4);
