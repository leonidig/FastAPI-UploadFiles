import os

from unittest import TestCase, main as main_test
from fastapi.testclient import TestClient

from backend import app


class TestBackend(TestCase):
    def setUp(self) -> None:
        self.client = TestClient(app)


    def test_url_parse_endpoint(self):
        response = self.client.get("/image/")
        self.assertEqual(response.status_code, 200)


    def test_upload_photo(self):
        with open("mock_image_for_test.jpg", "rb") as file:
            response = self.client.post(
                "/image/upload/",
                files={"image": ("mock_image_for_test.jpg", file, "image/jpeg")},
                data={"author": "leonid", "gallery": "test"}
)

        self.assertEqual(response.status_code, 201)


    def test_upload_invalid_file_format(self):
        with open("README.md", "rb") as file:
            response = self.client.post(
                "/image/upload/",
                files={"images": ("README.md", file, "application/octet-stream")},
                data={"author": "leonid", "gallery": "test"}  
            )
        self.assertEqual(response.status_code, 415)


if __name__ == "__main__":
    main_test()
