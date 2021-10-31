from entity.params.get_dmm_items_params import GetDmmItemsParams
from typing import Any, Dict
import requests


class DmmApiClient(object):
    def _request(self, params: Dict[str, str], url: str) -> Dict[str, Any]:
        response = requests.get(url, params=params)
        response.raise_for_status()
        return response.json()

    def get_items(self, params: GetDmmItemsParams) -> Dict[str, Any]:
        return self._request(
            # TODO: paramsクラスを直でasdictできるように。
            # paramsを追加したのにここの実装を忘れることがあるため
            params={
                'api_id': params.api_id,
                'affiliate_id': params.affiliate_id,
                'site': params.site,
                'service': params.service,
                'floor': params.floor,
                'hits': params.hits,
                'sort': params.sort,
                'cid': params.cid,
                'article': params.article,
                'article_id': params.article_id,
                'gte_date': params.gte_date,
                'lte_date': params.lte_date,
                'output': params.output,
            },
            url=params.url
        )
