from .models import (
    CounterModel,
    TotalQueryCountModel,
    AvgExecutionTimeModel,
    SleepModel,
    BackgroudJobModel,
)

Counter = CounterModel(0)
TotalQueryCount = TotalQueryCountModel(0)
AvgExecutionTime = AvgExecutionTimeModel(0.0)
Sleep = SleepModel(0.0)
BackgroundJobSaver = BackgroudJobModel()
