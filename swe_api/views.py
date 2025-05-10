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


@method_decorator(csrf_exempt, name='dispatch')
class SampleAPIView(APIView):
    permission_classes = [HasAPIKey]

    def get(self, request, id=None):
        return Response({
            "data": "Successfully, you reached an endpoint authenticated with an API-Key."
        })
        # swebench_python = "D:\\FYP\\google_cloud\\swe-bench\\swe_venv\\Scripts\\python"
        # swebench_script = "D:\\FYP\\google_cloud\\swe-bench\\responder.py"

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