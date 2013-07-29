#!/usr/bin/env python
import sys

import syncomatic
from syncomatic import app
from syncomatic.models import User

if __name__ == '__main__':
    # Reset the database only if we run with --initdb.
    if (len(sys.argv) > 1 and sys.argv[1] == '--initdb'):
        User.initdb()

    app.run(host='0.0.0.0')
