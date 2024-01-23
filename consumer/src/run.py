import argparse
import os

from dotenv import load_dotenv
import uvicorn

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Run the server in different modes.")

    app_mode = parser.add_argument_group(
        title="App Mode", description="Run the server in different modes."
    )
    app_mode.add_argument(
        "--prod", action="store_true", help="Run the server in production mode."
    )
    app_mode.add_argument(
        "--dev", action="store_true", help="Run the server in development mode."
    )
    app_mode.add_argument(
        "--k8s", action="store_true", help="Run the server in k8s environment."
    )

    args = parser.parse_args()

    if args.dev:
        # for development mode
        load_dotenv(".env/dev.env")


    uvicorn.run(
        "app:app",
        host="0.0.0.0",
        port=int(os.getenv("PORT")),
        reload=bool(os.getenv("RELOAD")),
    )
