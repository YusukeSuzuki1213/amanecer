from abc import ABCMeta, abstractmethod
from entity.params.get_dmm_items_params import GetDmmItemsParams
from entity.failure import Failure
from entity.item import Item
from datasource.remote.dmm_api_client import DmmApiClient
from typing import List, Union
from traceback import format_exc
from mapper.get_items_success_mapper import GetItemsSuccessMapper


class AbstractDmmRepository(metaclass=ABCMeta):
    @abstractmethod
    def get_items(self, params: GetDmmItemsParams) -> Union[List[Item], Failure]:
        pass


class DmmRepository(AbstractDmmRepository):
    def __init__(self, api_client: DmmApiClient) -> None:
        self.api_client = api_client

    def get_items(self, params: GetDmmItemsParams) -> Union[List[Item], Failure]:
        try:
            response = self.api_client.get_items(params)
            return GetItemsSuccessMapper.to_entity(response)

        except Exception:
            return Failure("dmm apiリクエスト中にエラー", format_exc())
