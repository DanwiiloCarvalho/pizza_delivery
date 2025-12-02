from enum import Enum


class OrderStatusEnum(str, Enum):
    PENDING = 'PENDENTE'
    CANCELED = 'CANCELADO'
    COMPLETED = 'FINALIZADO'
