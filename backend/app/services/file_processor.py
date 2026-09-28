import csv
import re
from io import StringIO, BytesIO
from datetime import datetime
from typing import List, Dict, Any
import pandas as pd
from app.services.data_sanitizer import DataSanitizer
import logging

logger = logging.getLogger(__name__)


class FileProcessor:
    """Processa arquivos de importação (CSV, PDF, Excel)"""

    def __init__(self):
        self.sanitizer = DataSanitizer()

    def process_file(self, file_content: bytes, file_type: str) -> List[Dict[str, Any]]:
        """Processa arquivo e retorna lista de transações"""

        if file_type == "csv":
            return self._process_csv(file_content)
        elif file_type == "xlsx":
            return self._process_excel(file_content)
        elif file_type == "pdf":
            return self._process_pdf(file_content)
        else:
            raise ValueError(f"Tipo de arquivo não suportado: {file_type}")

    def _process_csv(self, content: bytes) -> List[Dict[str, Any]]:
        """Processa arquivo CSV"""

        text = content.decode('utf-8', errors='ignore')
        csv_file = StringIO(text)
        reader = csv.DictReader(csv_file)

        transactions = []

        for row in reader:
            try:
                transaction = self._parse_transaction_row(row)
                if transaction:
                    transactions.append(transaction)
            except Exception as e:
                logger.warning(f"Erro ao processar linha CSV: {e}")
                continue

        return transactions

    def _process_excel(self, content: bytes) -> List[Dict[str, Any]]:
        """Processa arquivo Excel"""

        excel_file = BytesIO(content)
        df = pd.read_excel(excel_file)

        transactions = []

        for _, row in df.iterrows():
            try:
                row_dict = row.to_dict()
                transaction = self._parse_transaction_row(row_dict)
                if transaction:
                    transactions.append(transaction)
            except Exception as e:
                logger.warning(f"Erro ao processar linha Excel: {e}")
                continue

        return transactions

    def _process_pdf(self, content: bytes) -> List[Dict[str, Any]]:
        """Processa arquivo PDF (extrato bancário)"""

        try:
            from PyPDF2 import PdfReader
        except ImportError:
            raise ImportError("PyPDF2 é necessário para processar PDFs")

        pdf_file = BytesIO(content)
        reader = PdfReader(pdf_file)

        text = ""
        for page in reader.pages:
            text += page.extract_text()

        # Padrões de regex para extrair transações
        # Formato comum: DD/MM/YYYY | Descrição | Valor

        transactions = []

        # Padrão simples: data - descrição - valor
        pattern = r'(\d{2}/\d{2}/\d{4})\s*[|\-]?\s*(.+?)\s*[|\-]?\s*([\d.,]+)'
        matches = re.findall(pattern, text)

        for match in matches:
            try:
                date_str, description, amount_str = match

                # Sanitizar dados
                description = self.sanitizer.sanitize_description(description)
                if not description:
                    continue

                # Parsear data
                try:
                    trans_date = datetime.strptime(date_str, "%d/%m/%Y")
                except ValueError:
                    continue

                # Parsear valor
                amount_str = amount_str.replace(".", "").replace(",", ".")
                try:
                    amount = float(amount_str)
                except ValueError:
                    continue

                # Detectar tipo (income ou expense)
                trans_type = self._detect_transaction_type(description, amount)

                transaction = {
                    "description": description,
                    "amount": amount,
                    "transaction_date": trans_date,
                    "transaction_type": trans_type,
                    "notes": f"Importado de PDF"
                }

                transactions.append(transaction)
            except Exception as e:
                logger.warning(f"Erro ao processar linha PDF: {e}")
                continue

        return transactions

    def _parse_transaction_row(self, row: Dict[str, Any]) -> Dict[str, Any]:
        """Parseia uma linha de transação"""

        # Possíveis nomes de colunas
        date_cols = ["data", "date", "data_transacao", "transaction_date", "quando"]
        desc_cols = ["descricao", "description", "desc", "detalhes", "details"]
        amount_cols = ["valor", "amount", "montante", "quantia"]
        type_cols = ["tipo", "type", "categoria", "category"]

        # Encontrar colunas
        date_value = None
        desc_value = None
        amount_value = None
        type_value = None

        for col in date_cols:
            for key in row.keys():
                if key.lower() == col.lower():
                    date_value = row[key]
                    break

        for col in desc_cols:
            for key in row.keys():
                if key.lower() == col.lower():
                    desc_value = row[key]
                    break

        for col in amount_cols:
            for key in row.keys():
                if key.lower() == col.lower():
                    amount_value = row[key]
                    break

        for col in type_cols:
            for key in row.keys():
                if key.lower() == col.lower():
                    type_value = row[key]
                    break

        if not date_value or not desc_value or not amount_value:
            return None

        # Parsear data
        try:
            if isinstance(date_value, str):
                # Tentar formatos comuns
                for fmt in ["%d/%m/%Y", "%Y-%m-%d", "%d-%m-%Y"]:
                    try:
                        trans_date = datetime.strptime(date_value, fmt)
                        break
                    except ValueError:
                        continue
            else:
                trans_date = pd.to_datetime(date_value)
        except:
            return None

        # Parsear valor
        try:
            amount_str = str(amount_value).replace(".", "").replace(",", ".")
            amount = float(amount_str)
        except:
            return None

        # Sanitizar descrição
        description = self.sanitizer.sanitize_description(str(desc_value))
        if not description:
            return None

        # Detectar tipo
        if type_value:
            trans_type = "income" if str(type_value).lower() in ["receita", "income", "entrada"] else "expense"
        else:
            trans_type = self._detect_transaction_type(description, amount)

        return {
            "description": description,
            "amount": amount,
            "transaction_date": trans_date,
            "transaction_type": trans_type
        }

    def _detect_transaction_type(self, description: str, amount: float) -> str:
        """Detecta se é receita ou despesa"""

        income_keywords = ["salario", "salary", "receita", "revenue", "income", "deposito", "transfer in", "entrada"]
        expense_keywords = ["compra", "purchase", "pagamento", "payment", "debit", "saida", "withdrawal"]

        desc_lower = description.lower()

        for keyword in income_keywords:
            if keyword in desc_lower:
                return "income"

        for keyword in expense_keywords:
            if keyword in desc_lower:
                return "expense"

        # Padrão: valor negativo = despesa
        return "expense" if amount < 0 else "income"
