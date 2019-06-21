class TestPages(object):

    """Ensure that root page requires user login."""
    def test_root_page(self, base_client):
        response = base_client.get('/')
        assert response.status_code == 302
        assert b"/login" in response.data

    """Ensure that the login page works correctly."""
    def test_login_page(self, base_client):
        response = base_client.get('/login')
        assert response.status_code == 200
        assert b"Login Form" in response.data

    """Ensure that the register page works correctly."""
    def test_register_page(self, base_client):
        response = base_client.get('/register')
        assert response.status_code == 200
        assert b"Create Account" in response.data

    """Ensure that the home page works correctly."""
    def test_home_page(self, base_client):
        response = base_client.get('/home')
        assert response.status_code == 200
        assert b"Home" in response.data

    """Ensure that the overview flask page works correctly."""
    def test_overview_flask_page(self, base_client):
        response = base_client.get('/overview-flask')
        assert response.status_code == 200
        assert b"Flask Overview" in response.data

    """Ensure that the overview docker page works correctly."""
    def test_overview_docker_page(self, base_client):
        response = base_client.get('/overview-docker')
        assert response.status_code == 200
        assert b"Docker Overview" in response.data

    """Ensure that the overview kubernetes page works correctly."""
    def test_overview_kubernetes_page(self, base_client):
        response = base_client.get('/overview-kubernetes')
        assert response.status_code == 200
        assert b"Kubernetes Overview" in response.data

    """Ensure that the overview sqlite page works correctly."""
    def test_overview_sqlite_page(self, base_client):
        response = base_client.get('/overview-sqlite')
        assert response.status_code == 200
        assert b"SQLite Commands and General Usage" in response.data

    """Ensure that the overview postgresql page works correctly."""
    def test_overview_postgresql_page(self, base_client):
        response = base_client.get('/overview-postgresql')
        assert response.status_code == 200
        assert b"PostgreSQL Overview" in response.data

    """Ensure that the overview ansible page works correctly."""
    def test_overview_ansible_page(self, base_client):
        response = base_client.get('/overview-ansible')
        assert response.status_code == 200
        assert b"Ansible Overview" in response.data

    """Ensure that the overview linux page works correctly."""
    def test_overview_linux_page(self, base_client):
        response = base_client.get('/overview-linux')
        assert response.status_code == 200
        assert b"Linux Overview" in response.data

    """Ensure that the overview python page works correctly."""
    def test_overview_python_page(self, base_client):
        response = base_client.get('/overview-python')
        assert response.status_code == 200
        assert b"Python Overview" in response.data
