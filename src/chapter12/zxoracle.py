# how to use zxoracle w/o having to move it to sqlalchemy/lib/databases:
# 
# import zxoracle
# from sqlalchemy.engine.url import URL
# def get_dialect(self):
#     return zxoracle.dialect
# URL.get_dialect = get_dialect
# 
# (make the obvious changes if you actually need to use other dialects at the same time)


import re

from sqlalchemy import util, exc, sql, schema as schema
from sqlalchemy.engine import base, default
from sqlalchemy.databases import oracle as _oracle
from sqlalchemy import types as sqltypes

from java.sql import Types as jdbctypes

# todo normalize/denormalize from oracle.py

sa_types = {
    jdbctypes.ARRAY : None, # todo
    jdbctypes.BIGINT: sqltypes.Integer,
    jdbctypes.BINARY: sqltypes.Binary,
    # jdbctypes.BIT : 
    jdbctypes.BLOB : sqltypes.Binary,
    jdbctypes.BOOLEAN : sqltypes.Boolean,
    jdbctypes.CHAR : sqltypes.CHAR,
    jdbctypes.CLOB : sqltypes.Text,
    # jdbctypes.DATALINK : 
    jdbctypes.DATE : sqltypes.Date,
    jdbctypes.DECIMAL : sqltypes.Numeric,
    # jdbctypes.DISTINCT : 
    jdbctypes.DOUBLE : sqltypes.Float,
    jdbctypes.FLOAT : sqltypes.Float,
    jdbctypes.INTEGER : sqltypes.Integer,
    jdbctypes.LONGVARBINARY : sqltypes.Binary,
    jdbctypes.LONGVARCHAR : sqltypes.Text,
    # jdbctypes.NULL : 
    jdbctypes.NUMERIC : sqltypes.Numeric,
    jdbctypes.REAL : sqltypes.Float,
    # jdbctypes.REF : 
    jdbctypes.SMALLINT : sqltypes.Smallinteger,
    jdbctypes.TIME : sqltypes.Time,
    jdbctypes.TIMESTAMP : sqltypes.DateTime,
    jdbctypes.TINYINT : sqltypes.Smallinteger,
    jdbctypes.VARBINARY : sqltypes.Binary,
    jdbctypes.VARCHAR : sqltypes.String,
}

def _jdbc_metadata(saconn):
    return saconn.connection.__connection__.getMetaData()
def _jdbc_row(rs):
    rsmeta = rs.getMetaData()
    size = rsmeta.getColumnCount()
    return tuple([rs.getObject(i) for i in xrange(1, size + 1)])
def _jdbc_fetchall(rs):
    def generate_rows():
        while rs.next():
            yield rs
    return [_jdbc_row(rs) for rs in generate_rows()]

class JDBCDialect(object):
    supports_alter = True
    supports_unicode_statements = True
    supports_sane_rowcount = True
    default_paramstyle = 'qmark'

    def dbapi(cls):
        from com.ziclix.python.sql import zxJDBC
        return zxJDBC
    dbapi = classmethod(dbapi)

    def create_connect_args(self, url):
        opts = dict(url.query)
        driver = opts.pop('driver', self._driver)
        jdbc_url = self._jdbc_prefix + ':@%(host)s:%(port)s:%(database)s' % url.__dict__
        return [jdbc_url, url.username, url.password, driver], opts

    def do_executemany(self, cursor, statement, parameters, context=None):
        if parameters == {}:
            parameters = ()
        rowcount = cursor.executemany(statement, parameters)
        if context is not None:
            context._rowcount = rowcount

    def do_execute(self, cursor, statement, parameters, context=None):
        if parameters == {}:
            parameters = ()
        cursor.execute(statement, parameters)

    def _normalize_name(self, name):
        return name

    def _denormalize_name(self, name):
        return name

    def table_names(self, saconn, schema):
        meta = _jdbc_metadata(saconn)
        rs = meta.getTables(None, schema, '%', None)
        return [self._normalize_name(row[2]) for row in _jdbc_fetchall(rs)]

    def reflecttable(self, saconn, table, include_columns):
        # see http://java.sun.com/j2se/1.4.2/docs/api/java/sql/DatabaseMetaData.html
        meta = _jdbc_metadata(saconn)
        ora_tablename = self._denormalize_name(table.name)
        ora_schema = self._denormalize_name(table.schema)

        # load columns
        rs = meta.getColumns(None, ora_schema, ora_tablename, None)
        while rs.next():
            catalog, _, _, raw_colname, java_data_type, data_type, \
                column_size, _, decimal_digits, radix, _, remarks, \
                default, _, _, char_length, position, is_nullable = _jdbc_row(rs)
            nullable = is_nullable == 'YES'
            colname = self._normalize_name(raw_colname)

            if include_columns and colname not in include_columns:
                continue

            try:
                sa_type = sa_types[java_data_type]
                coltype = self._colspecs[sa_type]
            except KeyError:
                # jdbc OTHER type, or just oracle doing its own thing
                try:
                    coltype = self._ischema_names[data_type]
                except KeyError:
                    util.warn("Did not recognize other type '%s' of column '%s'" %
                              (data_type, colname))
                    coltype = sqltypes.NULLTYPE

            colargs = []
            if default is not None:
                colargs.append(schema.DefaultClause(sql.text(default)))
            table.append_column(schema.Column(colname, coltype, nullable=nullable, *colargs))

        if not table.columns:
            raise AssertionError("Couldn't find any column information for table %s" % table.name)

        # load PK
        rs = meta.getPrimaryKeys(None, ora_schema, ora_tablename)
        rows = _jdbc_fetchall(rs)
        rows.sort(key=lambda row: row[-2]) # sort by key_seq
        for catalog, _, _, raw_colname, key_seq, pk_name in rows:
             colname = self._normalize_name(raw_colname)
             table.primary_key.add(table.c[colname])
        
        # load FKs
        fks = {}
        rs = meta.getImportedKeys(None, ora_schema, ora_tablename)
        rows = _jdbc_fetchall(rs)
        rows.sort(key=lambda row: (row[11], row[8])) # sort by fk, key_seq
        for row in rows:
            # [None, 'HR', 'COUNTRIES', 'COUNTRY_ID', None, 'HR', 'LOCATIONS', 'COUNTRY_ID', 1, None, 1, 'LOC_C_ID_FK', 'COUNTRY_C_ID_PK', 7]
            fk_catalog, fk_raw_schema, fk_raw_tablename, fk_raw_colname, \
                catalog, _, _, raw_colname, \
                key_seq, update_rule, delete_rule, \
                constraint_name, referenced_constraint_name, deferrability = row
            colname = self._normalize_name(raw_colname)
            fk_schema = self._normalize_name(fk_raw_schema)
            fk_tablename = self._normalize_name(fk_raw_tablename)
            fk_colname = self._normalize_name(fk_raw_colname)

            try:
                fk = fks[constraint_name]
            except KeyError:
                fk = ([], [])
                fks[constraint_name] = fk
            if fk_tablename is None:
                # ticket 363
                util.warn(
                    ("Got 'None' querying 'table_name' - does the user have "
                     "proper rights to the table?"))
                continue

            if fk_schema and fk_schema != table.schema:
                refspec =  ".".join([fk_schema, fk_tablename, fk_colname])
                t = schema.Table(fk_tablename, table.metadata, autoload=True, autoload_with=saconn, schema=fk_schema, useexisting=True)
            else:
                refspec =  ".".join([fk_tablename, fk_colname])
                t = schema.Table(fk_tablename, table.metadata, autoload=True, autoload_with=saconn, useexisting=True)

            if colname not in fk[0]:
                fk[0].append(colname)
            if refspec not in fk[1]:
                fk[1].append(refspec)

        for name, value in fks.iteritems():
            table.append_constraint(schema.ForeignKeyConstraint(value[0], value[1], name=name))

    def has_table(self, saconn, table_name, schema=None):
        meta = _jdbc_metadata(saconn)
        rs = meta.getTables(None, schema, self._denormalize_name(table_name), None)
        return rs.next()

    def type_descriptor(self, typeobj):
        return sqltypes.adapt_type(typeobj, self._colspecs)


class ZXOracleDialect(JDBCDialect, default.DefaultDialect):
    """Details of the Oracle dialect.  Not used directly in application code."""
    max_identifier_length = 30
    preexecute_pk_sequences = True
    supports_pk_autoincrement = False

    use_ansi = True

    _driver = 'oracle.jdbc.driver.OracleDriver'
    _jdbc_prefix= 'jdbc:oracle:thin'
    _colspecs = _oracle.colspecs
    _ischema_names = _oracle.ischema_names
    optimize_limits = False

    def _normalize_name(self, name):
        if name is None:
            return None
        elif name.upper() == name and not self.identifier_preparer._requires_quotes(name.lower().decode(self.encoding)):
            return name.lower().decode(self.encoding)
        else:
            return name.decode(self.encoding)

    def _denormalize_name(self, name):
        if name is None:
            return None
        elif name.lower() == name and not self.identifier_preparer._requires_quotes(name.lower()):
            return name.upper().encode(self.encoding)
        else:
            return name.encode(self.encoding)

    def table_names(self, connection, schema):
        # there doesn't seem to be a way to check tablespaces in DatabaseMetaData,
        # so we resort to nonportable code here
        if schema is None:
            s = "select table_name from all_tables where nvl(tablespace_name, 'no tablespace') NOT IN ('SYSTEM', 'SYSAUX')"
            cursor = connection.execute(s)
        else:
            s = "select table_name from all_tables where nvl(tablespace_name, 'no tablespace') NOT IN ('SYSTEM','SYSAUX') AND OWNER = ?"
            cursor = connection.execute(s, self._denormalize_name(schema))
        return [self._normalize_name(row[0]) for row in cursor]

    def sequence_names(self, connection):
        cursor = connection.execute("""select sequence_name from all_sequences""")
        return [self._normalize_name(row[0]) for row in cursor.fetchall()]

    def has_sequence(self, connection, sequence_name):
        cursor = connection.execute("""select sequence_name from all_sequences where sequence_name=?""", self._denormalize_name(sequence_name))
        return cursor.fetchone() is not None

    def get_default_schema_name(self, connection):
        return connection.execute('SELECT USER FROM DUAL').scalar()
    get_default_schema_name = base.connection_memoize(
        ('dialect', 'default_schema_name'))(get_default_schema_name)

    def oid_column_name(self, column):
        if not isinstance(column.table, (sql.TableClause, sql.Select)):
            return None
        else:
            return "rowid"

dialect = ZXOracleDialect
dialect.statement_compiler = _oracle.OracleCompiler
dialect.schemagenerator = _oracle.OracleSchemaGenerator
dialect.schemadropper = _oracle.OracleSchemaDropper
dialect.preparer = _oracle.OracleIdentifierPreparer
dialect.defaultrunner = _oracle.OracleDefaultRunner

