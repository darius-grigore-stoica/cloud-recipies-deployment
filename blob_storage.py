"""
blob_storage.py — Handles all image uploads to Azure Blob Storage.
Think of this like uploading to Google Drive, but from code.
"""
import os
import uuid
from azure.storage.blob import BlobServiceClient, ContentSettings
from dotenv import load_dotenv

load_dotenv()

CONNECTION_STRING = os.getenv("AZURE_STORAGE_CONNECTION_STRING")
CONTAINER_NAME    = os.getenv("AZURE_STORAGE_CONTAINER", "recipe-images")


def get_blob_client():
    """Create a connection to Azure Blob Storage."""
    return BlobServiceClient.from_connection_string(CONNECTION_STRING)


def upload_image(file_bytes: bytes, filename: str, content_type: str) -> str:
    """
    Upload an image to Azure Blob Storage.
    Returns the public URL of the uploaded image.
    """
    # Give the file a unique name so uploads never overwrite each other
    ext = filename.rsplit(".", 1)[-1] if "." in filename else "jpg"
    unique_name = f"{uuid.uuid4()}.{ext}"

    blob_client = get_blob_client()

    # Make sure the container exists (creates it if not)
    container = blob_client.get_container_client(CONTAINER_NAME)
    try:
        container.get_container_properties()
    except Exception:
        container.create_container(public_access="blob")  # public so images load in browser

    # Upload the file
    blob = container.get_blob_client(unique_name)
    blob.upload_blob(
        file_bytes,
        overwrite=True,
        content_settings=ContentSettings(content_type=content_type),
    )

    # Return the public URL
    account_name = blob_client.account_name
    return f"https://{account_name}.blob.core.windows.net/{CONTAINER_NAME}/{unique_name}"


def delete_image(image_url: str):
    """Delete an image from Blob Storage given its URL."""
    if not image_url:
        return
    blob_name = image_url.split("/")[-1]
    blob_client = get_blob_client()
    container  = blob_client.get_container_client(CONTAINER_NAME)
    try:
        container.get_blob_client(blob_name).delete_blob()
    except Exception:
        pass  # if it doesn't exist, that's fine
