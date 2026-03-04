from locust import HttpUser, task, between


MAX_LOAD_SECONDS = 5.0
MAX_UPDATE_SECONDS = 2.0


class GudlftPerformanceTest(HttpUser):
    # Helps simulate human behaviour
    wait_time = between(1, 2)

    # Define test data
    test_email = 'test@club.com'
    test_club_name = 'Test Club 2'
    test_competition_name = 'Test Competition'
    booked_places = '5'

    @task
    def browse_and_book(self):
        # Load the index page
        with self.client.get('/', catch_response=True) as response:
            elapsed_time = response.elapsed.total_seconds()

            # Fails if HTTP code is not 200
            if response.status_code != 200:
                response.failure(f'GET / returned {response.status_code}')

            # Fails if too slow
            elif elapsed_time > MAX_LOAD_SECONDS:
                response.failure(f'GET / too slow: {elapsed_time} > {MAX_LOAD_SECONDS}s')

            else:
                response.success()

        # Load /showSummary
        with self.client.post(
            '/showSummary',
            data={'email': self.test_email},
            catch_response=True,
        ) as response:
            elapsed_time = response.elapsed.total_seconds()

            if response.status_code != 200:
                response.failure(f'GET /showSummary returned {response.status_code}')
            
            elif elapsed_time > MAX_LOAD_SECONDS:
                response.failure(f'GET /showSummary too slow: {elapsed_time} > {MAX_LOAD_SECONDS}s')
            
            elif "Points available" not in response.text:
                response.failure("POST /showSummary did not return expected page content")
            
            else:
                response.success()

        book_url = f'/book/{self.test_competition_name}/{self.test_club_name}'
        # Load booking page
        with self.client.get(book_url, catch_response=True) as response:
            elapsed_time = response.elapsed.total_seconds()

            if response.status_code != 200:
                response.failure(f'GET {book_url} returned {response.status_code}')
            
            elif elapsed_time > MAX_LOAD_SECONDS:
                response.failure(f'GET {book_url} too slow: {elapsed_time} > {MAX_LOAD_SECONDS}s')
            
            elif "How many places" not in response.text:
                response.failure("Booking page content not found")
            
            else:
                response.success()

        # Load and update after booking
        with self.client.post(
            '/purchasePlaces',
            data={
                'competition': self.test_competition_name,
                'club': self.test_club_name,
                'places': self.booked_places
            },
            catch_response=True
        ) as response:
            elapsed_time = response.elapsed.total_seconds()

            if response.status_code != 200:
                response.failure(f'POST /purchasePlaces returned {response.status_code}')
            
            elif elapsed_time > MAX_UPDATE_SECONDS:
                response.failure(f'POST /purchasePlaces too slow: {elapsed_time} > {MAX_UPDATE_SECONDS}s')
            
            elif "Great-booking complete" not in response.text:
                response.failure("Booking confirmation message not found")
            
            else:
                response.success()
