
import os
import enum as base_enum
import datetime

from sqlalchemy import Column, Integer, BigInteger, String, Enum, DateTime
from sqlalchemy.ext.declarative import declarative_base

"""
Use this as the base for all database based models. This is used by alembic to know what the tables
should look like in the database, so defining new base classes elsewhere will mean that they will not
be updated properly in the actual database.
"""
SQLAlchemyBase = declarative_base()


class DeliverySource(SQLAlchemyBase):

    __tablename__ = 'delivery_sources'

    # Project name associated with the source
    project_name = Column(String, nullable=False, primary_key=True)

    # The name of the source folder, for a runfolder it will be the
    # runfolder name, for arbitrary project it will be the name of the
    # delivery
    source_name = Column(String, nullable=False, primary_key=True)

    # The path to the source on disk at the time of creation
    path = Column(String, nullable=False)

    batch = Column(Integer, nullable=False, default=1)

    def __repr__(self):
        return "Delivery source: {project_name: %s, source: %s, path: %s, batch: %s}" % \
               (self.project_name,
                self.source_name,
                self.path,
                self.batch)

class StagingStatus(base_enum.Enum):
    """
    Enumerate possible staging statuses
    """

    pending = 'pending'

    staging_in_progress = 'staging_in_progress'
    staging_successful = 'staging_successful'
    staging_failed = 'staging_failed'


class StagingOrder(SQLAlchemyBase):
    """
    Models a order to stage a directory or file. Code using it is responsible for updating
    the staging_target and pid of the process carrying out the staging as this information becomes
    available.
    """

    __tablename__ = 'staging_orders'

    # Unique identified of the staging
    id = Column(Integer, primary_key=True, autoincrement=True)

    # The directory or file which should be staged
    source = Column(String, nullable=False)

    # The current status of the staging order
    status = Column(Enum(StagingStatus), nullable=False)

    # The target path into which the file/directory will be moved
    staging_target = Column(String)

    # The size of the staging order in bytes
    size = Column(BigInteger)

    # The pid of the processes which is carrying out the staging, alternatively which
    # which did do it if the status is no longer in progress.
    pid = Column(Integer)

    def get_staging_path(self):
        return os.path.join(self.staging_target)

    def __repr__(self):
        return "Staging order: {id: %s, source: %s, status: %s, pid: %s }" % (str(self.id),
                                                                              self.source,
                                                                              self.status,
                                                                              self.pid)


class DeliveryStatus(base_enum.Enum):
    """
    Enumerate possible delivery statuses
    """

    pending = 'pending'

    mover_processing_delivery = 'mover_processing_delivery'
    mover_failed_delivery = 'mover_failed_delivery'
    delivery_in_progress = 'delivery_in_progress'
    delivery_successful = 'delivery_successful'
    delivery_failed = 'delivery_failed'
    delivery_skipped = 'delivery_skipped'


class DeliveryOrder(SQLAlchemyBase):
    """
    Models a delivery order
    """

    __tablename__ = 'delivery_orders'

    id = Column(Integer, primary_key=True, autoincrement=True)
    delivery_source = Column(String, nullable=False)
    delivery_project = Column(String, nullable=False)

    # Optional path to md5sum file
    md5sum_file = Column(String)

    # Process id of Mover process used to start the delivery
    mover_pid = Column(Integer)

    # Mover delivery id - the id that is needed to query mover about
    # a delivery status
    mover_delivery_id = Column(String)

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

class NGIStatusAsEnum(base_enum.Enum):
    """
    Enumerate possible delivery statuses given the ngi-status from SUPR
    """
    pending = 'pending'
    successful = 'successful'
    failed = 'failed'

class NGIStatus(SQLAlchemyBase):
    """
    Models the ngi-status from SUPR
    """
    __tablename__ = 'ngi_status'

    order_id = Column(Integer, primary_key=True)  #Order id from table delivery_orders.
    delivery_project = Column(String) #Delivery project from table delivery orders, format deliveryXXXX.
    status = Column(Enum(NGIStatusAsEnum),server_default='pending')#Update dependent on ngi-status in SUPR
    timestamp = Column(DateTime(), default=datetime.datetime.now())

    def __repr__(self):
        return "NGI delivery status:{id: %s, delivery_project: %s, status: %s, timestamp: %s }" % (str(self.order_id),
                                                                                                   self.delivery_project,
                                                                                                   self.status,
                                                                                                   self.timestamp)
