from app.utils import formatar_moeda


def test_formatar_moeda_com_decimal():
    input = 60.9
    output = formatar_moeda(input)
    assert output == "60,90"


def test_formatar_moeda_int():
    assert formatar_moeda(45) == "45,00"


def test_formatar_moeda_zero():
    assert formatar_moeda(0) == "0,00"
