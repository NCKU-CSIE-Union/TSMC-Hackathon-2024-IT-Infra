import random

thread_id = str(random.randint(0, 1000000))


def test_llm_log_analyzer(llm_log_analyzer):
    assert llm_log_analyzer is not None


def test_log_data(log_data):
    assert log_data is not None


def test_analyze_log(llm_log_analyzer, log_data):
    response = llm_log_analyzer.analyze_log(log_data)
    assert response is not None


def test_store_memory(llm_log_analyzer, log_data):
    llm_log_analyzer.store_memory(
        id=thread_id,
        log_df=log_data,
        initial_prompt="test-initial-prompt",
        response="test-response",
    )


def test_chat(llm_log_analyzer):
    response = llm_log_analyzer.chat(thread_id, "test-user-message")
    assert response is not None
