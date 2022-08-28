import tempfile
from pathlib import Path

import uvicorn
from fastapi import FastAPI, Form, UploadFile
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from starlette.background import BackgroundTasks
from starlette.responses import FileResponse, RedirectResponse

from recipe_xml_converter import config
from recipe_xml_converter.helpers import setup_logging
from recipe_xml_converter.orchestrator import RecipeOrchestrator

setup_logging()

app = FastAPI()
"""The FastAPI app to use for the HTTP requests."""

app.mount(
    "/home",
    StaticFiles(directory=Path(__file__).parent.parent / "static", html=True),
    name="static",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/")
async def homepage() -> RedirectResponse:
    """Redirect to the homepage."""
    return RedirectResponse(url="/home")


@app.post("/api/transform/")
async def transform_recipes(
    files: list[UploadFile],
    background_tasks: BackgroundTasks,
    max_combined_files: int = Form(),
) -> FileResponse:
    """
    Transform RecipeML files to MyCookbook XML ones and return a zip containing the results.

    :param files: the RecipeML files
    :param background_tasks: tasks to run after the response is returned
    :param max_combined_files: the maximum number of files to combine in one
    :return: a zip file containing all the transformed MyCookbook XML files
    """
    temp_dir = tempfile.TemporaryDirectory(dir=config.BASE_DATA_DIR)
    background_tasks.add_task(lambda d: d.cleanup(), temp_dir)

    orchestrator = RecipeOrchestrator(
        tuple([f.file for f in files]), Path(temp_dir.name), max_combined_files
    )
    return FileResponse(
        orchestrator.orchestrate(),
        media_type="application/zip",
    )


def start_server() -> None:
    """Start the uvicorn server."""
    uvicorn.run(app, host="0.0.0.0", port=8000)


if __name__ == "__main__":
    start_server()
