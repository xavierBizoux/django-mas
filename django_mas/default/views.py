import json
import os

import swat
from django.http import HttpResponse, JsonResponse
from django.template import loader
from django.views.decorators.csrf import csrf_exempt
from dotenv import load_dotenv
from sasctl import Session
from sasctl.services import microanalytic_score as mas

from .models import ScoredData

load_dotenv()  # loads the configs from .env

SERVER = str(os.getenv("SERVER"))
USERNAME = str(os.getenv("USERNAME"))
PASSWORD = str(os.getenv("PASSWORD"))
CERTIFICATE = str(os.getenv("CERTIFICATE"))


def get_cas_session(request):
    if request.COOKIES.get("cas_session_id") != None:
        try:
            session_id = request.COOKIES.get("cas_session_id")
            cas_session = swat.CAS(
                f"{SERVER}/cas-shared-default-http",
                ssl_ca_list=CERTIFICATE,
                session=session_id,
            )
            return cas_session
        except Exception:
            print(f"Session {session_id} is not valid!")
    cas_session = swat.CAS(
        f"{SERVER}/cas-shared-default-http",
        username=USERNAME,
        password=PASSWORD,
        ssl_ca_list=CERTIFICATE,
    )
    return cas_session


def index(request):
    cas_session = get_cas_session(request)
    cas_session_id = getattr(cas_session, "_session")
    cas_table = cas_session.CASTable(name="Cars", caslib="Public")
    template = loader.get_template("default/index.html")
    context = {"origins": cas_table.origin.unique()}
    response = HttpResponse(template.render(context, request))
    response.set_cookie("cas_session_id", cas_session_id, max_age=15 * 60)
    return response


def get_make(request):
    cas_session = get_cas_session(request)
    cas_session_id = getattr(cas_session, "_session")
    cas_table = cas_session.CASTable(name="Cars", caslib="Public")
    table_filter = f"origin=\"{request.GET.get('origin')}\""
    data = cas_table.query(table_filter).to_frame()
    json_response = {"values": data.Make.unique().tolist()}
    response = JsonResponse(json_response)
    response.set_cookie("cas_session_id", cas_session_id)
    return response


def get_model(request):
    cas_session = get_cas_session(request)
    cas_session_id = getattr(cas_session, "_session")
    cas_table = cas_session.CASTable(name="Cars", caslib="Public")
    table_filter = (
        f"origin=\"{request.GET.get('origin')}\"&make=\"{request.GET.get('make')}\""
    )
    data = cas_table.query(table_filter).to_frame()
    json_response = {"values": data.Model.unique().tolist()}
    response = JsonResponse(json_response)
    response.set_cookie("cas_session_id", cas_session_id)
    return response


def get_details(request):
    cas_session = get_cas_session(request)
    cas_session_id = getattr(cas_session, "_session")
    cas_table = cas_session.CASTable(name="Cars", caslib="Public")
    table_filter = f"origin=\"{request.GET.get('origin')}\"&make=\"{request.GET.get('make')}\"&model=\"{request.GET.get('model')}\""
    data = cas_table.query(table_filter).to_frame()
    json_response = {"columns": list(data.columns), "rows": list(data.loc[0])}
    response = JsonResponse(json_response)
    response.set_cookie("cas_session_id", cas_session_id)
    return response


@csrf_exempt
def score_data(request):
    data = json.loads(request.body.decode("utf-8"))
    with Session(SERVER, USERNAME, PASSWORD, verify_ssl=CERTIFICATE):
        result = mas.execute_module_step("msrp_prediction", "score", **data)
        record = ScoredData()
        predicted_data = {**data, **result}
        for key, value in predicted_data.items():
            setattr(record, key, value)
        record.save()
        response = JsonResponse(result)
        return response
