import re
from typing import Optional


class DataSanitizer:
    """Sanitiza dados para remover informações sensíveis"""

    # Padrões de dados sensíveis
    CPF_PATTERN = r'\d{3}\.?\d{3}\.?\d{3}-?\d{2}'  # CPF com ou sem formatação
    CNPJ_PATTERN = r'\d{2}\.?\d{3}\.?\d{3}/?0001-?\d{2}'  # CNPJ
    PHONE_PATTERN = r'\(?[\d]{2,3}\)?[\s.-]?[\d]{4,5}[\s.-]?[\d]{4}'  # Telefone
    EMAIL_PATTERN = r'[\w\.-]+@[\w\.-]+\.\w+'  # Email
    ACCOUNT_PATTERN = r'conta\s*:?\s*\d{4,20}|account\s*:?\s*\d{4,20}'  # Número de conta
    FULL_NAME_PATTERN = r'^[A-Za-záéíóúâêôãõç][\w\s]+[A-Za-záéíóúâêôãõç]$'  # Nomes completos
    ADDRESS_PATTERN = r'(rua|avenida|travessa|praca|largo|estrada|av\.|trav\.|pça\.)\s+[\w\s,.\d]+'

    @staticmethod
    def sanitize_description(description: str) -> str:
        """Remove dados sensíveis de uma descrição"""

        if not description:
            return ""

        sanitizer = DataSanitizer()

        # Remover CPF
        description = re.sub(sanitizer.CPF_PATTERN, '[DOCUMENTO]', description, flags=re.IGNORECASE)

        # Remover CNPJ
        description = re.sub(sanitizer.CNPJ_PATTERN, '[DOCUMENTO]', description, flags=re.IGNORECASE)

        # Remover telefone
        description = re.sub(sanitizer.PHONE_PATTERN, '[TELEFONE]', description, flags=re.IGNORECASE)

        # Remover email
        description = re.sub(sanitizer.EMAIL_PATTERN, '[EMAIL]', description, flags=re.IGNORECASE)

        # Remover número de conta
        description = re.sub(sanitizer.ACCOUNT_PATTERN, '[CONTA]', description, flags=re.IGNORECASE)

        # Remover endereço
        description = re.sub(sanitizer.ADDRESS_PATTERN, '[ENDERECO]', description, flags=re.IGNORECASE)

        # Remover sequências longas de caracteres que possam ser dados sensíveis
        description = re.sub(r'[\w]{20,}', '[DADOS]', description)

        # Limpar espaços múltiplos
        description = re.sub(r'\s+', ' ', description).strip()

        # Se ficou vazio ou muito curto após sanitização, retornar vazio
        if len(description) < 3 or description.count('[') > 2:
            return ""

        return description

    @staticmethod
    def is_sensitive_data(text: str) -> bool:
        """Verifica se o texto contém dados sensíveis"""

        if not text:
            return False

        sanitizer = DataSanitizer()

        # Verificar cada padrão
        patterns = [
            sanitizer.CPF_PATTERN,
            sanitizer.CNPJ_PATTERN,
            sanitizer.PHONE_PATTERN,
            sanitizer.EMAIL_PATTERN,
            sanitizer.ACCOUNT_PATTERN,
            sanitizer.ADDRESS_PATTERN
        ]

        for pattern in patterns:
            if re.search(pattern, text, flags=re.IGNORECASE):
                return True

        return False

    @staticmethod
    def sanitize_file_content(content: str) -> str:
        """Sanitiza conteúdo inteiro de um arquivo"""

        lines = content.split('\n')
        sanitized_lines = []

        for line in lines:
            sanitized_line = DataSanitizer.sanitize_description(line)
            if sanitized_line:  # Apenas adicionar se não ficar vazia
                sanitized_lines.append(sanitized_line)

        return '\n'.join(sanitized_lines)

    @staticmethod
    def mask_sensitive_data(text: str) -> str:
        """Mascara dados sensíveis em vez de remover"""

        if not text:
            return text

        sanitizer = DataSanitizer()

        # Mascarar CPF (mostra apenas últimos 2 dígitos)
        text = re.sub(sanitizer.CPF_PATTERN, lambda m: '***.**.***.XX', text, flags=re.IGNORECASE)

        # Mascarar CNPJ
        text = re.sub(sanitizer.CNPJ_PATTERN, lambda m: '**.**.***/0001-XX', text, flags=re.IGNORECASE)

        # Mascarar telefone
        text = re.sub(sanitizer.PHONE_PATTERN, lambda m: '*XXXXXX*', text, flags=re.IGNORECASE)

        # Mascarar email
        text = re.sub(
            sanitizer.EMAIL_PATTERN,
            lambda m: m.group(0)[:2] + '*' * (len(m.group(0)) - 4) + m.group(0)[-2:],
            text,
            flags=re.IGNORECASE
        )

        # Mascarar número de conta
        text = re.sub(sanitizer.ACCOUNT_PATTERN, 'Conta: XXXXX', text, flags=re.IGNORECASE)

        return text

    @staticmethod
    def extract_sensitive_data_report(content: str) -> dict:
        """Extrai relatório de dados sensíveis encontrados"""

        sanitizer = DataSanitizer()
        report = {
            "cpfs": [],
            "cnpjs": [],
            "phones": [],
            "emails": [],
            "accounts": [],
            "has_sensitive_data": False
        }

        # Encontrar CPFs
        cpfs = re.findall(sanitizer.CPF_PATTERN, content, flags=re.IGNORECASE)
        if cpfs:
            report["cpfs"] = list(set(cpfs))
            report["has_sensitive_data"] = True

        # Encontrar CNPJs
        cnpjs = re.findall(sanitizer.CNPJ_PATTERN, content, flags=re.IGNORECASE)
        if cnpjs:
            report["cnpjs"] = list(set(cnpjs))
            report["has_sensitive_data"] = True

        # Encontrar telefones
        phones = re.findall(sanitizer.PHONE_PATTERN, content, flags=re.IGNORECASE)
        if phones:
            report["phones"] = list(set(phones))
            report["has_sensitive_data"] = True

        # Encontrar emails
        emails = re.findall(sanitizer.EMAIL_PATTERN, content, flags=re.IGNORECASE)
        if emails:
            report["emails"] = list(set(emails))
            report["has_sensitive_data"] = True

        # Encontrar contas
        accounts = re.findall(sanitizer.ACCOUNT_PATTERN, content, flags=re.IGNORECASE)
        if accounts:
            report["accounts"] = list(set(accounts))
            report["has_sensitive_data"] = True

        return report
