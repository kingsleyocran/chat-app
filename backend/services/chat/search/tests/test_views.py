"""Test for all Views
"""
from unittest.mock import patch

import pytest
from django.urls import reverse
from rest_framework.test import APITestCase


class TestViews(APITestCase):
    """Test View Class"""

    @pytest.mark.search
    def test_search_view(self) -> None:
        """Test Search View"""
        with patch("search.views.es") as mock_elastic:
            mock_elastic.search.return_value = {
                "hits": {"hits": [{"_source": {"USERNAME": "fiopapa"}}]}
            }
            response = self.client.get(reverse("search", args=("fiopapa",)))
            assert response.json() == [{"USERNAME": "fiopapa"}]
            assert response.status_code == 200

    @pytest.mark.search
    def test_all_users_view(self) -> None:
        """Test All users View"""
        with patch("search.views.es") as mock_elastic:
            mock_elastic.search.return_value = {
                "hits": {"hits": [{"_source": {"USERNAME": "fiopapa"}}]}
            }
            response = self.client.get(reverse("users"))
            assert response.json() == [{"USERNAME": "fiopapa"}]
            assert response.status_code == 200
