"""A wrapper for DateRanges."""

from typing import Any, Dict, Optional, Union

from ee import apifunction
from ee import computedobject


class DateRange(computedobject.ComputedObject):
  """An object to represent an Earth Engine DateRange.

  Examples:
    ee.DateRange(1498287600000, 1498312800000)
    ee.DateRange('2017-06-24', '2017-07-24')
    ee.DateRange('2017-06-24', '2017-07-24', 'UTC')
    ee.DateRange('2017-06-24T07:00:00', '2017-07-24T07:00:00',
                 'America/Los_Angeles')

    now = ee.Date(datetime.datetime.utcnow())
    ee.DateRange(now.advance(-1, 'year'), now)

    ee.DateRange.unbounded()
  """

  _initialized: bool = False

  def __init__(
      self,
      start: Union[float, str, computedobject.ComputedObject],
      end: Optional[Union[float, str, computedobject.ComputedObject]] = None,
      # pylint: disable-next=invalid-name
      timeZone: Optional[Union[str, computedobject.ComputedObject]] = None,
  ):
    """Creates a DateRange wrapper.

    When the start and end arguments are numbers, they are millisec (ms) from
    1970-01-01T00:00.

    Args:
      start: Beginning of the DateRange (inclusive).
      end: Optional ending of the DateRange (exclusive). Defaults to start + 1
        ms.
      timeZone: If start and/or end are strings, the time zone in which to
        interpret them. Defaults to UTC.
    """
    self.initialize()

    if (
        isinstance(start, computedobject.ComputedObject)
        and end is None
        and timeZone is None
    ):
      if self.is_func_returning_same(start):
        # If it is a call that is already returning a DateRange, just cast.
        super().__init__(start.func, start.args, start.varName)
        return

    args: Dict[str, Any] = {'start': start}
    if end is not None:
      args['end'] = end
    if timeZone is not None:
      args['timeZone'] = timeZone

    func = apifunction.ApiFunction(self.name())
    super().__init__(func, func.promoteArgs(args))

  @classmethod
  def initialize(cls) -> None:
    """Imports API functions to this class."""
    if not cls._initialized:
      apifunction.ApiFunction.importApi(cls, cls.name(), cls.name())
      cls._initialized = True

  @classmethod
  def reset(cls) -> None:
    """Removes imported API functions from this class."""
    apifunction.ApiFunction.clearApi(cls)
    cls._initialized = False

  @staticmethod
  def name() -> str:
    return 'DateRange'
