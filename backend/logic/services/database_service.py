import json

from sqlalchemy import create_engine, MetaData, func, text
from sqlalchemy.orm import sessionmaker, declarative_base, joinedload
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.exc import SQLAlchemyError
from contextlib import contextmanager
from typing import Type, List, Optional, Tuple
import configparser
from sqlalchemy import desc, asc, not_

Base = declarative_base()


class DatabaseService:
    def __init__(self, config: configparser.ConfigParser):
        db_config = config['database']
        self.db_url = self._create_db_url(db_config)
        self.engine = create_engine(self.db_url, echo=False)  # echo=True for debugging
        self.Session = sessionmaker(bind=self.engine)
        self.metadata = MetaData()
        self.Base = automap_base(metadata=self.metadata)
        self.Base.prepare(autoload_with=self.engine)
        for cls in self.Base.classes.values():
            self.enhance_repr(cls)

    def _create_db_url(self, db_config):
        return f"mysql+mysqlconnector://{db_config['user']}:{db_config['password']}@{db_config['host']}:{db_config['port']}/{db_config['db_name']}"

    def enhance_repr(self, cls):
        """Enhances the __repr__ method of SQLAlchemy models to print informative details."""
        cls.__repr__ = lambda self: "<%s(%s)>" % (
            cls.__class__.__name__,
            ', '.join(["%s=%r" % (key, getattr(self, key)) for key in sorted(self.__table__.columns.keys())])
        )

    @contextmanager
    def get_session(self):
        """Provide a transactional scope around a series of operations."""
        session = self.Session()
        try:
            yield session
            session.commit()
        except Exception as e:
            session.rollback()
            print(f"An error occurred: {e}")
            raise
        finally:
            session.close()

    def query_table(self, table_name: str, filters: Optional[List] = None, limit: Optional[int] = None):
        with self.get_session() as session:
            table_class = getattr(self.Base.classes, table_name)
            query = session.query(table_class)
            if filters:
                query = query.filter(*filters)
            if limit:
                query = query.limit(limit)

            # Using joinedload to eager load all relationships (if any)
            query = query.options(joinedload('*'))
            # Convert each result to a dictionary
            result = [row.__dict__ for row in query.all()]
            # Remove the '_sa_instance_state' key which is added by SQLAlchemy
            for row in result:
                row.pop('_sa_instance_state', None)

            return result

    def query_object(self, model: Type[Base], filters: Optional[List] = None, limit: Optional[int] = None,
                     sort_by: Optional[List[Tuple[str, str]]] = None):
        with self.get_session() as session:
            query = session.query(model)
            if filters:
                query = query.filter(*filters)

            if sort_by:
                for attribute, order in sort_by:
                    if order == 'asc':
                        query = query.order_by(asc(getattr(model, attribute)))
                    elif order == 'desc':
                        query = query.order_by(desc(getattr(model, attribute)))

            if limit:
                query = query.limit(limit)

            # Assuming that the entire object should be loaded completely
            query = query.options(joinedload('*'))
            # Convert each result to a dictionary
            result = [row.__dict__ for row in query.all()]
            # Remove the '_sa_instance_state' key which is added by SQLAlchemy
            for row in result:
                row.pop('_sa_instance_state', None)

            return result

    def query_text(self, sql_text, parameters=None):
        try:
            with self.engine.connect() as connection:
                if parameters:
                    result = connection.execute(text(sql_text), parameters)
                else:
                    result = connection.execute(sql_text).fetchall()
                return result.fetchall()
        except SQLAlchemyError as e:
            print(f"Database error occurred: {e}")
            raise

    def get_column_names_and_types(self, table):
        columns_info = []
        for column in table.columns:
            columns_info.append({
                "name": column.name,
                "type": self.map_column_type(str(column.type).lower())
            })
        return columns_info

    def map_column_type(self, column_type: str):
        if ('text' in column_type or
                'varchar' in column_type or
                'char' in column_type):
            return 'string'

        # if 'int' in column_type:
        if 'int' in column_type or 'decimal' in column_type:
            return 'integer'

        # if 'decimal' in column_type:
        #     return 'float'

        return column_type

    # region SHARED METHODS
    def fetch_course_modules_by_ids(self, object_id, module_id):
        CourseModule = self.Base.classes.mdl_course_modules

        filters = [
            CourseModule.instance == object_id,
            CourseModule.module == module_id,
        ]
        course_modules = self.query_object(CourseModule, filters)
        return course_modules if course_modules else None

    def fetch_related_calendar_events(self, module_name, instance_id):
        Calendar_Event = self.Base.classes.mdl_event

        filter_conditions = [
            Calendar_Event.modulename == module_name,
            Calendar_Event.instance == instance_id,
        ]

        events = self.query_object(Calendar_Event, filter_conditions)
        return events if events else None

    def fetch_assignment_files_by_context_id(self, context_id):
        Files = self.Base.classes.mdl_files
        filter_conditions = [
            Files.contextid == context_id,
            Files.component == "mod_assign",
            not_((Files.filename.like(".")) | (Files.filename.like(""))),
        ]
        rows = self.query_object(Files, filter_conditions)
        return rows if rows else None

    # endregion SHARED METHODS

# Example usage:
if __name__ == "__main__":
    config = configparser.RawConfigParser()
    config.add_section('database')
    config.set('database', 'host', 'localhost')
    config.set('database', 'port', '3306')
    config.set('database', 'user', 'root')
    config.set('database', 'password', 'password')
    config.set('database', 'db_name', 'moodle')
    # Retrieve server configuration
    #host = config.get('database', 'host')
    #port = config.get('database', 'port')

    # Print the server configuration
    #print(f"Server Host: {host}")
    #print(f"Server Port: {port}")

    # Create an instance of the DBService
    db_service = DatabaseService(config)

    # Query the mdl_logstore_standard_log table
    # print("[INFO] READ TOP 10 ROWS IN LOGSTORE TABLE")
    # Log = db_service.Base.classes.mdl_logstore_standard_log
    # filter_conditions = [
    #     Log.action.in_(['created', 'updated']),
    #     Log.other.like('%url%')
    #     # func.JSON_EXTRACT(Log.other, '$.modulename') == 'url'
    # ]
    # data = db_service.query_table('mdl_logstore_standard_log',filters=filter_conditions,  limit=10)
    # for item in data:
    #     #print(item)
    #     print(item['component'], item['eventname'], item['other'])

    # Define your filter conditions
    print("[INFO] READ FILTERED ROWS IN LOGSTORE TABLE")
    Log = db_service.Base.classes.mdl_logstore_standard_log
    filter_conditions = [
        #Log.action.in_(['created', 'updated']),
        #Log.other.like('%url%')
        #func.JSON_EXTRACT(Log.other, '$.modulename') == 'url'
        Log.action == 'created',
        Log.target == 'course_module',
        func.JSON_EXTRACT(Log.other, '$.modulename') == 'url'
    ]

    # Apply the filter conditions and retrieve the results
    data = db_service.query_object(Log, filter_conditions, limit=5)

    # Iterate over the filtered data
    for item in data:
        other_data = json.loads(item['other'])

        # Access the 'instanceid' from the parsed dictionary
        instanceid = other_data['instanceid']

        # Print the instanceid
        print(f"Instance ID: {instanceid}")
        #print(item)
        #print(item.keys())
        #print(f"==Action: {item['action']}, Other: {item['other']}")
        #print(f"--Action: {item.get('action', 'N/A')}, Other: {item.get('other', 'N/A')}")
