from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base
from config.settings import DATABASE_URL
from utils.logger import get_logger

logger = get_logger("database_connection")

Base = declarative_base()

try:
    engine = create_engine(DATABASE_URL, pool_pre_ping=True, echo=False)
    SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
    logger.info("Engine de banco de dados inicializada com sucesso.")
except Exception as e:
    logger.error(f"Erro ao inicializar conexão com o Banco de Dados: {e}", exc_info=True)
    raise e

def init_db() -> None:
    """Cria de forma síncrona as tabelas estruturadas caso não existam."""
    try:
        Base.metadata.create_all(bind=engine)
        logger.info("Tabelas do banco de dados validadas/criadas com sucesso.")
    except Exception as e:
        logger.error(f"Falha ao gerar o DDL das tabelas: {e}", exc_info=True)
        raise e