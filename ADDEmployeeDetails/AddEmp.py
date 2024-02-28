import logging

import azure.functions as func
import pymssql


def main(req: func.HttpRequest) -> func.HttpResponse:
    logging.info('Python HTTP trigger function processed a request.')
    
    # Retrieve the employee details from the request body
    try:
        req_body = req.get_json()
        employee_id = req_body.get('EmployeeID')
        lastname = req_body.get('Lastname')
        firstname = req_body.get('Firstname')
        middle_initial = req_body.get('MiddleInitial')
        birth_date = req_body.get('BirthDate')
        ssn = req_body.get('SSN')
        job_title = req_body.get('JobTitle')
        work_location = req_body.get('Worklocation')
        work_desk_id = req_body.get('WorkDeskID')
        work_phone = req_body.get('Workphone')
        cell_phone = req_body.get('CellPhone')
        organization = req_body.get('Organization')
        supervisor_name = req_body.get('SupervisorName')
        supervisor_job_title = req_body.get('SupervisorJobTitle')
        supervisor_contact_number = req_body.get('SupervisorContactNumber')
        hire_date = req_body.get('HireDate')
        annual_salary = req_body.get('AnnualSalary')
        residence_address = req_body.get('ResidenceAddress')
        #address_street1 = residence_address.get('AddressStreet1')
        #address_street2 = residence_address.get('AddressStreet2')
        #address_city = residence_address.get('AddressCity')
        #address_state = residence_address.get('AddressState')
        #address_zip = residence_address.get('AddressZip')
    except ValueError:
        return func.HttpResponse(
            "Invalid request body.",
            status_code=400
        )
    
    # Connect to the SQL Server database
    server = 'lt-sqldb.database.windows.net'
    database = 'ltlab'
    username = 'ltadmin'
    password = 'LeverageTechnologies@2023'
    conn = pymssql.connect(server=server, database=database, user=username, password=password)

    try:
        with conn.cursor() as cursor:
            # Execute the SQL query to insert employee details
            query = """
            INSERT INTO Employee (
                EmployeeID, Lastname, Firstname, MiddleInitial, BirthDate, SSN, JobTitle,
                Worklocation, WorkDeskID, Workphone, CellPhone, Organization,
                SupervisorName, SupervisorJobTitle, SupervisorContactNumber, HireDate,
                AnnualSalary, ResidenceAddress
            )
            VALUES (
                %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s
            )
            """
            logging.info(f"SQL query: {query}")
            cursor.execute(
                query,
                (
                    employee_id, lastname, firstname, middle_initial, birth_date, ssn, job_title,
                    work_location, work_desk_id, work_phone, cell_phone, organization,
                    supervisor_name, supervisor_job_title, supervisor_contact_number, hire_date,
                    annual_salary, residence_address
                )
            )
            conn.commit()
            
            logging.info("Employee details inserted.")
            return func.HttpResponse("Employee details inserted successfully.", status_code=200)
    except pymssql.Error as e:
        logging.error(f"Database connection or query error: {str(e)}")
        return func.HttpResponse("Internal Server Error", status_code=500)
    finally:
        conn.close()

