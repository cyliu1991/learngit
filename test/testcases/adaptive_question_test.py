import logging
LOG = logging.getLogger(__name__)
import requests
import time
import json
import numpy as np


def _test_adaptive_question_backend():
    """
    测试出题接口
    """
    unit_list = ["5.1.02", "1.1.05", "5.2.01", "1.1.04", "4.2.01", "4.2.03"]
    url = f"http://127.0.0.1:{PORT}/api/realTimeCompute/createNextQuestion"
    for unit in unit_list:
        request_json_dict = {
            "parameters": {
                "student_id": "0101010011201001",
                "textbook_id": "A1",
                "unit_id": unit,
                "question_list": [
                    {"is_right": "", "question_id": ""}
                ]
            }
        }

        result_rate_len = 0
        i = 0
        while i < 15:

            LOG.info("request with json %s", json.dumps(request_json_dict))
            beg_time = time.time()
            res = requests.post(url, json=json.dumps(request_json_dict))
            LOG.info("[total] %s", time.time() - beg_time)

            # 请求正常返回
            assert res.status_code == 200

            # 接口运行正常
            post_result = json.loads(res.content)
            LOG.info("receive %s", post_result)
            assert post_result["code"] == 10000

            # 每次得到的掌握程度都比上一次要多（至少数量一样）
            result_rate = [
                (item["point_id"], item["rate"])
                for item in post_result["point_list"]
            ]
            assert len(result_rate) >= result_rate_len
            result_rate_len = len(result_rate)
            LOG.info("[mastery result] %s", result_rate)

            question_next = post_result["question_list"][0]["question_id"]
            if question_next == "":
                break
            request_json_dict["parameters"]["question_list"][0][
                "question_id"] = question_next
            request_json_dict["parameters"]["question_list"][0][
                "is_right"] = np.random.choice(
                ["true", "false"],
                p=[0.8, 0.2])
            i += 1

        # 结束出题时，做题数量小于等于12(终止条件是否有效)
        assert i <= 12

