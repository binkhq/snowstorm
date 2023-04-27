import pendulum
from loguru import logger
from sqlalchemy.orm import Session

from snowstorm.database import APIStats, Events, FreshService, engine


class Job_DatabaseCleanup:
    def __init__(self, days: int) -> None:
        self.days = days

    def cleanup(self) -> None:
        delta = pendulum.today().subtract(days=self.days)
        with Session(engine) as session:
            apistats = session.query(APIStats).filter(APIStats.date_time <= delta)
            logger.warning("apistats records found", extra={"record_count": apistats.count()})
            apistats.delete()

            freshservice = session.query(FreshService).filter(FreshService.updated_at <= delta)
            logger.warning("freshservice records found", extra={"record_count": freshservice.count()})
            freshservice.delete

            events = session.query(Events).filter(Events.event_date_time <= delta)
            logger.warning("events records found", extra={"record_count": events.count()})
            events.delete()

            session.commit()
