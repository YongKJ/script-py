import concurrent.futures
import os


class ThreadUtil:

    @staticmethod
    def parallelism():
        n = (os.cpu_count() or 1) * 2
        return max(8, min(64, n))

    @staticmethod
    def executeWithListDataByThreadPool(await_minutes, lst_data, function):
        """并行处理列表元素，等待全部完成或超时；任一元素抛异常则向上抛首个异常。

        对应 Java 版 ThreadUtil.executeWithListDataByThreadPool(long, List<T>, Consumer<T>)。
        """
        if not lst_data:
            return
        executor = concurrent.futures.ThreadPoolExecutor(max_workers=ThreadUtil.parallelism())
        try:
            futures = [executor.submit(function, data) for data in lst_data]
            done, not_done = concurrent.futures.wait(futures, timeout=await_minutes * 60)
            if not_done:
                raise RuntimeError("多线程执行超时（超过 %d 分钟）" % await_minutes)
            for future in futures:
                future.result()  # 抛出首个任务异常
        finally:
            executor.shutdown(wait=False)

    @staticmethod
    def executeWithMapDataByThreadPool(await_minutes, map_data, function):
        """并行处理字典元素，等待全部完成或超时；任一元素抛异常则向上抛首个异常。

        对应 Java 版 ThreadUtil.executeWithMapDataByThreadPool(long, Map<K,V>, BiConsumer<K,V>)。
        """
        if not map_data:
            return
        executor = concurrent.futures.ThreadPoolExecutor(max_workers=ThreadUtil.parallelism())
        try:
            futures = [executor.submit(function, key, value) for key, value in map_data.items()]
            done, not_done = concurrent.futures.wait(futures, timeout=await_minutes * 60)
            if not_done:
                raise RuntimeError("多线程执行超时（超过 %d 分钟）" % await_minutes)
            for future in futures:
                future.result()
        finally:
            executor.shutdown(wait=False)
