from decimal import ROUND_HALF_EVEN, ROUND_HALF_UP, Decimal

CENT = Decimal("0.01")


def round_half_up(amount: Decimal) -> Decimal:

    """

    Rounds an amount to whole cents, breaking ties away from zero.


    Parameters
    ----------
    amount : Decimal
        The exact amount to round.


    Returns
    -------
    Decimal
        The amount quantized to two decimal places, with a half cent
        rounded to the larger magnitude.


    Raises
    ------
    None.

    """

    return amount.quantize(CENT, rounding=ROUND_HALF_UP)


def round_half_even(amount: Decimal) -> Decimal:

    """

    Rounds an amount to whole cents, breaking ties toward the even cent.


    Parameters
    ----------
    amount : Decimal
        The exact amount to round.


    Returns
    -------
    Decimal
        The amount quantized to two decimal places, with a half cent
        rounded to the neighbour whose final digit is even.


    Raises
    ------
    None.

    """

    return amount.quantize(CENT, rounding=ROUND_HALF_EVEN)


def is_tie(amount: Decimal) -> bool:

    """

    Reports whether an amount sits exactly halfway between two cents.


    Parameters
    ----------
    amount : Decimal
        The exact amount to inspect.


    Returns
    -------
    holds_tie : bool
        True when the amount's remainder past whole cents is exactly
        half a cent, which is the only case where the two strategies
        disagree.


    Raises
    ------
    None.

    """

    return (amount * 100) % 1 == Decimal("0.5")
