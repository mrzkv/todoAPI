import pytest
from httpx import AsyncClient, ASGITransport
from src.app_services.security import get_token
from src.main import app


@pytest.mark.asyncio
async def test_sign_in_correct_and_conflict():
    async with AsyncClient(
            transport=ASGITransport(app=app),
            base_url='http://test') as ac:
        first_response = await ac.post(
            url='/v1/api/auth/sign-in',
            json=dict(login='CorrectLogin', password='CorrectPassword555!')
        )
        second_response = await ac.post(
            url='/v1/api/auth/sign-in',
            json=dict(login='SuperUserRoot', password='KorReCTPWD1234@#')
        )
        third_response = await ac.post(
            url='/v1/api/auth/sign-in',
            json=dict(login='marzkv', password='ThisIsCorrectPassword!1901')
        )
        assert first_response.status_code == 200
        assert second_response.status_code == 200
        assert third_response.status_code == 200

        first_data, second_data, third_data = first_response.json(), second_response.json(), third_response.json()

        assert first_data == {
            'access_token': await get_token('CorrectLogin')
        }
        assert second_data == {
            'access_token': await get_token('SuperUserRoot')
        }
        assert third_data == {
            'access_token': await get_token('marzkv')
        }
