from google.cloud import storage
import tempfile


class GCS:
    def __init__(self, bucket_name: str, verbose: bool = True):
        self.bucket_name = bucket_name
        self.client = storage.Client()
        self.bucket = self.client.bucket(bucket_name)
        self.verbose = verbose

    def upload_blob_from_file(self, content, destination_blob_name,
                              content_type="application/octet-stream"):
        """Uploads a file to the bucket."""
        blob = self.bucket.blob(destination_blob_name)

        with tempfile.TemporaryFile() as fp:
            fp.write(content)
            fp.seek(0)
            blob.upload_from_file(fp, content_type=content_type)

            if self.verbose:
                print(
                    f"File uploaded to {destination_blob_name}."
                )

    def download_blob_into_memory(self, blob_name):
        """Downloads a blob into memory."""
        blob = self.bucket.blob(blob_name)
        contents = blob.download_as_bytes()

        if self.verbose:
            print(
                "Downloaded storage object {} from bucket {}.".format(
                    blob_name, self.bucket_name
                )
            )
        return contents

    def blob_exists(self, blob_name):
        blob = self.bucket.blob(blob_name)
        return blob.exists()
