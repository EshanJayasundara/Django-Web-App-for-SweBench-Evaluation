from django.shortcuts import render
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from django.conf import settings
import json
import subprocess
from rest_framework_api_key.permissions import HasAPIKey
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework_api_key.models import APIKey
from django.contrib.auth.models import User
from rest_framework.parsers import MultiPartParser, FormParser
from decouple import config
import os

@method_decorator(csrf_exempt, name='dispatch')
class FileUploadView(APIView):
    permission_classes = [HasAPIKey]
    parser_classes = [MultiPartParser, FormParser]

    def post(self, request, id=None):
        UPLOAD_DIR = os.path.join(config('APP_DIR'), "SWE-bench", "uploaded_files")
        os.makedirs(UPLOAD_DIR, exist_ok=True)  # Ensure dir exists
        uploaded_file = request.FILES.get('file')

        if not uploaded_file:
            return Response({"status": "error", "message": "No file uploaded."})

        if not uploaded_file.name.endswith('.jsonl'):
            return Response({"status": "error", "message": "Only .jsonl files are allowed."})

        file_path = os.path.join(UPLOAD_DIR, uploaded_file.name)

        # Save the uploaded file
        with open(file_path, 'wb+') as destination:
            for chunk in uploaded_file.chunks():
                destination.write(chunk)

        return Response({
            "status": "success",
            "message": f"File '{uploaded_file.name}' uploaded successfully.",
            "path": file_path
        })


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

    # def post(self, request, id=None):
    #     APP_DIR = config('APP_DIR')
    #     swebench_python = "SWE-bench/.venv/bin/python3"
    #     swebench_script = "SWE-bench/swebench/harness/run_evaluation.py"

    #     data = json.loads(request.body.decode('utf-8'))

    #     dataset_name = data.get('dataset_name', 'princeton-nlp/SWE-bench_Lite')
    #     max_workers = data.get('max_workers', 1)
    #     run_id = data.get('run_id', 'my_first_evaluation')
    #     predictions = data.get('predictions', None)
    #     instance_ids = []

    #     # if len(predictions) > 1:
    #     #     return Response("Eventhough, 'predictions' is a list. Currently support only one prediction at a time.")

    #     with open(f'{APP_DIR}/SWE-bench/predictions.jsonl', 'w') as f:
    #         for prediction in predictions:
    #             if set(prediction.keys()) != {"instance_id", "model_name_or_path", "model_patch"}:
    #                 return Response("Invalid keys in predictions list.")
    #             instance_ids.append(prediction['instance_id'])
    #             json.dump(prediction, f)
    #             f.write('\n')
    #         f.close()

    #     if max_workers > 3:
    #         return Response("Maximim worksers allowed is 3.")
        
    #     if dataset_name != 'princeton-nlp/SWE-bench_Lite':
    #         return Response("Currently only 'princeton-nlp/SWE-bench_Lite' is supported")
        
    #     if not predictions:
    #         return Response("Predictions can not be empty.")

    #     command = [
    #         swebench_python,
    #         swebench_script,
    #         "--dataset_name", dataset_name,
    #         "--max_workers", str(max_workers),
    #         "--instance_ids", *instance_ids,  # ✅ this expands to multiple args
    #         "--run_id", run_id,
    #         "--predictions_path", f"{APP_DIR}/SWE-bench/predictions.jsonl",
    #     ]

    #     try:
    #         result = subprocess.run(
    #             command,
    #             capture_output=True,
    #             text=True,
    #             timeout=300  # Increase timeout if SWE-bench takes longer
    #         )

    #         # response_data = dict([o.strip().split(": ") for o in result.stdout.strip().split("\n") if ":" in o])
    #         # response_data = {}
    #         # for line in result.stdout.strip().split("\n"):
    #         #     if ":" in line:
    #         #         try:
    #         #             key, value = line.strip().split(":", 1)
    #         #             response_data[key.strip()] = value.strip()
    #         #         except ValueError as e:
    #         #             # Log or skip malformed lines
    #         #             print(f"Skipping malformed line: {line} -- {e}")

    #         return Response({
    #             "status": "success",
    #             "data": result.stdout.strip().split("\n"), # response_data,
    #             "stderr": result.stderr.strip(),
    #             "returncode": result.returncode
    #             # "command": command
    #             })

    #     except subprocess.TimeoutExpired:
    #         return Response({"status": "error", "details": "Subprocess timed out."})

    #     except Exception as e:
    #         return Response({"status": "error", "details": str(e)})

    def post(self, request, id=None):
        APP_DIR = config('APP_DIR')
        UPLOAD_DIR = os.path.join(APP_DIR, "SWE-bench", "uploaded_files")
        os.makedirs(UPLOAD_DIR, exist_ok=True)  # Ensure dir exists

        swebench_python = "SWE-bench/.venv/bin/python3"
        swebench_script = "SWE-bench/swebench/harness/run_evaluation.py"

        dataset_name = request.data.get('dataset_name', 'princeton-nlp/SWE-bench_Lite')
        max_workers = int(request.data.get('max_workers', 1))
        run_id = request.data.get('run_id', 'my_first_evaluation')
        predictions_path = f"{UPLOAD_DIR}/predictions.jsonl"  # full path to the .jsonl file

        if not predictions_path:
            return Response({"status": "error", "details": "Missing 'predictions_path' parameter."})

        updated_predictions = []
        instance_ids = []
        try:
            # Read and modify
            with open(predictions_path, 'r', encoding='utf-8') as f:
                for line in f:
                    line = line.strip()
                    if not line:
                        continue
                    try:
                        prediction = json.loads(line)
                    except json.JSONDecodeError:
                        return Response({"status": "error", "details": "Invalid JSON in predictions file."})

                    if "model_name_or_path" not in prediction:
                        prediction["model_name_or_path"] = "debugai"

                    required_keys = {"instance_id", "model_name_or_path", "model_patch"}
                    if set(prediction.keys()) != required_keys:
                        return Response({"status": "error", "details": f"Invalid keys in prediction: {prediction}"})

                    updated_predictions.append(prediction)
                    instance_ids.append(prediction['instance_id'])

            # Write back to the same file
            with open(predictions_path, 'w', encoding='utf-8') as f:
                for prediction in updated_predictions:
                    json.dump(prediction, f)
                    f.write('\n')

        except FileNotFoundError:
            return Response({"status": "error", "details": f"Predictions file not found: {predictions_path}"})
        except Exception as e:
            return Response({"status": "error", "details": f"Error reading predictions file: {str(e)}"})

        if not updated_predictions:
            return Response({"status": "error", "details": "Predictions cannot be empty."})

        if max_workers > 3:
            return Response({"status": "error", "details": "Maximum workers allowed is 3."})

        if dataset_name != 'princeton-nlp/SWE-bench_Lite':
            return Response({"status": "error", "details": "Only 'princeton-nlp/SWE-bench_Lite' is supported."})

        command = [
            swebench_python,
            swebench_script,
            "--dataset_name", dataset_name,
            "--max_workers", str(max_workers),
            "--instance_ids", *instance_ids,
            "--run_id", run_id,
            "--predictions_path", predictions_path,
        ]

        try:
            result = subprocess.run(
                command,
                capture_output=True,
                text=True,
                timeout=300
            )

            with open(f"{APP_DIR}/{run_id}")
            return Response({
                "status": "success",
                "data": 
                "stdout": result.stdout.strip().split("\n"),
                "stderr": result.stderr.strip(),
                "returncode": result.returncode
            })

        except subprocess.TimeoutExpired:
            return Response({"status": "error", "details": "Subprocess timed out."})
        except Exception as e:
            return Response({"status": "error", "details": str(e)})
        