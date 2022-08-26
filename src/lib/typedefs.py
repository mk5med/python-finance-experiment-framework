import typing
TransactionTypeDef = typing.Tuple[typing.Union[int, float], typing.Union[int, float]]
TransactionListTypeDef = typing.Sequence[TransactionTypeDef]
ShareGroupChainTypeDef = typing.List[
    typing.Tuple[str, TransactionTypeDef, TransactionListTypeDef]
]