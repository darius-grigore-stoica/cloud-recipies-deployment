import os
import uuid
from azure.storage.blob import BlobServiceClient, ContentSettings
from dotenv import load_dotenv

load_dotenv()

CONNECTION_STRING = os.getenv("AZURE_STORAGE_CONNECTION_STRING")
CONTAINER_NAME    = os.getenv("AZURE_STORAGE_CONTAINER", "recipe-images")


def get_blob_client():
    return BlobServiceClient.from_connection_string(CONNECTION_STRING)


def upload_image(file_bytes: bytes, filename: str, content_type: str) -> str:
    ext = filename.rsplit(".", 1)[-1] if "." in filename else "jpg"
    unique_name = f"{uuid.uuid4()}.{ext}"

    blob_client = get_blob_client()
    container = blob_client.get_container_client(CONTAINER_NAME)

    blob = container.get_blob_client(unique_name)
    blob.upload_blob(
        file_bytes,
        overwrite=True,
        content_settings=ContentSettings(content_type=content_type),
    )

    account_name = blob_client.account_name
    return f"https://{account_name}.blob.core.windows.net/{CONTAINER_NAME}/{unique_name}"


def delete_image(image_url: str):
    if not image_url:
        return
    blob_name = image_url.split("/")[-1]
    blob_client = get_blob_client()
    container = blob_client.get_container_client(CONTAINER_NAME)
    try:
        container.get_blob_client(blob_name).delete_blob()
    except Exception:
        pass