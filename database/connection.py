from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base
from config.settings import DATABASE_URL
from utils.logger import get_logger

logger = get_logger("database_connection")

Base = declarative_base()

# Tenta inicializar com a URL tratada (Psycopg 3). Se falhar por dialeto, faz o fallback seguro.
try:
    logger.info("Tentando conectar usando o driver moderno psycopg (v3)...")
    engine = create_engine(DATABASE_URL, pool_pre_ping=True, echo=False)
    SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
except Exception as e:
    logger.warning(f"Falha ao carregar com driver psycopg v3: {e}. Tentando fallback clássico...")
    try:
        # Força o fallback trocando para o dialeto antigo caso o ambiente exija psycopg2
        fallback_url = DATABASE_URL.replace("postgresql+psycopg://", "postgresql+psycopg2://")
        fallback_url = fallback_url.replace("postgresql://", "postgresql+psycopg2://")
        
        engine = create_engine(fallback_url, pool_pre_ping=True, echo=False)
        SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
        logger.info("Engine de banco de dados inicializada via fallback psycopg2 com sucesso.")
    except Exception as fallback_err:
        logger.error(f"Erro crítico em ambos os drivers de banco de dados: {fallback_err}", exc_info=True)
        raise fallback_err

def init_db() -> None:
    """Cria de forma síncrona as tabelas estruturadas caso não existam."""
    try:
        Base.metadata.create_all(bind=engine)
        logger.info("Tabelas do banco de dados validadas/criadas com sucesso.")
    except Exception as e:
        logger.error(f"Falha ao gerar o DDL das tabelas: {e}", exc_info=True)
        raise e
