import typing

TransactionTypeDef = typing.Tuple[typing.Union[int, float], typing.Union[int, float]]
TransactionListTypeDef = typing.Sequence[TransactionTypeDef]
ShareGroupChainTypeDef = typing.List[
    typing.Union[
        typing.Tuple[typing.Literal["buy"], TransactionTypeDef],
        typing.Tuple[
            typing.Literal["sell"], TransactionTypeDef, TransactionListTypeDef
        ],
    ]
]
