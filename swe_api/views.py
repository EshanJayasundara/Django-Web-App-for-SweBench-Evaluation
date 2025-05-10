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
            "data": "Successfully, you reached the 'test' endpoint authenticated with an API-Key."
        })

@method_decorator(csrf_exempt, name='dispatch')
class SweAPIView(APIView):
    permission_classes = [HasAPIKey]

    def post(self, request, id=None):
        APP_DIR = config('APP_DIR')
        swebench_python = "SWE-bench/.venv/bin/python3"
        swebench_script = "SWE-bench/swebench/harness/run_evaluation.py"

        data = json.loads(request.body.decode('utf-8'))

        dataset_name = data.get('dataset_name', 'princeton-nlp/SWE-bench_Lite')
        max_workers = data.get('max_workers', 1)
        run_id = data.get('run_id', 'my_first_evaluation')
        predictions = data.get('predictions', None)
        instance_ids = []

        if len(predictions) > 1:
            return Response("Eventhough, 'predictions' is a list. Currently support only one prediction at a time.")

        with open(f'{APP_DIR}/SWE-bench/predictions.jsonl', 'w') as f:
            for prediction in predictions:
                if set(prediction.keys()) != {"instance_id", "model_name_or_path", "model_patch"}:
                    return Response("Invalid keys in predictions list.")
                instance_ids.append(prediction['instance_id'])
                json.dump(prediction, f)
                f.write('\n')
            f.close()

        if max_workers > 3:
            return Response("Maximim worksers allowed is 3.")
        
        if dataset_name != 'princeton-nlp/SWE-bench_Lite':
            return Response("Currently only 'princeton-nlp/SWE-bench_Lite' is supported")
        
        if not predictions:
            return Response("Predictions can not be empty.")

        command = [
            swebench_python, swebench_script,
            "--dataset_name", dataset_name,
            "--max_workers", str(max_workers),
            "--instance_ids", " ".join(instance_ids),
            "--run_id", run_id,
            "--predictions_path", f"{APP_DIR}/SWE-bench/predictions.jsonl",
        ]

        try:
            result = subprocess.run(
                command,
                capture_output=True,
                text=True,
                timeout=300  # Increase timeout if SWE-bench takes longer
            )

            response_data = dict([o.strip().split(":") for o in result.stdout.strip().split("\n") if ":" in o])

            return Response({
                "status": "success",
                "data": response_data,
                "stderr": result.stderr.strip(),
                "returncode": result.returncode
                })

        except subprocess.TimeoutExpired:
            return Response({"status": "error", "details": "Subprocess timed out."})

        except Exception as e:
            return Response({"status": "error", "details": str(e)})