from app import create_app

app = create_app()

if __name__ == "__main__":
    print("Agentic Banking Backend Running on Port 5000")
    app.run(debug=True, port=5000)
