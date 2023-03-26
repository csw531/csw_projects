import time

class GPTSession:
    def __init__(self):
        self.start_time = None
        self.end_time = None
        self.quality_ratings = []

    def start_session(self):
        self.start_time = time.time()

    def end_session(self):
        self.end_time = time.time()

    def add_quality_rating(self, rating):
        if 1 <= rating <= 5:
            self.quality_ratings.append(rating)
        else:
            raise ValueError("Rating must be between 1 and 5")

    def get_session_duration(self):
        if self.start_time and self.end_time:
            return self.end_time - self.start_time
        else:
            raise ValueError("Session has not been started or ended")

    def get_average_quality(self):
        if len(self.quality_ratings) > 0:
            return sum(self.quality_ratings) / len(self.quality_ratings)
        else:
            raise ValueError("No quality ratings available")

class ChatGPT:
    def __init__(self):
        self.sessions = []

    def create_session(self):
        session = GPTSession()
        self.sessions.append(session)
        return session

    def total_time_spent(self):
        total_time = 0
        for session in self.sessions:
            if session.start_time and session.end_time:
                total_time += session.get_session_duration()
        return total_time

    def total_conversation_depth(self):
        depth = 0
        for session in self.sessions:
            depth += len(session.quality_ratings)
        return depth

if __name__ == "__main__":
    session = GPTSession()

    # Start a GPT session
    session.start_session()

    # Simulate interaction with GPT
    time.sleep(5)

    # End the session
    session.end_session()

    # Add quality ratings for the session
    session.add_quality_rating(4)
    session.add_quality_rating(5)

    # Get the session duration
    print(f"Session duration: {session.get_session_duration()} seconds")

    # Get the average quality
    print(f"Average quality: {session.get_average_quality()}")
