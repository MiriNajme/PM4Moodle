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
        db_config = config["database"]
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
            ", ".join(
                [
                    "%s=%r" % (key, getattr(self, key))
                    for key in sorted(self.__table__.columns.keys())
                ]
            ),
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

    def query_table(
        self,
        table_name: str,
        filters: Optional[List] = None,
        limit: Optional[int] = None,
    ):
        with self.get_session() as session:
            table_class = getattr(self.Base.classes, table_name)
            query = session.query(table_class)
            if filters:
                query = query.filter(*filters)
            if limit:
                query = query.limit(limit)

            query = query.options(joinedload("*"))
            result = [row.__dict__ for row in query.all()]
            for row in result:
                row.pop("_sa_instance_state", None)

            return result

    def query_object(
        self,
        model: Type[Base],
        filters: Optional[List] = None,
        limit: Optional[int] = None,
        sort_by: Optional[List[Tuple[str, str]]] = None,
    ):
        with self.get_session() as session:
            query = session.query(model)
            if filters:
                query = query.filter(*filters)

            if sort_by:
                for attribute, order in sort_by:
                    if order == "asc":
                        query = query.order_by(asc(getattr(model, attribute)))
                    elif order == "desc":
                        query = query.order_by(desc(getattr(model, attribute)))

            if limit:
                query = query.limit(limit)

            query = query.options(joinedload("*"))
            result = [row.__dict__ for row in query.all()]
            for row in result:
                row.pop("_sa_instance_state", None)

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
            columns_info.append(
                {
                    "name": column.name,
                    "type": self.map_column_type(str(column.type).lower()),
                }
            )
        return columns_info

    def map_column_type(self, column_type: str):
        if "text" in column_type or "varchar" in column_type or "char" in column_type:
            return "string"

        if "int" in column_type or "decimal" in column_type:
            return "integer"

        return column_type

    # region SHARED METHODS
    def fetch_assignment_files_by_context_id(self, context_id):
        Files = self.Base.classes.mdl_files
        filter_conditions = [
            Files.contextid == context_id,
            Files.component == "mod_assign",
            not_((Files.filename.like(".")) | (Files.filename.like(""))),
        ]
        rows = self.query_object(Files, filter_conditions)
        return rows if rows else None

    def fetch_module_id(self, module_name):
        moduleTypeTable = self.Base.classes.mdl_modules
        filter_conditions = [moduleTypeTable.name.like(f"%{module_name}%")]
        result = self.query_object(moduleTypeTable, filter_conditions)

        if result:
            return result[0].get("id")

        return None

    # endregion SHARED METHODS
