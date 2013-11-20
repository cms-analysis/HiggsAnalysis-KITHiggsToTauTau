#!/usr/bin/env python
# -*- coding: utf-8 -*-

import logging


# function that provides a logger that should be used by every python script
# see http://docs.python.org/2/library/logging.html for more info
def getLogger(argParser=None, name=""):

	logLevel = "debug"

	if argParser:
		argParser.add_argument("--log-level", default="debug",
			                   choices=["debug", "info", "warning", "error", "critical"],
			                   help="Log level. [Default: debug]")
		args = argParser.parse_args()
		logLevel = args.log_level

	logging.basicConfig(level=getattr(logging, logLevel.upper()),
	                    format="%(levelname)s: %(message)s")

	return logging.getLogger(name)

