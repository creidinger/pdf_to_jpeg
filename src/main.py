import json
import os
import logging

# 3rd party
from wand.image import Image
import requests


# init logger
logger = logging.getLogger()
logging.basicConfig(filename="logger.log", level=logging.INFO)

logging.info("PDF to Jpeg")


def pdf_to_jpeg(file_name):
    """Convert PDF to JPEG

    Args:
        file_name (string): The file we'll be using for the image
        pdf_file (string): the url of the pdf file
    """

    pdf_path = f"./assets/pdf/{file_name}.pdf"
    jpg_file = f"./assets/img/{file_name}.jpg"

    try:
        with Image(filename=pdf_path, resolution=300) as img:
            img.save(filename=jpg_file)
    except Exception as e:
        logging.error("pdf_to_jpeg: error")
        logging.error(f"pdf_to_jpeg: file_name {file_name}")
        logging.error(f"pdf_to_jpeg: \n{e}")
        return False

    logging.info(f"pdf_to_jpeg: success | {jpg_file}")
    return True


def get_data(json_file):
    """Open a json file and return the data

    Args:
        json_file (string): The path to the json data

    Returns:
        array: and array of json objects
    """

    try:
        with open(json_file, "r") as f:
            return json.load(f)
    except Exception as e:
        logging.error("get_data: Failed")
        logging.error(f"get_data: {e}")


def get_pdf_file(file_name, pdf_file):
    """Download a pdf file from an s3 link

    Args:
        pdf_file (string): The url of the pdf file
    """

    pdf_path = f"./assets/pdf/{file_name}.pdf"

    r = requests.get(url=pdf_file)

    try:
        with open(pdf_path, "wb") as f:
            f.write(r.content)
    except Exception as e:
        logging.error("get_pdf_file: Failed")
        logging.error(f"get_pdf_file: {e}")

    logging.info("get_pdf_file: success")


if __name__ == "__main__":
    json_file = "./assets/data.json"
    errors = []
    error_id = 0

    data = get_data(json_file=json_file)

    for i, file in enumerate(data):
        file_name = file["file_name"]
        pdf_file = file["s3_url"]

        get_pdf_file(file_name=file_name, pdf_file=pdf_file)

        copy_success = pdf_to_jpeg(file_name=file_name)

        # if there is an error, store the error
        if not copy_success:
            error = {"id": error_id, "file_name": file_name}
            errors.append(error)

            with open("./assets/errors.json", "w") as f:
                json.dump(errors, f, indent=4)

            error_id += 1

    logging.info(errors)
