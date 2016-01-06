__author__ = 'niznik'

# ClickHistDo is very much specific to the implementation of ClickHist
# As an example, here is a blank ClickHistDo that tells the user that
# it will do nothing as the "hint" provided after an initial click
# (In the IDV implementation, this message is 'save IDV bundle'
#
# The do method is where all of the scripting should occur - see
# the IDV implementation for one such example

class ClickHistDo:
    def __init__(self):
        """
        Initialize the ClickHistDo
        :return:
        """
        self.doObjectHint = 'do nothing - default empty ClickHistDo...'
        return

    def do(self):
        """
        Performs the desired functionality based on the input from ClickHist
        :return:
        """
        print('Doing nothing - default empty ClickHistDo...')
        return

