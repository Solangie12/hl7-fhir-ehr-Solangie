from connection import connect_to_mongodb
from bson import ObjectId
from fhir.resources.patient import Patient
import json

collection = connect_to_mongodb("SamplePatientService", "patients")

def GetPatientById(patient_id: str):
    try:
        patient = collection.find_one({"_id": ObjectId(patient_id)})
        if patient:
            patient["_id"] = str(patient["_id"])
            return "success", patient
        return "notFound", None
    except Exception as e:
        return f"notFound", None

def WritePatient(patient_dict: dict):
    try:
        pat = Patient.model_validate(patient_dict)
    except Exception as e:
        return f"errorValidating: {str(e)}",None
    validated_patient_json = pat.model_dump()
    result = collection.insert_one(patient_dict)
    if result:
        inserted_id = str(result.inserted_id)
        return "success",inserted_id
    else:
        return "errorInserting", None

def GetPatientByIdentifier(patientSystem, patientValue):
    try:
        patient = collection.find_one({
            "identifier": {
                "$elemMatch": {
                    "system": patientSystem,
                    "value": patientValue
                }
            }
        })
        if patient:
            patient["_id"] = str(patient["_id"])
            return "success", patient
        return "notFound", None
    except Exception as e:
        print("Error en GetPatientByIdentifier:", e)
        return "notFound", None

def ReadServiceRequest(service_request_id: str) -> dict:
    """
    Recupera una solicitud de servicio de la base de datos a partir de su ID.

    :param service_request_id: ID de la solicitud de servicio (como string).
    :return: Diccionario con los datos de la solicitud o None si no se encuentra.
    """
    try:
        # Intenta convertir el string del ID a un ObjectId de MongoDB
        query = {"_id": ObjectId(service_request_id)}
    except Exception as e:
        print(f"Error al convertir el ID: {e}")
        return None

    # Busca la solicitud en la colección
    service_request = collection.find_one(query)
    
    if service_request:
        # Convertir el ObjectId a string para que sea compatible con JSON
        service_request["_id"] = str(service_request["_id"])
        return service_request
    else:
        return None


def GetAppointmentByIdentifier(appointmentSystem, appointmentValue):
    try:
        appointment = appointments_collection.find_one({
            "identifier": {
                "$elemMatch": {
                    "system": appointmentSystem,
                    "value": appointmentValue
                }
            }
        })
        if appointment:
            appointment["_id"] = str(appointment["_id"])
            return "success", appointment
        return "notFound", None
    except Exception as e:
        print("Error en GetAppointmentByIdentifier:", e)
        return "notFound", None

