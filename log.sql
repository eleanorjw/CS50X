-- Keep a log of any SQL queries you execute as you solve the mystery.

--description of crimescene report
Select description
FROM crime_scene_reports
WHERE year = 2020 AND month = 7 AND day = 28 AND street = "Chamberlin Street";
--3 interviews 

--transcript of interviews
SELECT name, transcript
FROM interviews
WHERE year = 2020 AND month = 7 AND day = 28;
--Eugene, Raymond, Ruth (ATM on Fifer Street, 
--they called someone who talked to them for less than a minute. In the call, I heard the thief say that they were planning to take the earliest flight out of Fiftyville tomorrow. The thief then asked the person on the other end of the phone to purchase the flight ticket., 
--within ten minutes of the theft, I saw the thief get into a car in the courthouse parking lot and drive away.)

--footage
SELECT activity, license_plate
FROM courthouse_security_logs
WHERE year = 2020 AND month = 7 AND day = 28 AND hour = 10 AND minute >= 15 AND minute <= 25;
--5P2BI95 94KL13X 6P58WS2 4328GD8 G412CB7 L93JTIZ 322W7JE 0NTHK55

--phonecall
SELECT caller, receiver
FROM phone_calls
WHERE year = 2020 AND month = 7 AND day = 28 AND duration < 60;

--atm
SELECT account_number, amount
FROM atm_transactions
WHERE year = 2020 AND month = 7 AND day = 28 AND transaction_type = "withdraw";

--flight
SELECT id, destination_airport_id
FROM flights
WHERE origin_airport_id IN (SELECT id FROM airports WHERE city LIKE "fiftyville")
AND year = 2020 AND month = 7 AND day = 29
ORDER BY hour, minute;
--36, 4


--REVEAL
--thief
SELECT name
FROM people
JOIN bank_accounts
ON bank_accounts.person_id = people.id
WHERE phone_number IN (SELECT caller FROM phone_calls WHERE year = 2020 AND month = 7 AND day = 28 AND duration < 60)
AND passport_number IN (SELECT passport_number FROM passengers WHERE flight_id = (SELECT id FROM flights WHERE origin_airport_id = (SELECT id FROM airports WHERE city LIKE "fiftyville") AND year = 2020 AND month = 7 AND day = 29 ORDER BY hour, minute LIMIT 1))
AND license_plate IN (SELECT license_plate FROM courthouse_security_logs WHERE year = 2020 AND month = 7 AND day = 28 AND hour = 10 AND minute >= 15 AND minute <= 25 AND activity = "exit")
AND account_number IN (SELECT account_number FROM atm_transactions WHERE year = 2020 AND month = 7 AND day = 28 AND transaction_type = "withdraw");
--Ernest

--accomplice
SELECT name
FROM people
WHERE phone_number = (SELECT receiver FROM phone_calls WHERE year = 2020 AND month = 7 AND day = 28 AND duration < 60 AND caller = (SELECT phone_number FROM people WHERE name = "Ernest"));
--Berthold

--city
SELECT city
FROM airports
WHERE id = 4;
--London