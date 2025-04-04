from connection import connect_to_mongodb
from bson import ObjectId
from fhir.resources.patient import Patient
import json

# Conexión a la base de datos para la colección de pacientes
collection = connect_to_mongodb("SamplePatientService", "patients")
# Conexión a la base de datos para la colección de solicitudes de servicio
service_requests_collection = connect_to_mongodb("SamplePatientService", "service_requests")

def GetPatientById(patient_id: str):
    try:
        patient = collection.find_one({"_id": ObjectId(patient_id)})
        if patient:
            patient["_id"] = str(patient["_id"])
            return "success", patient
        return "notFound", None
    except Exception as e:
        print("Error in GetPatientById:", e)
        return "notFound", None

def WritePatient(patient_dict: dict):
    try:
        pat = Patient.model_validate(patient_dict)
    except Exception as e:
        print("Error validating patient:", e)
        return f"errorValidating: {str(e)}", None
    # Es recomendable insertar el objeto validado en lugar del dict original
    validated_patient_json = pat.model_dump()
    result = collection.insert_one(validated_patient_json)
    if result:
        inserted_id = str(result.inserted_id)
        return "success", inserted_id
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
        print("Error in GetPatientByIdentifier:", e)
        return "notFound", None

def WriteServiceRequest(service_request_data: dict):
    try:
        # Inserta la solicitud en la colección configurada para solicitudes de servicio
        result = service_requests_collection.insert_one(service_request_data)
        return "success", str(result.inserted_id)
    except Exception as e:
        print("Error in WriteServiceRequest:", e)
        return "error", None


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

