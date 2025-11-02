from dotenv import load_dotenv


load_dotenv()

from graph.graph import app



if __name__ == "__main__":
    print("Automatic reliable code generation with documentation creation")

    print(app.invoke({"user_input": "Example user input"}))