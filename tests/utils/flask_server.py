import json
import os
import socket
import time
import subprocess
import sys
from pathlib import Path


HOST = '127.0.0.1'
PORT = '5000'
BASE_URL = f'http://{HOST}:{PORT}'


def wait_for_server(host, port, server_process, timeout_seconds=5.0):
    '''Create a loop to allow Flask time to launch and avoid connection errors.'''
    start = time.time()

    # Loop until server responds or timeout expires
    while True:
        # If Flask process stopped, returns error details
        if server_process.poll() is not None:
            out, err = server_process.communicate(timeout=1)
            raise RuntimeError(
                "Server process exited early.\n"
                f"Exit code: {server_process.returncode}\n"
                f"STDOUT:\n{out}\n"
                f"STDERR:\n{err}\n"
            )
        
        # If error is returned then the server is not yet ready
        try:
            with socket.create_connection((host, port), timeout=0.2):
                return
        except OSError:
            # Check if timeout is expired
            if time.time() - start > timeout_seconds:
                out, err = server_process.communicate(timeout=1)
                raise RuntimeError(
                    f"Server not ready on {host}:{port} after {timeout_seconds}s\n"
                    f"STDOUT:\n{out}\n"
                    f"STDERR:\n{err}\n"
                )
        
        # Let some time before trying to create connection again
        time.sleep(0.05)


def start_server_with_temp_data(tmp_path):
    '''
    Create fake temporary JSON data to use during tests and launch Flask
    '''
    # Create temporary path
    clubs_path = tmp_path / 'clubs.json'
    competitions_path = tmp_path / 'competitions.json'

    # Create test data
    clubs_data = {'clubs':[
        {'name': 'Test Club', 'email': 'test@club.com', 'points': '10'},
        {'name': 'Test Club 2', 'email': 'test2@club.com', 'points': '15'}
    ]}

    competitions_data = {'competitions':[
        {'name': 'Test Competition', 'date': '2045-02-12 12:30:00', 'numberOfPlaces': '15'},
        {'name': 'Test Competition 2', 'date': '2026-01-01 14:00:00', 'numberOfPlaces': '8'}
    ]}

    # Save data in temporary files
    clubs_path.write_text(json.dumps(clubs_data), encoding='utf-8')
    competitions_path.write_text(json.dumps(competitions_data), encoding='utf-8')

    # Copy environment to protect it and setup variables
    env = os.environ.copy()

    env['CLUBS_FILEPATH'] = str(clubs_path)
    env['COMPETITIONS_FILEPATH'] = str(competitions_path)
    env['FLASK_APP'] = 'server.py'
    env['FLASK_DEBUG'] = '0'

    project_root = Path(__file__).resolve().parents[2]

    # Start Flask
    server_process = subprocess.Popen(
        [sys.executable, '-m', 'flask', 'run',
         '--host', HOST,
         '--port', PORT],
        cwd=str(project_root),
        env=env,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True,
    )

    wait_for_server(HOST, PORT, server_process)
    return server_process


def stop_server(server_process):
    '''Used to stop Flask process'''
    server_process.terminate()

    # Give some time for the process to stop and terminate it if it does not
    server_process.wait(timeout=2)
