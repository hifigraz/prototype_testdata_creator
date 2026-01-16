import os

from pytest import CaptureFixture

from testdata_creator import utils


# This Test will fail
def test_00(capfd: CaptureFixture[str]):
    utils.test()
    out, err = capfd.readouterr()
    assert "This is a test!" + os.linesep == out
    assert "" == err
