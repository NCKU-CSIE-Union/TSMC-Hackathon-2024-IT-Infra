from monitor.service.conversation_manager import ConversationManager, get_redis_setting
import pandas as pd


def test_conversation_manager_init():
    setting = get_redis_setting()
    assert setting is not None


def test_conversation_manager(conversation_manager: ConversationManager) -> None:
    manager = conversation_manager
    assert manager is not None


def test_conversation_manager_new_conversation(
    conversation_manager: ConversationManager,
) -> None:
    manager = conversation_manager
    df = pd.DataFrame()
    df["test"] = [1, 2, 3]
    manager.new_conversation("test-thread-id", df)

    result_json = manager.get_conversation("test-thread-id")
    assert result_json is not None


def test_conversation_manager_get_conversation(
    conversation_manager: ConversationManager,
) -> None:
    manager = conversation_manager
    result_json = manager.get_conversation("test-thread-id")

    assert result_json is not None
    assert result_json["log"] is not None
    assert result_json["feedbacks"] is not None
    assert result_json["user_messages"] is not None


def test_conversation_manager_update_conversation_feedbacks(
    conversation_manager: ConversationManager,
) -> None:
    manager = conversation_manager
    manager.update_conversation_feedbacks("test-thread-id", "test-feedbacks")

    result_json = manager.get_conversation("test-thread-id")
    assert result_json["feedbacks"] is not None


def test_conversation_manager_update_conversation_user_messages(
    conversation_manager: ConversationManager,
) -> None:
    manager = conversation_manager
    manager.update_conversation_user_messages("test-thread-id", "test-user-messages")

    result_json = manager.get_conversation("test-thread-id")
    assert result_json["user_messages"] is not None
