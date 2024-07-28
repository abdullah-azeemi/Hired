print("Starting application...")
from app.init import create_app
print("Imported create_app from app")

app = create_app()
print("Created app instance")

if __name__ == "__main__":
    print("Running app...")
    app.run(debug=True)
