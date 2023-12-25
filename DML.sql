 -------------------------------|
 --SELECTS: One for each table--|
 --Fulfills READ----------------| 
 -------------------------------|

 -- Employees--

SELECT Employees.employeeID AS `Employee ID`, Employees.name AS `Employee Name`, \
        Employees.email AS `Employee Email`, Employees.phoneNum AS `Phone Number`, \
        EmploymentTypes.typeName AS `Employment Status`, Jobs.jobName AS `Job Name`, \
        Departments.depName AS `Department Name` FROM Employees \
        LEFT JOIN Jobs ON Employees.jobID = Jobs.jobID  \
        LEFT JOIN Departments ON Employees.departmentID = Departments.departmentID \
        LEFT JOIN EmploymentTypes ON Employees.typeName = EmploymentTypes.typeName;
 
 -- Departments--

SELECT Departments.departmentID AS `Department ID`, \
            Departments.depName AS `Department Name`,\
            Departments.description AS `Description` FROM Departments;
 
 -- Employment Types--

SELECT EmploymentTypes.typeName AS `Type of Employment`,\
            EmploymentTypes.hoursAllow AS `Hours Allowed to Work` FROM EmploymentTypes;
 
 -- Department_has_EmploymentTypes--

SELECT Department_has_EmploymentTypes.empDeptID AS `empDeptID`,\
            EmploymentTypes.typeName AS `Employment Status`, \
            Departments.depName as `Department Name` \
            FROM Department_has_EmploymentTypes \
            LEFT JOIN EmploymentTypes ON EmploymentTypes.typeName = Department_has_EmploymentTypes.typeName \
            LEFT JOIN Departments ON Departments.departmentID = Department_has_EmploymentTypes.departmentID;
 
 -- Jobs--

SELECT Jobs.jobID AS `Job ID`, Jobs.jobName AS `Job Name`, \
            Jobs.description AS `Description` FROM Jobs;
 
 -- Jobs_has_Departments--

SELECT Jobs_has_Departments.jobDeptID AS `Job Department ID Number`, \
            Jobs.jobName AS `Job Name`, Departments.depName AS `Department Name` \
            FROM Jobs_has_Departments \
            LEFT JOIN Jobs ON Jobs.jobID = Jobs_has_Departments.jobID \
            LEFT JOIN Departments ON Departments.departmentID = Jobs_has_Departments.departmentID;
 
 -- Schedules--

SELECT Schedules.scheduleID AS `Schedule ID`, \
            Schedules.scheduleType AS `Schedule Type`, \
            Schedules.shift AS `Shift`, Schedules.startTime AS `Start Time`, \
            Schedules.endTime AS `End Time`, \
            Employees.name AS `Employee Name`, \
            EmploymentTypes.typeName AS `Employment Status`, \
            Departments.depName AS `Department Name` \
            FROM Schedules LEFT JOIN Employees ON \
            Employees.employeeID = Schedules.employeeID \
            LEFT JOIN EmploymentTypes ON \
            EmploymentTypes.typeName = Schedules.typeName \
            LEFT JOIN Departments ON \
            Departments.departmentID = Schedules.departmentID;

 -------------------------------|
 --INSERTS: One for each table--|
 --Fulfills CREATE--------------|
 -------------------------------|

 ---: colon is the special character that represents input variables-| 
 -- that will be computed by the backend and passed to the DB--------|

 -- Employees--

INSERT INTO Employees (name, phoneNum, typeName, jobID, departmentID) \
            VALUES :nameInput, :phoneNumInput,\
                (SELECT typeName FROM EmploymentTypes WHERE typeName=:typeNameinput), \
                (SELECT jobID FROM Jobs WHERE jobName = :jobNameInput),\
                (SELECT departmentID FROM Departments WHERE depName =:depNameInput));

 -- Departments--

INSERT INTO Departments (depName, description) VALUES(:depNameInput, :descriptionInput);;

 -- Employment Types--

INSERT INTO EmploymentTypes (typeName, hoursAllow) VALUES(:typeNameInput, :hoursAllowInput);

 -- Department_has_EmploymentTypes--

INSERT INTO Department_has_EmploymentTypes (departmentID, typeName) \
            VALUES((SELECT departmentID FROM Departments WHERE depName = :depNameInput),\
            (SELECT typeName FROM EmploymentTypes WHERE typeName = :typeNameinput));

 -- Jobs--

INSERT INTO Jobs (jobName, description) VALUES(:jobNameInput, :descriptionInput);

 -- Jobs_has_Departments--

INSERT INTO Jobs_has_Departments(jobID, departmentID)\
                VALUES((SELECT jobID FROM Jobs WHERE jobName = :jobNameInput),\
                (SELECT departmentID FROM Departments WHERE depName = :depNameInput));

 -- Schedules--

INSERT INTO Schedules (scheduleType, shift, startTime, endTime, employeeID, typeName, departmentID) \
             VALUES( :scheduleTypeInput, :shiftInput, startTimeInput, endTimeInput,\
            (SELECT employeeID FROM Employees WHERE name=:nameInputs),\
            (SELECT typeName FROM EmploymentTypes WHERE typeName = :typeNameInput),\
            (SELECT departmentID FROM Departments WHERE depName = :depNameInput));


----------|
--UPDATE--| 
----------|

--Employees--------------------|
--Fulfills setting FK to NULL--|
--Department ID is optional----| 
--relationship-----------------|

UPDATE Employees SET name = :nameInput, email = :emailInput, phoneNum = :phoneNumInput, typeName = :typeNameInput, \
            jobID = :jobIDInput, departmentID = :departmentIDInput WHERE employeeID = :employeeIDInput;


UPDATE Employees SET name = :nameInput, email = :emailInput, phoneNum = :phoneNumInput, typeName = :typeNameInput, \
            jobID = :jobIDInput, departmentID = :NULL WHERE employeeID = :employeeIDInput;


--Jobs-----------------------|
--Fulfills M:N relationship--|

UPDATE Jobs SET jobName = :jobNameInput, description = :descriptionInput WHERE Jobs.jobID = :jobIDInput;

--Departments----------------|
--Fulfills M:N relationship--|

UPDATE Departments SET depName = :depNameInput, description = :descriptionInput WHERE Departments.departmentID = :descriptionInput;


--Jobs_has_Departments----------------|

UPDATE Jobs_has_Departments SET jobID = :jobIDInput, departmentID = :departmentIDInput WHERE jobDeptID = :jobDeptIDInput

----------|
--DELETE--| 
----------|

--Employees--|

DELETE FROM Employees WHERE employeeID = :employeeIDInput;

--Departments----------------------------------------|
--Fulfills M:N relationship--------------------------|
--Will Delete if an FK's in both Intersection Tables-|

DELETE FROM Departments WHERE departmentID = :departmentIDInput;

--Jobs---------|

DELETE FROM Jobs WHERE jobID = :jobIDInput;

--EmploymentTypes---------|

DELETE FROM EmploymentTypes WHERE typeName = :typeNameInput;

--Department_has_EmploymentTypes---------------|

DELETE FROM Department_has_EmploymentTypes WHERE empDeptID = :empDeptIDInput;

--Jobs_had_Departments---------------|

DELETE FROM Jobs_has_Departments WHERE jobDeptID = :jobDeptIDInput;

--Schedules---------------|

DELETE FROM Schedules WHERE scheduleID = :scheduleIDInput;

--------------------|
--Drop Down Menu----|
--Represent FK's----|
--------------------|

SELECT employeeID, name FROM Employees;

SELECT departmentID, depName FROM Departments;

SELECT jobID, jobName FROM Jobs;

SELECT typeName FROM EmploymentTypes;



 