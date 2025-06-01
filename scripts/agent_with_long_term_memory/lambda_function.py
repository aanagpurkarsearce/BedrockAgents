import json
import uuid
import boto3

def get_named_parameter(event, name):
    """
    Get a parameter from lambda event
    """
    return next(item for item in event['parameters'] if item['name'] == name)['value']

def book_trip(origin, destination, start_date, end_date, transportation_mode):
    """
    Book a trip and return booking_id
    """
    booking_id = str(uuid.uuid4())[:8]
    return f"Successfully booked trip from {origin}({start_date}) to {destination}({end_date}) via {transportation_mode}. Booking ID is {booking_id}"


def populate_function_response(event, response_body):
    return {
        'response':{
            'actionGroup': event['actionGroup'],
            'function': event['function'],
            'functionResponse':{
                'responseBody': {
                    'TEXT': {
                        'body': response_body
                    }
                }
            }
        }
    }

def update_existing_trip_dates(booking_id, new_start_date, new_end_date):
    return f"Successfully updated trip details for booking_id {booking_id} with start_date {new_start_date} and end_date {new_end_date}"


def delete_existing_trip_reservation(booking_id):
    return f"Successfully cancelled reservation for booking_id {booking_id}"


def lambda_handler(event, context):
    # get action group, function and parameters
    actionGroup = event.get('actionGroup', '')
    function = event.get('function', '')
    parameters = event.get('parameters', [])

    if function == "update_existing_trip_dates":
        booking_id = get_named_parameter(event, "booking_id")
        new_start_date = get_named_parameter(event, "new_start_date")
        new_end_date = get_named_parameter(event, "new_end_date")
        if booking_id and new_start_date and new_end_date:
            response = update_existing_trip_dates(booking_id, new_start_date, new_end_date)
            result = json.dumps(response)
        else:
            result = "Missing required parameters"
    
    elif function == "book_trip":
        origin = get_named_parameter(event, "origin")
        destination = get_named_parameter(event, "destination")
        start_date = get_named_parameter(event, "start_date")
        end_date = get_named_parameter(event, "end_date")
        transportation_mode = get_named_parameter(event, "transportation_mode")

        if origin and destination and start_date and end_date and transportation_mode:
            response = book_trip(origin, destination, start_date, end_date, transportation_mode)
            result = json.dumps(response)
        
        else:
            result = "Missing required parameters"
    
    elif function == "delete_existing_trip_reservation":
        booking_id = get_named_parameter(event, "booking_id")
        
        if booking_id:
            response = delete_existing_trip_reservation(booking_id)
            result = json.dumps(response)
        else:
            result = "Missing booking_id"
    
    else:
        result = "Invalid Function"
    
    action_response = populate_function_response(event, result)

    print(action_response)

    return action_response
