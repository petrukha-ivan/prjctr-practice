import time
import numpy as np
from concurrent.futures import wait, ProcessPoolExecutor, ThreadPoolExecutor
from dask.distributed import Client
import ray
from utils import time_profile


class Model:
    def predict(self, batch):
        return [(time.sleep(0.0001), 0)[1] for _ in batch]


def batch_generator(inputs, batch_size=128):
    for i in range(0, len(inputs), batch_size):
        yield inputs[i:i + batch_size]


def test_naive_inference(corpus, model):
    with time_profile('Naive inference'):
        return [model.predict(batch) for batch in batch_generator(corpus)]


def test_process_pool_inference(corpus, model):
    with time_profile('Process pool inference'):
        with ProcessPoolExecutor() as executor:
            futures = wait([executor.submit(model.predict, batch) for batch in batch_generator(corpus)]).done
            results = [future.result() for future in futures]
            return results
            

def test_thread_pool_inference(corpus, model):
    with time_profile('Thread pool inference'):
        with ThreadPoolExecutor() as executor:
            futures = wait([executor.submit(model.predict, batch) for batch in batch_generator(corpus)]).done
            results = [future.result() for future in futures]
            return results


def test_dusk_inference(corpus, model):
    client = Client()
    with time_profile('Dusk inference'):
        futures = [client.submit(model.predict, batch) for batch in batch_generator(corpus)]
        results = client.gather(futures)
        return results


def test_ray_inference(corpus, model):
    @ray.remote
    def predict_ray(batch):
        return model.predict(batch)
    
    with time_profile('Ray inference'):
        futures = [predict_ray.remote(batch) for batch in batch_generator(corpus)]
        results = ray.get(futures)
        return results


def main():
    model = Model()
    corpus = np.repeat(0, 100_000)
    test_naive_inference(corpus, model)
    test_process_pool_inference(corpus, model)
    test_thread_pool_inference(corpus, model)
    test_dusk_inference(corpus, model)
    test_ray_inference(corpus, model)


if __name__ == '__main__':
    main()