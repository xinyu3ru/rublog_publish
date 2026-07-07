import asyncio
import logging
from typing import Optional, Dict, Any, Tuple
from urllib.parse import urlparse, ParseResult

import aiohttp

from lib.api import WordpressEndpoint, User, Post, Medium


class AsyncWordpress:
    def __init__(self, endpoint: WordpressEndpoint):
        self.endpoint = endpoint
        self.session: Optional[aiohttp.ClientSession] = None
        self._users_by_id: Dict[str, User] = {}
        self._media: Dict[str, Medium] = {}

    @property
    def auth(self) -> Tuple[str, str]:
        return (self.endpoint.username, self.endpoint.password)

    @property
    def basic_auth_header(self) -> str:
        import base64
        credentials = f"{self.endpoint.username}:{self.endpoint.password}"
        return f"Basic {base64.b64encode(credentials.encode()).decode()}"

    @property
    def url(self) -> str:
        return self.endpoint.url

    def normalize_url(self, url: str) -> str:
        return self.endpoint.normalize_url(url)

    async def _request_with_retry(self, method: str, url: str, **kwargs) -> aiohttp.ClientResponse:
        auth = kwargs.pop('auth', self.auth)
        headers = kwargs.pop('headers', {})
        
        async with self.session.request(method, url, auth=auth, headers=headers, **kwargs) as response:
            if response.status == 401 and auth is not None:
                headers_with_auth = headers.copy()
                headers_with_auth["Authorization"] = self.basic_auth_header
                async with self.session.request(method, url, headers=headers_with_auth, **kwargs) as retry_response:
                    return retry_response
            return response

    async def create_tag(self, name: str) -> int:
        response = await self._request_with_retry("POST", f"{self.url}/tags", json={"name": name})
        
        if response.status in [200, 201]:
            tag_data = await response.json()
            return tag_data["id"]
        
        raise Exception(f"Failed to create tag '{name}': {await response.text()}")

    async def upload_media(self, slug: str, content: bytes, filename: str, content_type: str) -> Medium:
        headers = {
            "Content-Disposition": f'attachment; filename="{filename}"',
            "Content-Type": content_type,
        }

        response = await self._request_with_retry(
            "POST",
            f"{self.url}/media/",
            data=content,
            headers=headers,
            params={"slug": slug, "title": slug},
        )
        
        if response.status in [200, 201]:
            return Medium(await response.json())
        
        raise Exception(f"Failed to upload media '{slug}': {await response.text()}")

    async def create_post(self, properties: dict) -> Post:
        response = await self._request_with_retry("POST", f"{self.url}/posts", json=properties)
        
        if response.status in [200, 201]:
            return Post(await response.json())
        
        raise Exception(f"Failed to create post: {await response.text()}")

    async def update_post(self, guid: str, properties: dict) -> Post:
        response = await self._request_with_retry("PATCH", self.normalize_url(guid), json=properties)
        
        if response.status in [200, 201]:
            return Post(await response.json())
        
        raise Exception(f"Failed to update post: {await response.text()}")

    async def __aenter__(self):
        self.session = aiohttp.ClientSession()
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        if self.session:
            await self.session.close()
