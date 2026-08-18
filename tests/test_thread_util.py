from script_py.util.ThreadUtil import ThreadUtil


def test_execute_with_list_data():
    lst = list(range(100))
    result = []
    ThreadUtil.executeWithListDataByThreadPool(1, lst, result.append)
    assert sum(result) == 4950


def test_execute_with_list_data_propagates_error():
    lst = list(range(50))

    def fn(v):
        if v == 25:
            raise RuntimeError("boom")

    try:
        ThreadUtil.executeWithListDataByThreadPool(1, lst, fn)
        assert False, "应当抛出异常"
    except RuntimeError as e:
        assert str(e) == "boom"


def test_execute_with_map_data():
    m = {str(i): i for i in range(100)}
    result = []
    ThreadUtil.executeWithMapDataByThreadPool(1, m, lambda k, v: result.append(v))
    assert len(result) == 100
    assert sum(result) == 4950
