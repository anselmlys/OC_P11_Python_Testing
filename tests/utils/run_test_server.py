import tempfile
from pathlib import Path

import flask_server


def main():
    # Create a temporary folder to stock JSON test files
    with tempfile.TemporaryDirectory() as tmp_dir:
        tmp_path = Path(tmp_dir)

        # Start the server
        server_process = flask_server.start_server_with_temp_data(tmp_path)

        try:
            print(f'Test server running at: {flask_server.BASE_URL}')
            print('Press Ctrl+C to stop the server...')
            while True:
                pass

        # Ctrl+C stops the server 
        except KeyboardInterrupt:
            print('Stopping server')
        
        # Make sure to stop the server
        finally:
            flask_server.stop_server(server_process)


if __name__ == '__main__':
    main()
