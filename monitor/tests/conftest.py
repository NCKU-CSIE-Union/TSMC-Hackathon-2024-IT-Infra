import pytest
from monitor.service.cloudrun import CloudRunManager
from monitor.service.conversation_manager import ConversationManager


@pytest.fixture(scope="class")
def cloud_run_manager():
    return CloudRunManager()


@pytest.fixture(scope="class")
def conversation_manager():
    return ConversationManager()
