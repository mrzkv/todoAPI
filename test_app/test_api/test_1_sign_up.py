import pytest
from httpx import AsyncClient, ASGITransport
from src.main import app


@pytest.mark.asyncio
async def test_sign_up_correct_and_conflict():
    correct_registration_content = {
        'status': 'ok',
        'message': 'account registered'
    }
    async with AsyncClient(
            transport=ASGITransport(app=app),
            base_url="http://test") as ac:
        # Correct user registration
        first_response = await ac.post(
            url='/v1/api/auth/sign-up',
            json=dict(login='CorrectLogin', password='CorrectPassword555!')
        )
        assert first_response.status_code == 201
        first_data = first_response.json()
        assert first_data == correct_registration_content
        second_response = await ac.post(
            url='/v1/api/auth/sign-up',
            json=dict(login='SuperUserRoot', password='KorReCTPWD1234@#')
        )
        assert second_response.status_code == 201
        second_data = second_response.json()
        assert second_data == correct_registration_content
        third_response = await ac.post(
            url='/v1/api/auth/sign-up',
            json=dict(login='marzkv', password='ThisIsCorrectPassword!1901')
        )
        assert third_response.status_code == 201
        third_data = third_response.json()
        assert third_data == correct_registration_content

        # Conflict user registration
        first_response = await ac.post(
            url='/v1/api/auth/sign-up',
            json=dict(login='CorrectLogin', password='CorrectPassword555!')
        )
        assert first_response.status_code == 409
        second_response = await ac.post(
            url='/v1/api/auth/sign-up',
            json=dict(login='SuperUserRoot', password='KorReCTPWD1234@#')
        )
        assert second_response.status_code == 409
        third_response = await ac.post(
            url='/v1/api/auth/sign-up',
            json=dict(login='marzkv', password='ThisIsCorrectPassword!1901')
        )
        assert third_response.status_code == 409

