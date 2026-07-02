from typing import List, Optional
from sqlalchemy.orm import Session
from models.analise import AnaliseModel
from utils.logger import get_logger
import datetime

logger = get_logger("analise_repository")

class AnaliseRepository:
    def __init__(self, db_session: Session):
        self.db = db_session

    def save(self, analise: AnaliseModel) -> AnaliseModel:
        """Salva ou atualiza um registro de análise no banco de dados."""
        try:
            self.db.add(analise)
            self.db.commit()
            self.db.refresh(analise)
            logger.info(f"Análise ID {analise.id} persistida com sucesso.")
            return analise
        except Exception as e:
            self.db.rollback()
            logger.error(f"Erro ao salvar análise no banco de dados: {e}", exc_info=True)
            raise e

    def get_all(self, search_query: Optional[str] = None, start_date: Optional[datetime.date] = None, end_date: Optional[datetime.date] = None) -> List[AnaliseModel]:
        """Recupera os registros aplicando filtros complexos de busca e intervalo temporal."""
        try:
            query = self.db.query(AnaliseModel)
            
            if start_date:
                query = query.filter(AnaliseModel.created_at >= datetime.datetime.combine(start_date, datetime.time.min))
            if end_date:
                query = query.filter(AnaliseModel.created_at <= datetime.datetime.combine(end_date, datetime.time.max))
            
            if search_query:
                search_filter = f"%{search_query}%"
                query = query.filter(
                    (AnaliseModel.descricao.ilike(search_filter)) | 
                    (AnaliseModel.objetos.ilike(search_filter)) |
                    (AnaliseModel.transcricao.ilike(search_filter))
                )
                
            return query.order_by(AnaliseModel.created_at.desc()).all()
        except Exception as e:
            logger.error(f"Erro ao buscar lista de análises: {e}", exc_info=True)
            return []

    def delete(self, analise_id: int) -> bool:
        """Remove um registro do banco de dados pelo ID."""
        try:
            record = self.db.query(AnaliseModel).filter(AnaliseModel.id == analise_id).first()
            if record:
                self.db.delete(record)
                self.db.commit()
                logger.info(f"Registro {analise_id} removido com sucesso do banco de dados.")
                return True
            return False
        except Exception as e:
            self.db.rollback()
            logger.error(f"Erro ao deletar registro {analise_id}: {e}", exc_info=True)
            return False