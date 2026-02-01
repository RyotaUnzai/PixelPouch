from pathlib import Path

import pytest
from pixelpouch.libs.core.parsing.qss.loader import (
    QssLoader,
    QssLoaderError,
)


@pytest.fixture
def qss_root(tmp_path: Path) -> Path:
    return tmp_path


def test_simple_import(qss_root: Path) -> None:
    base = qss_root / "base.qss"
    main = qss_root / "main.qss"

    base.write_text("QWidget { color: red; }")
    main.write_text('@import url("base.qss");')

    loader = QssLoader(qss_root)
    result = loader.load(main)

    assert "color: red" in result


def test_missing_import_file(qss_root: Path) -> None:
    main = qss_root / "main.qss"
    main.write_text('@import url("missing.qss");')

    loader = QssLoader(qss_root)

    with pytest.raises(QssLoaderError):
        loader.load(main)


def test_path_traversal_is_blocked(qss_root: Path) -> None:
    outside = qss_root.parent / "evil.qss"
    outside.write_text("QWidget { color: black; }")

    main = qss_root / "main.qss"
    main.write_text('@import url("../evil.qss");')

    loader = QssLoader(qss_root)

    with pytest.raises(QssLoaderError):
        loader.load(main)


def test_root_variable_expansion(qss_root: Path) -> None:
    qss = qss_root / "style.qss"
    qss.write_text(
        """
        :root {
            --main-color: blue;
        }

        QWidget {
            color: var(--main-color);
        }
        """
    )

    loader = QssLoader(qss_root)
    result = loader.load(qss)

    assert "blue" in result
