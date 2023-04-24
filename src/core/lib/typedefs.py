import typing
from datetime import datetime

TransactionTypeDef = typing.Tuple[
    # Price
    typing.Union[int, float],
    # Qty
    typing.Union[int, float],
]
TransactionListTypeDef = typing.Sequence[TransactionTypeDef]
ShareGroupChainTypeDef = typing.List[
    typing.Union[
        typing.Tuple[
            typing.Literal["buy"],
            TransactionTypeDef,
            # Transaction date
            datetime,
        ],
        typing.Tuple[
            typing.Literal["sell"],
            TransactionTypeDef,
            # Transaction date
            datetime,
        ],
    ]
]
