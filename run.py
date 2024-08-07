from app import create_app
from app.scheduler import start_scheduler, update_data

app = create_app()

if __name__ == '__main__':
    update_data()  # Initial data fetch before starting the app
    app.run(debug=True)
    start_scheduler()