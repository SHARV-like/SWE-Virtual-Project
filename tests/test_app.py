import pytest
from dash.testing.application_runners import import_app


# Load your Dash app
@pytest.fixture
def app():
    return import_app("app")  # make sure your file is app.py


# 1️⃣ Test Header Presence
def test_header_present(dash_duo, app):
    dash_duo.start_server(app)

    header = dash_duo.find_element("h1")
    assert header is not None
    assert "Soul Foods Sales Dashboard" in header.text


# 2️⃣ Test Graph Presence
def test_graph_present(dash_duo, app):
    dash_duo.start_server(app)

    graph = dash_duo.find_element("#sales-graph")
    assert graph is not None


# 3️⃣ Test Region Picker Presence
def test_region_picker_present(dash_duo, app):
    dash_duo.start_server(app)

    region_picker = dash_duo.find_element("#region-filter")
    assert region_picker is not None