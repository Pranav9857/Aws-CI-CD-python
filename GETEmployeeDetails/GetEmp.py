import json
import logging

import azure.functions as func
import pymssql


def main(req: func.HttpRequest) -> func.HttpResponse:
    logging.info('Python HTTP trigger function processed a request.')

    # Retrieve the EmployeeID from query parameters or request body
    employee_id = req.params.get('EmployeeID')
    if not employee_id:
        try:
            req_body = req.get_json()
            employee_id = req_body.get('EmployeeID')
        except ValueError:
            pass

    if not employee_id:
        return func.HttpResponse(
            "Please provide the 'EmployeeID' parameter in the query string or request body.",
            status_code=400
        )

    # Connect to the SQL Server database
    server = 'lt-sqldb.database.windows.net'
    database = 'ltlab'
    username = 'ltadmin'
    password = 'LeverageTechnologies@2023'
    conn = pymssql.connect(server=server, database=database, user=username, password=password)

    try:
        with conn.cursor(as_dict=True) as cursor:
            # Execute the SQL query to retrieve employee details
            query = "SELECT * FROM Employee WHERE EmployeeID = %s"
            logging.info(f"SQL query: {query}")
            cursor.execute(query, (employee_id,))
            rows = cursor.fetchall()

            if rows:
                logging.info(f"Number of rows retrieved: {len(rows)}")
                # Convert rows to a list of dictionaries
                rows_dict = [dict(row) for row in rows]
                # Return the rows as JSON response
                return func.HttpResponse(body=json.dumps(rows_dict), mimetype='application/json')
            else:
                logging.info("No rows retrieved.")
                return func.HttpResponse("Employee not found.", status_code=404)
    except pymssql.Error as e:
        logging.error(f"Database connection or query error: {str(e)}")
        return func.HttpResponse("Internal Server Error", status_code=500)
    finally:
        conn.close()
