import os

import pytest

from g2w import Ws

given = pytest.mark.parametrize


@pytest.mark.skipif(os.getenv("WS_URL_ALL_USERS") is None, reason="Environment variable 'WS_URL_ALL_USERS' is absent")
def test_users():
    assert len(Ws().all_users()) > 20


@pytest.mark.skipif(os.getenv("WS_EMAIL") is None, reason="Email account for worksection is absent")
@pytest.mark.skipif(os.getenv("WS_URL_POST_COMMENT") is None, reason="Environment variable 'WS_URL_POST_COMMENT' is absent")
def test_add_comment():
    assert (
        Ws().add_comment(
            223728,
            6231285,
            "%3Ca%20href%3D%22https%3A%2F%2Fgitlab.myown.com.ua%2Ffront-myown%2Ffront-site%2F-%2Fcommit%2Fa68fef399f828059e2c532ede70ca5ab84ee71e7%22%3E2%20new%20commits%3C%2Fa%3E%26nbsp%3Bpushed%20to%20%3Cb%20style%3D%22background%3A%20rgb%28196%2C%20255%2C%20166%29%22%3E%3Ca%20href%3D%22https%3A%2F%2Fff%22%3Edevelop%3C%2Fa%3E%26ZeroWidthSpace%3B%3C%2Fb%3E%26ZeroWidthSpace%3B%26ZeroWidthSpace%3B%20by%26nbsp%3B%3Cspan%20class%3D%22invite%20invite_old%22%20rel%3D%22252468%22%20spellcheck%3D%22false%22%20contenteditable%3D%22false%22%3E%D0%9C%D0%B0%D0%B6%D0%B0%D1%80%D0%B5%D0%BD%D0%BA%D0%BE%20%D0%A1%D1%82%D0%B0%D0%BD%D0%B8%D1%81%D0%BB%D0%B0%D0%B2%3C%2Fspan%3E%26nbsp%3B%3Cbr%3E%3Cul%3E%3Cli%3E%3Ca%20href%3D%22https%3A%2F%2Fgitlab.myown.com.ua%2Ffront-myown%2Ffront-site%2F-%2Fcommit%2Fa68fef399f828059e2c532ede70ca5ab84ee71e7%22%3Eeb3fdffb%3C%2Fa%3E%26nbsp%3B-%26nbsp%3BUpdate%20README.md%26ZeroWidthSpace%3B%3C%2Fli%3E%3Cli%3E%3Ca%20href%3D%22https%3A%2F%2Fgitlab.myown.com.ua%2Ffront-myown%2Ffront-site%2F-%2Fcommit%2F156af0d58832810fe79378c13d78c458a115aa8d%22%3E156af0d5%3C%2Fa%3E%26nbsp%3B-%26nbsp%3BAdded%20a%20new%20line%20just%20to%20trigger%20new%20Gilab%20CI%20runner%20hosted%20in%20myown%20network%26ZeroWidthSpace%3B%3C%2Fli%3E%3C%2Ful%3E",
        )["id"]
        is not None
    )
