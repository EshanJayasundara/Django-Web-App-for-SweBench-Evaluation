from django.shortcuts import render
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
import json
import subprocess
from rest_framework_api_key.permissions import HasAPIKey
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework_api_key.models import APIKey
from django.contrib.auth.models import User
from decouple import config


@method_decorator(csrf_exempt, name='dispatch')
class SampleAPIView(APIView):
    permission_classes = [HasAPIKey]

    def get(self, request, id=None):
        return Response({
            "data": "Successfully, you reached an endpoint authenticated with an API-Key."
        })

@method_decorator(csrf_exempt, name='dispatch')
class SweAPIView(APIView):
    permission_classes = [HasAPIKey]

    def post(self, request, id=None):
        # APP_DIR = config('APP_DIR')
        # swebench_python = "SWE-bench/.venv/bin/python3"
        # swebench_script = "SWE-bench/swebench/harness/run_evaluation.py"

        # dataset_name = request.GET.get('dataset_name', 'princeton-nlp/SWE-bench_Lite')
        # max_workers = request.GET.get('max_workers', 1)
        # instance_ids = request.GET.get('instance_ids', 'sympy__sympy-20590')
        # run_id = request.GET.get('run_id', 'validate_gold')
        # prediction = request.GET.get('prediction')
        
        # try:
        #     result = subprocess.run(
        #         [swebench_python, swebench_script, "HelloFromCaller"],
        #         capture_output=True,
        #         text=True,
        #         timeout=300
        #     )

        #     return Response({
        #         'data': "Caller: subprocess completed",
        #         "STDOUT": f"{result.stdout.strip()}",
        #         "STDERR": f"{result.stderr.strip()}",
        #         "Return Code": f"{result.returncode}"
        #         })

        # except Exception as e:
        #     return Response(f"Caller: subprocess failed: {e}")
        data = json.loads(request.body.decode('utf-8'))
        return Response({
                'data': "Request processed successfully",
                'received_data': data
            })