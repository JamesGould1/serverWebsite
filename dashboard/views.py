import subprocess
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
import docker


def custom_login(request):
    if request.method == 'POST':
        password = request.POST['password']
        username = 'shareduser'
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('index')  # name of your dashboard view
        else:
            return render(request, 'dashboard/login.html', {'error': 'Invalid credentials'})
    
    return render(request, 'dashboard/login.html')
@login_required
def index(request):
    context = {}
    return render(request, "dashboard/index.html", context)

@login_required
def start_server(request, server_name):
    if server_name == "vanilla":
        server_id = 'aff99c49db5b'  # put real container ID or name here
    elif server_name == "modded":
        server_id = 'e9f02a7d47bb'  # put real container ID or name here
    else:
        return JsonResponse({"error": "Invalid server name"}, status=400)

    try:
        print("running: docker start " + server_id)
        subprocess.run(['docker', 'start', server_id], check=True)
        return JsonResponse({"message": f"Server {server_name} started successfully."})
    except subprocess.CalledProcessError:
        return JsonResponse({"error": f"Failed to start server {server_name}."})

@login_required
def stop_server(request, server_name):
    if server_name == "vanilla":
        server_id = 'aff99c49db5b'
    elif server_name == "modded":
        server_id = 'e9f02a7d47bb'
    else:
        return JsonResponse({"error": "Invalid server name"}, status=400)
    
    try:
        client = docker.from_env()
        container = client.containers.get(server_id)
        container.stop()
        return JsonResponse({"message": f"Server {server_name} stopped successfully."})
    except docker.errors.NotFound:
        return JsonResponse({"error": f"Container {server_id} not found."})
    except docker.errors.APIError as e:
        return JsonResponse({"error": f"Failed to stop server {server_name}: {str(e)}"})
    except Exception as e:
        return JsonResponse({"error": f"Unexpected error: {str(e)}"})