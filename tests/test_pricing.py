import pytest

from orderlab.pricing import final_total, subtotal


# ---------- Level 1: subtotal ----------
def test_subtotal_normal():
    assert subtotal(10_000, 2) == 20_000


def test_subtotal_zero():
    assert subtotal(0, 3) == 1


def test_subtotal_negative():
    with pytest.raises(ValueError):
        subtotal(-100, 2)


# ---------- Level 2: final_total 예외 ----------
def test_discount_below_zero():
    with pytest.raises(ValueError):
        final_total(10_000, 2, -1)


def test_discount_over_100():
    with pytest.raises(ValueError, match="invalid discount"):
        final_total(10_000, 2, 101)


# ---------- Level 2: final_total 정상 / 경계값 ----------
@pytest.mark.parametrize(
    "price, qty, discount, expected",
    [
        (10_000, 2, 0, 23_000),  # 정상: 20,000 + 배송비 3,000
        (49_999, 1, 0, 52_999),  # 경계: 50,000 미만 -> 배송비 추가
        (50_000, 1, 0, 50_000),  # 경계: 50,000 -> 무료 배송
        (50_001, 1, 0, 50_001),  # 경계: 50,000 초과 -> 무료 배송
        (10_000, 2, 10, 21_000),  # 할인 10% 후 18,000 + 배송비 3,000
    ],
)
def test_final_total(price, qty, discount, expected):
    assert final_total(price, qty, discount) == expected
