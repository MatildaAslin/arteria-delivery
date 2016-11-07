
from sqlalchemy import Column, Integer, String, Enum
import enum as base_enum


from sqlalchemy.ext.declarative import declarative_base

SQLAlchemyBase = declarative_base()


class StagingStatus(base_enum.Enum):

    pending = 'pending'

    staging_in_progress = 'staging_in_progress'
    staging_successful = 'staging_successful'
    staging_failed = 'staging_failed'


class StagingOrder(SQLAlchemyBase):

    __tablename__ = 'staging_orders'

    id = Column(Integer, primary_key=True, autoincrement=True)
    source = Column(String, nullable=False)
    status = Column(Enum(StagingStatus), nullable=False)
    staging_target = Column(String)
    pid = Column(Integer)

    def __repr__(self):
        return "Staging order: {id: %s, source: %s, status: %s, pid: %s }" % (str(self.id),
                                                                              self.source,
                                                                              self.status,
                                                                              self.pid)


class DeliveryStatus(base_enum.Enum):

    pending = 'pending'

    delivery_in_progress = 'delivery_in_progress'
    delivery_finished = 'delivery_successful'
    delivery_failed = 'delivery_failed'


class DeliveryOrder(SQLAlchemyBase):

    __tablename__ = 'delivery_orders'

    id = Column(Integer, primary_key=True, autoincrement=True)
    delivery_source = Column(String, nullable=False)
    delivery_project = Column(String, nullable=False)

    # TODO Depending on how Mover will work we might not
    # store the delivery status here, but rather poll Mover about it...
    delivery_status = Column(Enum(DeliveryStatus))
    # TODO This should really be enforcing a foreign key constraint
    # against the staging order table, but this does not seem to
    # be simple to get working with sqlite and alembic, so I'm
    # skipping it for now. / JD 20161107
    staging_order_id = Column(Integer)

    def __repr__(self):
        return "Delivery order: {id: %s, source: %s, project: %s, status: %s }" % (str(self.id),
                                                                                   self.delivery_source,
                                                                                   self.delivery_project,
                                                                                   self.delivery_status)