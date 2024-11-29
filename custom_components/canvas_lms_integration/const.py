"""Constants for integration_blueprint."""

from logging import Logger, getLogger

LOGGER: Logger = getLogger(__package__)

DOMAIN = "canvas_lms"
ATTRIBUTION = "Data provided by http://jsonplaceholder.typicode.com/"
CONF_OBSERVEES = "observees"
CONF_OBSERVEE = "observee"
CONF_CANVAS_URL = "canvas_url"
CONF_COURSES = "courses"

NAME = "Canvas LMS"
VERSION = "0.0.1"
# Sensors
MissingAssignments = "missing_assignments"
Courses = "courses"
